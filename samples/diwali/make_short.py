"""Vertical YouTube Short (1080x1920, under 3 minutes) cut from the long build.

usage: .venv/bin/python make_short.py --build ~/Movies/diwali-build --work ~/Movies/diwali-short [--scenes 1,6,9,11,13]

Reuses the long build's trimmed presenter clips (pres/NN.mp4, keyed NN_key.mov) and voice (voice/NN.wav), so the takes
are read once. Per the Shorts recipe: his frame scaled 1.4x and shifted down 280 px (face about 600-950 px, clear of the captions at 1230-1400), matted onto
the scene clip (dimmed, softened); full-screen scene for voice-only beats; word-synced captions at 62-70% of frame height;
a short label at the top and the source line at the bottom. A scene can be cut after a given word (TRIM) so a lead-in to a
dropped scene does not dangle.
"""
import argparse, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make_long as ml, captions

W, H = 1080, 1920
FF = ml.FF_FULL
DEFAULT = [1, 6, 9, 11, 13]
TRIM = {9: 23.45}                 # scene 9 ends after "...Guinness World Record mein register" (speech ends 23.3 s; the economy lead-in follows)
TOP = {"hook": "DIWALI · 1,000+ SAAL PURANI ROSHNI", "rama": "SHRI RAM KA AYODHYA LAUTNA", "ayodhya": "26,17,215 DIYE · GUINNESS WORLD RECORD",
       "reflection": "EK CHHOTA SA DIYA", "wishes": "SHUBH DEEPAVALI"}
BG = {"hook": "d_hook_diyas", "rama": "d_deepavali", "ayodhya": "d_ghats", "reflection": "d_one_diya", "wishes": "d_hook_diyas"}


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"failed: {' '.join(cmd[:8])}\n{r.stderr[-1500:]}")
    return r


