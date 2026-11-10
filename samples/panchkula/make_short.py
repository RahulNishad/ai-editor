"""Vertical YouTube Short (1080x1920) built straight from his Short takes, or as a scratch-voice direction preview.

usage:
  direction preview (Piper voice, YOUR CLIP slots):  .venv/bin/python make_short.py --direction --work ~/Movies/panchkula-short-direction
  final from his takes:                              .venv/bin/python make_short.py --takes ~/Movies/panchkula-short-takes --work ~/Movies/panchkula-short

Unlike the Diwali Short (cut out of the long build), this one has its own script (`script.short.json`) recorded separately,
so it runs the long pipeline's first stages itself: match takes, trim silences, conform to 1080x1920, key the green cloth,
Whisper word timings. Per the Shorts recipe: his frame scaled 1.15x and matted onto the scene photo (dimmed, softened,
slow push-in); voice-only fact scenes show the photo sharp; word-synced captions at about 70% of frame height; the
scene's `top` label at the top, its `source` line at the bottom; a 2.5 s end card. Gaps are tight (0.2 s in, 0.25 s out).
"""
import argparse, json, os, re, shutil, subprocess, sys, wave
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import make_long as ml, captions

W, H = 1080, 1920
FF = ml.FF_FULL
END_SECONDS = 2.5
END_TOP = "THINK WITH RAHUL NISHAD · THINK BEYOND HEADLINES!"
END_LINES = ["LIKE · SHARE · SUBSCRIBE", "Aaj raat apne bachche se ek sawaal poochiye:", "'aaj tumhe kis baat par gussa aaya?'"]


class Gap(dict):
    def __init__(self, v): self.v = v
    def get(self, k, d=None): return self.v


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(f"failed: {' '.join(cmd[:8])}\n{r.stderr[-1500:]}")
    return r


