"""Render one still per scene with estimated timings and build a labelled storyboard sheet.
usage: python storyboard.py [script.long.json]   (needs node + npm install)"""
import importlib.util, json, os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
spec = importlib.util.spec_from_file_location("ml", "make_long.py"); ml = importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
sc = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "script.long.json"))["scenes"]
tl = ml.build_timeline(sc, {s["n"]: len(s["text"].split()) / 140 * 60 for s in sc})
json.dump(tl, open("timeline.preview.json", "w"), indent=1)
frames = [int((s["start"] + s["dur"] * 0.62) * 30) for s in tl["scenes"]]
subprocess.run(["node", "stills.js", "0", "1"], check=True, env=dict(os.environ, TL="timeline.preview.json", OUT="frames_prev", LIST=",".join(map(str, frames))))
font = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
os.makedirs("sb", exist_ok=True); tiles = []
for s, f in zip(tl["scenes"], frames):
    vf = []
    box = {"L": (1268, 42, 568, 996), "C": (656, 0, 608, 1080)}.get(s["layout"])
    if box:
        x, y, w, h = box
        vf.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0xffffff@0.18:t=fill,drawbox=x={x}:y={y}:w={w}:h={h}:color=0xe0312e:t=6,"
                  f"drawtext=fontfile={font}:text='YOU':fontsize=90:fontcolor=white:x={x}+({w}-tw)/2:y=500")
    lab = {"C": "YOU CENTRED", "L": "YOU RIGHT", "F": "VOICE ONLY"}[s["layout"]]
    vf.append(f"drawbox=x=0:y=0:w=1920:h=120:color=black@0.75:t=fill,drawtext=fontfile={font}:text='{s['n']:02d}.mp4  ·  {lab}':fontsize=70:fontcolor=white:x=40:y=28")
    out = f"sb/{s['n']:02d}.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"frames_prev/{f:05d}.jpg", "-vf", ",".join(vf) + ",scale=640:360", out], check=True); tiles.append(out)
while len(tiles) % 4: tiles.append("sb/blank.jpg") if os.path.exists("sb/blank.jpg") else subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i","color=c=black:s=640x360","-frames:v","1","sb/blank.jpg"],check=True) or tiles.append("sb/blank.jpg")
rows = []
for r in range(0, len(tiles), 4):
    o = f"sb/row{r // 4}.jpg"; subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *sum([["-i", t] for t in tiles[r:r + 4]], []), "-filter_complex", "hstack=inputs=4", o], check=True); rows.append(o)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *sum([["-i", t] for t in rows], []), "-filter_complex", f"vstack=inputs={len(rows)}", "STORYBOARD.jpg"], check=True)
print("STORYBOARD.jpg:", len(sc), "scenes, about", round(tl["total"] / 60, 1), "min")
