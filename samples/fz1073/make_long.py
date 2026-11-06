"""Merge Rahul's recorded takes with the Claude-rendered graphics into the final long video.

usage:
  python make_long.py --script script.long.json --takes <folder of 01.mp4 ...> --work <work dir>
                      [--scenes 1,5,8] [--workers 3] [--skip-render]

Outputs in <work>/out: final.mp4, subtitles.srt, chapters.txt, report.md
Original takes are only read, never modified.
"""
import argparse, glob, json, math, os, re, shutil, subprocess, sys, time, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
FPS = 30
PRE = {"title": 1.2, "question": 1.0}
POST = {"end": 1.8, "plunge": 0.8, "attack": 0.6}
CARD_W, CARD_H = 560, 996          # presenter card in L layout (9:16)
C_W, C_H = 608, 1080               # presenter in C layout (9:16, full height)


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=kw.pop("text", True), **kw)
    if r.returncode:
        sys.exit(f"command failed: {' '.join(cmd[:6])} ...\n{r.stderr[-2000:]}")
    return r


def probe(path):
    j = json.loads(sh(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", path]).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []):
        if "rotation" in sd:
            rot = int(float(sd["rotation"]))
    rot = int(v.get("tags", {}).get("rotate", rot))
    if abs(rot) % 180 == 90:
        w, h = h, w
    return {"w": w, "h": h, "dur": float(j["format"]["duration"]), "has_audio": any(s["codec_type"] == "audio" for s in j["streams"])}


def pick_takes(folder, scenes):
    files = [f for f in glob.glob(os.path.join(folder, "**", "*"), recursive=True)
             if re.search(r"\.(mp4|mov|m4v|mkv)$", f, re.I)]
    out = {}
    for s in scenes:
        cand = []
        for f in files:
            m = re.match(r"^0*(\d+)(?:[_\- ](\d+))?\b", os.path.basename(f))
            if m and int(m.group(1)) == s["n"]:
                cand.append((int(m.group(2) or 1), f))
        if cand:
            out[s["n"]] = sorted(cand)[-1][1]
    return out


def load_audio(path):
    raw = sh(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"], text=False).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def keep_segments(a, head=0.15, tail=0.30, max_gap=0.75, keep_gap=0.45):
    """Energy-based trim: drop leading/trailing silence, shorten long internal pauses."""
    hop = int(0.02 * SR)
    n = len(a) // hop
    if n == 0:
        return [(0.0, len(a) / SR)]
    rms = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    floor, top = np.percentile(db, 10), np.percentile(db, 97)
    thr = floor + 0.35 * (top - floor)
    voiced = db > thr
    # hangover: fill gaps shorter than 200 ms
    k = 10
    idx = np.where(voiced)[0]
    if len(idx) == 0:
        return [(0.0, len(a) / SR)]
    segs, s0, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > k:
            segs.append((s0, prev + 1)); s0 = i
        prev = i
    segs.append((s0, prev + 1))
    t = lambda i: i * hop / SR
    out = []
    start = max(0.0, t(segs[0][0]) - head)
    cur_a = start
    for (a0, a1), (b0, _) in zip(segs, segs[1:]):
        gap = t(b0) - t(a1)
        if gap > max_gap:
            out.append((cur_a, t(a1) + keep_gap / 2))
            cur_a = t(b0) - keep_gap / 2
    out.append((cur_a, min(len(a) / SR, t(segs[-1][1]) + tail)))
    return out


def cut_presenter(take, info, segs, dst_mp4, dst_wav):
    parts, fc = [], []
    for i, (a, b) in enumerate(segs):
        fc.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]")
        parts.append(f"[v{i}][a{i}]")
    vert = info["h"] >= info["w"]
    frame = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" if vert \
        else "crop=ih*9/16:ih,scale=1080:1920"
    fc.append("".join(parts) + f"concat=n={len(segs)}:v=1:a=1[cv][ca];[cv]{frame},fps={FPS},format=yuv420p[vo];[ca]aresample={SR},pan=mono|c0=c0[ao]")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", take, "-filter_complex", ";".join(fc),
        "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17",
        "-c:a", "pcm_s16le", "-ar", str(SR), dst_mp4])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", dst_mp4, "-vn", "-ac", "1", "-ar", str(SR), dst_wav])
    return probe(dst_mp4)["dur"]


