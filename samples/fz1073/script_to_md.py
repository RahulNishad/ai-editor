import json, sys
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
LAY = {"C": "You on screen, centred", "L": "You on the right, graphic on the left", "F": "Full-screen graphic, only your voice"}
words = sum(len(s["text"].split()) for s in d["scenes"])
mins = words / 140
L = [f"# {d['title']}", "", f"_{d['subtitle']}_", "",
     f"**{len(d['scenes'])} scenes · {words} words · about {mins:.0f} minutes at 140 words per minute**", "",
     "## How to record", ""]
for k, v in d["recording"].items():
    L.append(f"- **{k.capitalize()}:** {v}")
L += ["- **Every scene needs a clip**, even full-screen ones, because your voice runs under the graphic. For full-screen scenes the camera framing does not matter.",
      "- **Upload** the clips in one folder or zip. Keep your original files; nothing is overwritten.", "", "## Script", ""]
chap = None
for s in d["scenes"]:
    if s.get("chapter") and s["chapter"] != chap:
        chap = s["chapter"]; L += [f"### {chap}", ""]
    L.append(f"**{s['n']:02d}.mp4** · Shot {s['shot']} · {LAY[s['layout']]}")
    L.append(f"> {s['text']}")
    if s.get("text_dev"):
        L.append(">"); L.append(f"> {s['text_dev']}")
    L.append(f"_Direction: {s['direction']}_")
    L.append("")
L += ["---", "Sign-off is scene 23. Sources for every on-screen fact are in `README.md`."]
open(out, "w").write("\n".join(L) + "\n")
print(words, "words,", round(mins, 1), "min")
