"""Render the direction video: the whole film before Rahul records, so he can record to it.

usage:
  .venv/bin/python make_direction.py --work <work dir> [--script script.long.json] [--workers 4] [--scenes 1,2]

Every scene is timed to a Piper scratch voice (hi_IN-rohan-medium, reads the Devanagari line).
Wherever Rahul appears, a "YOUR CLIP nn" slot shows the clip number, shot and face note.
Output: <work>/out/direction.mp4 (1920x1080, 30 fps) and direction_timeline.md.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, wave

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_long as ml

VOICE = os.path.expanduser("~/.cache/piper/hi_IN-rohan-medium.onnx")
PIPER = os.path.join(HERE, ".venv", "bin", "piper")


def scratch_voice(text, dst):
    """Cache by text so unchanged lines are not re-voiced."""
    stamp = dst + ".sha1"
    h = hashlib.sha1(text.encode()).hexdigest()
    if not (os.path.exists(dst) and os.path.exists(stamp) and open(stamp).read() == h):
        subprocess.run([PIPER, "-m", VOICE, "-f", dst, "--sentence-silence", "0.25"], input=text.encode(), check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        open(stamp, "w").write(h)
    with wave.open(dst) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default=os.path.join(HERE, "script.long.json"))
    ap.add_argument("--work", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--scenes", default="")
    a = ap.parse_args()
    if not os.path.exists(VOICE):
        sys.exit(f"missing scratch voice {VOICE}; download hi_IN-rohan-medium.onnx and .onnx.json from rhasspy/piper-voices")
    work = os.path.abspath(a.work)
    for d in ("voice", "out"):
        os.makedirs(os.path.join(work, d), exist_ok=True)
    scenes = json.load(open(a.script))["scenes"]
    if a.scenes:
        keep = {int(x) for x in a.scenes.split(",")}
        scenes = [s for s in scenes if s["n"] in keep]

    print("1/4 scratch voice")
    durs = {}
    for s in scenes:
        durs[s["n"]] = scratch_voice(s.get("text_dev") or s["text"], os.path.join(work, "voice", f"{s['n']:02d}.wav"))
        print(f"  {s['n']:02d} {s['id']}: {durs[s['n']]:.1f}s")

    print("2/4 timeline")
    tl = ml.build_timeline(scenes, durs)
    tl["preview"] = True
    for s, t in zip(scenes, tl["scenes"]):
        t["shot"], t["expression"] = s.get("shot", "A"), s.get("expression", "")
    tl_name = "timeline.direction.json"
    json.dump(tl, open(os.path.join(HERE, tl_name), "w"), indent=1, ensure_ascii=False)

    print(f"3/4 rendering {tl['total']:.0f}s of graphics")
    fd = "frames_direction"
    if os.path.isdir(os.path.join(HERE, fd)):
        shutil.rmtree(os.path.join(HERE, fd))
    os.makedirs(os.path.join(HERE, fd))
    ml.render_frames(work, tl_name, fd, a.workers)

    print("4/4 sound and export")
    video = os.path.join(work, "out", "video.mp4")
    ml.sh(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(ml.FPS), "-i", os.path.join(HERE, fd, "%05d.jpg"),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", video])
    ml.sh([sys.executable, os.path.join(HERE, "sound2.py"), os.path.join(HERE, tl_name), os.path.join(work, "voice"), os.path.join(work, "out")])
    final = os.path.join(work, "out", "direction.mp4")
    ml.sh(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-i", os.path.join(work, "out", "mix.wav"), "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "-shortest", final])

    rows = ["| Clip | Starts | Length | Where you are | Shot |", "| --- | --- | --- | --- | --- |"]
    where = {"C": "On screen, centred", "L": "Right-hand card", "F": "Voice only"}
    for s in tl["scenes"]:
        m, sec = divmod(int(s["start"]), 60)
        rows.append(f"| {s['n']:02d}.mp4 | {m}:{sec:02d} | {s['dur']:.0f}s | {where[s['layout']]} | {s['shot']} |")
    open(os.path.join(work, "out", "direction_timeline.md"), "w").write("\n".join(rows) + "\n")
    print("done:", final, f"{os.path.getsize(final) / 1e6:.0f} MB, {tl['total']:.0f}s")


if __name__ == "__main__":
    main()