def transcribe(wavs):
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    from faster_whisper import WhisperModel
    model = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="cpu", compute_type="int8")
    res = {}
    for n, w in wavs.items():
        segs, _ = model.transcribe(_resample16(w), language="hi")
        res[n] = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segs]
    return res


def _resample16(path):
    raw = sh(["ffmpeg", "-loglevel", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], text=False).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_timeline(scenes, durs):
    t, out = 0.0, []
    for s in scenes:
        pre, post = PRE.get(s["id"], 0.35), POST.get(s["id"], 0.5)
        dur = pre + durs[s["n"]] + post
        out.append({"n": s["n"], "id": s["id"], "look": s["look"], "layout": s.get("layout", "F"),
                    "chapter": s.get("chapter", ""), "phrases": s.get("phrases", []), "params": s.get("params"),
                    "source": s.get("source", ""), "photos": s.get("photos", []), "photo_style": s.get("photo_style"), "alarm": s.get("alarm"), "start": round(t, 3), "dur": round(dur, 3),
                    "vo_at": round(t + pre, 3), "vo_dur": round(durs[s["n"]], 3), "pre": pre, "post": post})
        t += dur
    return {"fps": FPS, "total": round(t, 3), "scenes": out}


def render_frames(work, tl_name, out_dir, workers):
    total = int(json.load(open(os.path.join(HERE, tl_name)))["total"] * FPS)
    env = dict(os.environ, TL=tl_name, OUT=out_dir)
    procs = [subprocess.Popen(["node", "render.js", str(k), str(total), str(workers)], cwd=HERE, env=env,
                              stdout=open(os.path.join(work, f"render{k}.log"), "w"), stderr=subprocess.STDOUT)
             for k in range(workers)]
    t0 = time.time()
    while any(p.poll() is None for p in procs):
        time.sleep(20)
        done = len(os.listdir(os.path.join(HERE, out_dir)))
        print(f"  render {done}/{total} frames, {time.time() - t0:.0f}s", flush=True)
    if any(p.returncode for p in procs):
        sys.exit("render worker failed, see render*.log")
    return total