def dur(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def ass_short(path, phr, offset, top, source, dur_s):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,{captions.FONT},80,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,-1,0,0,0,100,100,0,0,1,3.4,0,2,60,60,520,1
Style: TOP,Helvetica Neue,46,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,-1,0,0,0,100,100,2,0,1,2.6,0,8,60,60,150,1
Style: SRC,Helvetica Neue,26,&H00C8CFD6,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,1,0,1,1.8,0,2,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    if top: ev.append(f"Dialogue: 0,{captions._ts(0.3)},{captions._ts(dur_s - 0.3)},TOP,,0,0,0,,{top}")
    if source: ev.append(f"Dialogue: 0,{captions._ts(0.3)},{captions._ts(dur_s - 0.3)},SRC,,0,0,0,,{source}")
    for pi, p in enumerate(phr):
        nxt = phr[pi + 1][0]["start"] if pi + 1 < len(phr) else None
        for i in range(len(p)):
            a = p[i]["start"] + offset
            end = p[-1]["end"] + captions.HOLD
            if nxt is not None: end = min(end, nxt - 0.02)
            b = (p[i + 1]["start"] if i + 1 < len(p) else end) + offset
            if b - a < 0.04: b = a + 0.04
            ev.append(f"Dialogue: 1,{captions._ts(a)},{captions._ts(b)},T,,0,0,0,,{' '.join(x['word'] for x in p[:i + 1])}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")
    return path.replace(":", "\\:")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default=os.path.join(HERE, "script.long.json"))
    ap.add_argument("--build", required=True); ap.add_argument("--work", required=True)
    ap.add_argument("--scenes", default=",".join(map(str, DEFAULT)))
    a = ap.parse_args()
    keep = [int(x) for x in a.scenes.split(",")]
    work = os.path.abspath(a.work); build = os.path.abspath(a.build)
    for d in ("pres", "voice", "seg", "out"): os.makedirs(os.path.join(work, d), exist_ok=True)
    allsc = json.load(open(a.script, encoding="utf-8"))["scenes"]
    scenes = [s for s in allsc if s["n"] in keep]

    print("1/4 voice, words and trims")
    wavs = {s["n"]: os.path.join(build, "voice", f"{s['n']:02d}.wav") for s in scenes}
    trans = ml.transcribe(wavs)
    durs, caps, pres = {}, {}, {}
    for s in scenes:
        n = s["n"]
        words = captions.correct(trans[n]["words"], s.get("text_dev") or s["text"])
        src_mp4 = os.path.join(build, "pres", f"{n:02d}.mp4"); key = os.path.join(build, "pres", f"{n:02d}_key.mov")
        src = key if os.path.exists(key) else src_mp4
        cut = None
        if n in TRIM:
            if isinstance(TRIM[n], (int, float)): cut = float(TRIM[n])          # seconds into the trimmed take
            else:
                hits = [w for w in words if captions._norm(w["word"]).startswith(TRIM[n])]
                if hits: cut = hits[-1]["end"] + 0.3
            if cut: words = [dict(w, end=min(w["end"], cut)) for w in words if w["start"] < cut - 0.05]
        pres[n] = os.path.join(work, "pres", os.path.basename(src)); wav = os.path.join(work, "voice", f"{n:02d}.wav")
        if cut:
            sh([FF, "-y", "-loglevel", "error", "-i", src, "-t", f"{cut:.3f}", "-c", "copy", pres[n]])
            sh([FF, "-y", "-loglevel", "error", "-i", wavs[n], "-t", f"{cut:.3f}", "-c", "copy", wav])
        else:
            shutil.copy(src, pres[n]); shutil.copy(wavs[n], wav)
        durs[n] = dur(wav); caps[n] = captions.phrases(words)
        print(f"  {n:02d} {s['id']}: {durs[n]:.1f}s{f' (cut at {cut:.1f}s)' if cut else ''}")
    tl = ml.build_timeline(scenes, durs, captions=True)
    tl_path = os.path.join(work, "timeline.short.json"); json.dump(tl, open(tl_path, "w"), indent=1)
    print(f"  total {tl['total']:.1f}s")
    if tl["total"] > 180: sys.exit("over 3 minutes: drop a scene or add a TRIM")

    print("2/4 scenes")
    segs = []
    for s, t in zip(scenes, tl["scenes"]):
        n, d = s["n"], t["dur"]
        frames = os.path.join(HERE, "assets", "ai", BG[s["id"]])
        if not os.path.isdir(frames): sys.exit(f"missing clip frames {frames}; run the long build first")
        onscreen = s.get("layout", "F") in ("C", "L")
        soften = ",gblur=sigma=5,eq=brightness=-0.10:saturation=0.95" if onscreen else ",eq=brightness=-0.03"
        bg = f"[0:v]scale=-2:{H}:flags=lanczos,crop={W}:{H},fps={ml.FPS}{soften}[bg]"
        ass = ass_short(os.path.join(work, "seg", f"{n:02d}.ass"), caps[n], t["pre"], TOP.get(s["id"], ""),
                        (s.get("source") or "") + ("   ·   AI ILLUSTRATION" if BG[s["id"]].startswith("d_") else ""), d)
        out = os.path.join(work, "seg", f"{n:02d}.mp4"); segs.append(out)
        inp = ["-stream_loop", "-1", "-framerate", str(ml.FPS), "-i", os.path.join(frames, "%05d.jpg")]
        if onscreen:
            pad = f"tpad=start_duration={t['pre']}:start_mode=clone:stop_duration={t['post'] + 0.5}:stop_mode=clone"
            pv = (f"[1:v]{pad},scale={int(1080 * 1.4)}:{int(1920 * 1.4)},format=yuva420p,"
                  f"fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={d - 0.25:.3f}:d=0.25:alpha=1[p]")
            fc = f"{bg};{pv};[bg][p]overlay=-216:280:shortest=0:eof_action=pass[v0];[v0]subtitles={ass}[v]"
            sh([FF, "-y", "-loglevel", "error", *inp, "-i", pres[n], "-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-an", out])
        else:
            sh([FF, "-y", "-loglevel", "error", *inp, "-filter_complex", f"{bg};[bg]subtitles={ass}[v]", "-map", "[v]", "-t", f"{d:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-an", out])
        print(f"  {n:02d} done")
    lst = os.path.join(work, "seg", "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    video = os.path.join(work, "out", "video.mp4")
    sh([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])

    print("3/4 sound")
    r = subprocess.run([sys.executable, os.path.join(HERE, "sound2.py"), tl_path, os.path.join(work, "voice"), os.path.join(work, "out")], capture_output=True, text=True)
    mix = os.path.join(work, "out", "mix.wav")
    if r.returncode or not os.path.exists(mix):
        print("  sound2 failed on this subset; voice-only mix at -14 LUFS\n" + r.stderr[-600:])
        parts = sum([["-i", os.path.join(work, "voice", f"{s['n']:02d}.wav")] for s in scenes], [])
        delays = ";".join(f"[{i}:a]adelay={int(t['vo_at'] * 1000)}:all=1[a{i}]" for i, t in enumerate(tl["scenes"]))
        sh([FF, "-y", "-loglevel", "error", *parts, "-filter_complex", f"{delays};{''.join(f'[a{i}]' for i in range(len(scenes)))}amix=inputs={len(scenes)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11", mix])

    print("4/4 export")
    import re
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", subprocess.run([FF, "-nostats", "-i", mix, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)
    gain = -14.0 - float(m.group(1)) if m else 0.0
    print(f"  mix {m.group(1) if m else '?'} LUFS -> {gain:+.1f} dB to -14")
    final = os.path.join(work, "out", "short.mp4")
    sh([FF, "-y", "-loglevel", "error", "-i", video, "-i", mix, "-map", "0:v", "-map", "1:a", "-af", f"volume={gain:.2f}dB", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final])
    srt, i = [], 1
    for t in tl["scenes"]:
        cues, i = captions.srt_lines(caps[t["n"]], t["vo_at"], i); srt += cues
    open(os.path.join(work, "out", "short.srt"), "w", encoding="utf-8").write("\n".join(srt))
    print("done:", final, f"{os.path.getsize(final) / 1e6:.0f} MB, {dur(final):.1f}s")


if __name__ == "__main__":
    main()