def dur(p): return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def silent_wav(path, seconds):
    with wave.open(path, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(ml.SR); w.writeframes(b"\x00\x00" * int(seconds * ml.SR))


def esc(t): return t.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def ass_short(path, phr, offset, top, source, dur_s, slot=None, big=None):
    """Captions plus the top label and source line; `slot` draws the YOUR CLIP placeholder, `big` centred end-card lines."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,{captions.FONT},80,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,-1,0,0,0,100,100,0,0,1,3.4,0,2,60,60,520,1
Style: TOP,Helvetica Neue,44,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,-1,0,0,0,100,100,2,0,1,2.6,0,8,60,60,64,1
Style: SRC,Helvetica Neue,24,&H00C8CFD6,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,1,0,1,1.8,0,2,60,60,70,1
Style: SLOT,Helvetica Neue,54,&H00FFFFFF,&H00FFFFFF,&H00802020,&H96000000,-1,0,0,0,100,100,1,0,1,3,0,5,80,80,0,1
Style: BIG,Helvetica Neue,60,&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,-1,0,0,0,100,100,1,0,1,3,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    a0, a1 = captions._ts(0.3), captions._ts(dur_s - 0.3)
    ev = []
    if top: ev.append(f"Dialogue: 0,{a0},{a1},TOP,,0,0,0,,{esc(top)}")
    if source: ev.append(f"Dialogue: 0,{a0},{a1},SRC,,0,0,0,,{esc(source)}")
    if slot: ev.append(f"Dialogue: 0,{a0},{a1},SLOT,,0,0,0,,{esc(slot)}")
    if big:
        text = "\\N".join(esc(x) for x in big)
        ev.append(f"Dialogue: 0,{a0},{a1},BIG,,0,0,0,,{text}")
    for pi, p in enumerate(phr or []):
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


def bg_input(s):
    key = next((p["src"] for p in s.get("photos") or [] if p.get("src")), None)
    if key:
        d = os.path.join(HERE, "assets", "ai", key)
        if os.path.isdir(d): return ["-stream_loop", "-1", "-framerate", str(ml.FPS), "-i", os.path.join(d, "%05d.jpg")], True
        p = os.path.join(HERE, "assets", "photos", key + ".jpg")
        if os.path.exists(p): return ["-loop", "1", "-framerate", str(ml.FPS), "-i", p], False
    sys.exit(f"no background photo for scene {s['n']} ({key}); run commons.py first")


def bg_filter(d, onscreen, moving):
    """Fill the frame from the 16:9 photo and push in slowly (1.0 -> 1.06 over the scene); dim and soften behind him."""
    soften = ",gblur=sigma=5,eq=brightness=-0.12:saturation=0.9" if onscreen else ",eq=brightness=-0.05:saturation=0.95"
    if moving: return f"[0:v]scale=-2:{H}:flags=lanczos,crop={W}:{H},fps={ml.FPS}{soften}[bg]"
    big = int(H * 1.08)
    return (f"[0:v]scale=-2:{big}:flags=lanczos,fps={ml.FPS},"
            f"crop={W}:{H}:x=(iw-{W})/2:y=(ih-{H})/2,"
            f"zoompan=z='1+0.06*on/({d:.3f}*{ml.FPS})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={ml.FPS}{soften}[bg]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default=os.path.join(HERE, "script.short.json"))
    ap.add_argument("--takes"); ap.add_argument("--direction", action="store_true", help="scratch voice and YOUR CLIP slots instead of takes")
    ap.add_argument("--work", required=True)
    ap.add_argument("--key", default="auto", choices=["auto", "on", "off"])
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    if not a.takes and not a.direction: sys.exit("give --takes <folder> or --direction")
    work = os.path.abspath(a.work)
    for d in ("pres", "voice", "seg", "out"): os.makedirs(os.path.join(work, d), exist_ok=True)
    script = json.load(open(a.script, encoding="utf-8")); scenes = script["scenes"]

    durs, pres, wavs, caps, report = {}, {}, {}, {}, []
    if a.direction:
        print("1/4 scratch voice")
        import make_direction as md
        for s in scenes:
            wavs[s["n"]] = os.path.join(work, "voice", f"{s['n']:02d}.wav")
            durs[s["n"]] = md.scratch_voice(s.get("text_dev") or s["text"], wavs[s["n"]])
            print(f"  {s['n']:02d} {s['id']}: {durs[s['n']]:.1f}s")
        # the preview carries the scripted line as its transcript, split evenly over the scratch voice
        for s in scenes:
            ws = (s.get("text_dev") or s["text"]).split(); step = durs[s["n"]] / max(1, len(ws))
            caps[s["n"]] = captions.phrases([{"start": i * step, "end": (i + 1) * step, "word": w} for i, w in enumerate(ws)])
    else:
        print("1/4 takes: match, trim, conform, key, transcribe")
        takes = ml.pick_takes(a.takes, scenes)
        missing = [s["n"] for s in scenes if s["n"] not in takes]
        if missing: sys.exit(f"missing takes for scenes: {missing}. Name files 01.mp4, 02.mp4 ...")
        for s in scenes:
            n, take = s["n"], takes[n]; info = ml.probe(take)
            if not info["has_audio"]: sys.exit(f"take {take} has no audio track")
            segs = ml.keep_segments(ml.load_audio(take))
            pres[n] = os.path.join(work, "pres", f"{n:02d}.mp4"); wavs[n] = os.path.join(work, "voice", f"{n:02d}.wav")
            durs[n] = ml.cut_presenter(take, info, segs, pres[n], wavs[n])
            expect = len(s["text"].split()) / 150 * 60
            flag = "CHECK" if not (0.6 * expect <= durs[n] <= 1.6 * expect) else "ok"
            report.append(f"{n:02d} {os.path.basename(take)}: {info['dur']:.1f}s -> {durs[n]:.1f}s, expected about {expect:.0f}s ({flag})")
            print("  " + report[-1])
        on = [s for s in scenes if s.get("layout", "F") in ("C", "L")]
        if a.key == "on" or (a.key == "auto" and on and ml.is_green_screen(pres[on[0]["n"]])):
            print("  keying the green cloth")
            pres = ml.key_presenters(pres, scenes, work, a.workers)
        trans = ml.transcribe(wavs)
        for s in scenes: caps[s["n"]] = captions.phrases(captions.correct(trans[s["n"]]["words"], s.get("text_dev") or s["text"]))

    # end card: a voice-less pseudo scene so the timeline, sound bed and segments line up
    end = {"n": 99, "id": "end", "layout": "F", "look": "end", "text": "", "photos": scenes[-1]["photos"], "_end": True}
    durs[99] = END_SECONDS - 0.45; caps[99] = []; silent_wav(os.path.join(work, "voice", "99.wav"), durs[99])
    scenes = scenes + [end]
    ml.PRE, ml.POST = Gap(0.2), Gap(0.25)
    tl = ml.build_timeline(scenes, durs, captions=True)
    tl_path = os.path.join(work, "timeline.short.json"); json.dump(tl, open(tl_path, "w"), indent=1)
    print(f"  total {tl['total']:.1f}s")
    if tl["total"] > 180: sys.exit("over 3 minutes: shorten the script")

    print("2/4 scenes")
    segs = []
    for s, t in zip(scenes, tl["scenes"]):
        n, d = s["n"], t["dur"]
        out = os.path.join(work, "seg", f"{n:02d}.mp4"); segs.append(out)
        enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-an", out]
        inp, moving = bg_input(s)
        onscreen = s.get("layout", "F") in ("C", "L") and not s.get("_end")
        bg = bg_filter(d, onscreen or bool(s.get("_end")), moving)
        if s.get("_end"):
            ass = ass_short(os.path.join(work, "seg", f"{n:02d}.ass"), [], 0, END_TOP, "", d, big=END_LINES)
            sh([FF, "-y", "-loglevel", "error", *inp, "-filter_complex", f"{bg};[bg]fade=t=out:st={d - 0.5:.3f}:d=0.5,subtitles={ass}[v]", "-map", "[v]", "-t", f"{d:.3f}", *enc])
            print(f"  {n:02d} end card"); continue
        slot = f"YOUR CLIP {n:02d} · SHOT {s.get('shot', 'A')}" if (a.direction and onscreen) else None
        ass = ass_short(os.path.join(work, "seg", f"{n:02d}.ass"), caps[n], t["pre"], s.get("top", ""), s.get("source", ""), d, slot=slot)
        if onscreen and not a.direction:
            pad = f"tpad=start_duration={t['pre']}:start_mode=clone:stop_duration={t['post'] + 0.5}:stop_mode=clone"
            pv = (f"[1:v]{pad},scale={int(W * 1.15)}:{int(H * 1.15)},format=yuva420p,"
                  f"fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={d - 0.25:.3f}:d=0.25:alpha=1[p]")
            fc = f"{bg};{pv};[bg][p]overlay=-81:0:shortest=0:eof_action=pass[v0];[v0]subtitles={ass}[v]"
            sh([FF, "-y", "-loglevel", "error", *inp, "-i", pres[n], "-filter_complex", fc, "-map", "[v]", "-t", f"{d:.3f}", *enc])
        else:
            sh([FF, "-y", "-loglevel", "error", *inp, "-filter_complex", f"{bg};[bg]subtitles={ass}[v]", "-map", "[v]", "-t", f"{d:.3f}", *enc])
        print(f"  {n:02d} {s['id']} done")
    lst = os.path.join(work, "seg", "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    video = os.path.join(work, "out", "video.mp4")
    sh([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])

    print("3/4 sound")
    r = subprocess.run([sys.executable, os.path.join(HERE, "sound2.py"), tl_path, os.path.join(work, "voice"), os.path.join(work, "out")], capture_output=True, text=True)
    mix = os.path.join(work, "out", "mix.wav")
    if r.returncode or not os.path.exists(mix):
        print("  sound2 failed on this script; voice-only mix at -14 LUFS\n" + r.stderr[-600:])
        parts = sum([["-i", os.path.join(work, "voice", f"{t['n']:02d}.wav")] for t in tl["scenes"]], [])
        delays = ";".join(f"[{i}:a]adelay={int(t['vo_at'] * 1000)}:all=1[a{i}]" for i, t in enumerate(tl["scenes"]))
        sh([FF, "-y", "-loglevel", "error", *parts, "-filter_complex", f"{delays};{''.join(f'[a{i}]' for i in range(len(tl['scenes'])))}amix=inputs={len(tl['scenes'])}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11", mix])

    print("4/4 export")
    ms = re.findall(r"I:\s+(-?[\d.]+) LUFS", subprocess.run([FF, "-nostats", "-i", mix, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr)
    lufs = float(ms[-1]) if ms else -14.0
    gain = max(-6.0, min(6.0, -14.0 - lufs))
    print(f"  mix {lufs:.1f} LUFS -> {gain:+.1f} dB to -14")
    final = os.path.join(work, "out", "short_direction.mp4" if a.direction else "short.mp4")
    sh([FF, "-y", "-loglevel", "error", "-i", video, "-i", mix, "-map", "0:v", "-map", "1:a", "-af", f"volume={gain:.2f}dB", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", final])
    if not a.direction:
        srt, i = [], 1
        for t in tl["scenes"]:
            if caps.get(t["n"]): cues, i = captions.srt_lines(caps[t["n"]], t["vo_at"], i); srt += cues
        open(os.path.join(work, "out", "short.srt"), "w", encoding="utf-8").write("\n".join(srt))
        open(os.path.join(work, "out", "report.md"), "w").write("# Short build report\n\n" + "\n".join(f"- {x}" for x in report) + "\n")
    print("done:", final, f"{os.path.getsize(final) / 1e6:.0f} MB, {dur(final):.1f}s")


if __name__ == "__main__":
    main()