def composite(work, tl, frames_dir, pres):
    segs = []
    for s in tl["scenes"]:
        f0, f1 = round(s["start"] * FPS), round((s["start"] + s["dur"]) * FPS)
        out = os.path.join(work, "seg", f"{s['n']:02d}.mp4")
        g = ["-framerate", str(FPS), "-start_number", str(f0), "-i", os.path.join(HERE, frames_dir, "%05d.jpg")]
        common = ["-frames:v", str(f1 - f0), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-an", out]
        lay = s["layout"]
        if lay == "F":
            sh(["ffmpeg", "-y", "-loglevel", "error", *g, *common])
        else:
            d = s["dur"]
            pad = f"tpad=start_duration={s['pre']}:start_mode=clone:stop_duration={s['post'] + 0.5}:stop_mode=clone"
            if lay == "L":
                pv = (f"[1:v]{pad},scale={CARD_W}:{CARD_H},pad={CARD_W + 8}:{CARD_H}:8:0:color=0xe0312e,format=yuva420p,"
                      f"fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={d - 0.25:.3f}:d=0.25:alpha=1[p]")
                x, y = 1920 - CARD_W - 8 - 84, (1080 - CARD_H) // 2
            else:
                pv = (f"[1:v]{pad},scale={C_W}:{C_H},format=yuva420p,"
                      f"fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={d - 0.25:.3f}:d=0.25:alpha=1[p]")
                x, y = (1920 - C_W) // 2, 0
            sh(["ffmpeg", "-y", "-loglevel", "error", *g, "-i", pres[s["n"]], "-filter_complex",
                f"{pv};[0:v][p]overlay={x}:{y}:shortest=0:eof_action=pass[v]", "-map", "[v]", *common])
        segs.append(out)
    lst = os.path.join(work, "seg", "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    return lst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default=os.path.join(HERE, "script.long.json"))
    ap.add_argument("--takes", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--scenes", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--skip-render", action="store_true")
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    for d in ("pres", "voice", "seg", "out"):
        os.makedirs(os.path.join(work, d), exist_ok=True)
    script = json.load(open(a.script))
    scenes = script["scenes"]
    if a.scenes:
        keep = {int(x) for x in a.scenes.split(",")}
        scenes = [s for s in scenes if s["n"] in keep]

    print("1/6 matching takes")
    takes = pick_takes(a.takes, scenes)
    missing = [s["n"] for s in scenes if s["n"] not in takes]
    if missing:
        sys.exit(f"missing takes for scenes: {missing}. Name files 01.mp4, 02.mp4 ...")

    print("2/6 trimming silences and conforming to 1080x1920")
    durs, pres, wavs, report = {}, {}, {}, []
    for s in scenes:
        n, take = s["n"], takes[s["n"]]
        info = probe(take)
        if not info["has_audio"]:
            sys.exit(f"take {take} has no audio track")
        segs = keep_segments(load_audio(take))
        pres[n] = os.path.join(work, "pres", f"{n:02d}.mp4")
        wavs[n] = os.path.join(work, "voice", f"{n:02d}.wav")
        durs[n] = cut_presenter(take, info, segs, pres[n], wavs[n])
        expect = len(s["text"].split()) / 140 * 60
        flag = "CHECK" if not (0.6 * expect <= durs[n] <= 1.6 * expect) else "ok"
        report.append((n, os.path.basename(take), info["dur"], durs[n], len(segs), expect, flag))
        print(f"  {n:02d} {os.path.basename(take)}: {info['dur']:.1f}s -> {durs[n]:.1f}s ({flag})")

    print("3/6 transcribing with Whisper")
    trans = transcribe(wavs)

    print("4/6 building timeline and rendering graphics")
    tl = build_timeline(scenes, durs)
    tl_name = "timeline.long.json"
    json.dump(tl, open(os.path.join(HERE, tl_name), "w"), indent=1)
    frames_dir = "frames_long"
    fd = os.path.join(HERE, frames_dir)
    if not a.skip_render:
        if os.path.isdir(fd):
            shutil.rmtree(fd)
        os.makedirs(fd)
        render_frames(work, tl_name, frames_dir, a.workers)

    print("5/6 compositing presenter and graphics")
    lst = composite(work, tl, frames_dir, pres)
    video = os.path.join(work, "out", "video.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])

    print("6/6 sound design, mix, export")
    sh([sys.executable, os.path.join(HERE, "sound2.py"), os.path.join(HERE, tl_name), os.path.join(work, "voice"), os.path.join(work, "out")])
    final = os.path.join(work, "out", "final.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", os.path.join(work, "out", "mix.wav"),
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "6.5M", "-bufsize", "13M",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final])

    # subtitles (Whisper text, Devanagari) and chapters
    srt, i = [], 1
    for s in tl["scenes"]:
        for seg in trans.get(s["n"], []):
            srt.append(f"{i}\n{srt_time(s['vo_at'] + seg['start'])} --> {srt_time(s['vo_at'] + seg['end'])}\n{seg['text']}\n"); i += 1
    open(os.path.join(work, "out", "subtitles.srt"), "w").write("\n".join(srt))
    ch, seen = ["0:00 Intro"], set()
    for s in tl["scenes"]:
        c = s["chapter"]
        if c and c not in seen:
            seen.add(c); m, sec = divmod(int(s["start"]), 60)
            ch.append(f"{m}:{sec:02d} {c.split('·', 1)[-1].strip().title()}")
    open(os.path.join(work, "out", "chapters.txt"), "w").write("\n".join(ch) + "\n")
    rep = ["| Scene | Take | Raw s | Cut s | Pieces | Expected s | Check |", "| --- | --- | --- | --- | --- | --- | --- |"]
    rep += [f"| {n:02d} | {t} | {r:.1f} | {c:.1f} | {p} | {e:.1f} | {f} |" for n, t, r, c, p, e, f in report]
    rep += ["", "## Whisper transcript per scene", ""] + [f"- **{n:02d}**: " + " ".join(x["text"] for x in trans[n]) for n in sorted(trans)]
    open(os.path.join(work, "out", "report.md"), "w").write("\n".join(rep) + "\n")
    print("done:", final, f"{os.path.getsize(final) / 1e6:.0f} MB, {tl['total']:.1f}s")


if __name__ == "__main__":
    main()
