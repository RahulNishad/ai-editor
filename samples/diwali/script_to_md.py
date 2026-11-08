import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {"diya": "a clay diya, close-up", "lamps_wb": "rows of Diwali lamps at night", "lakshmi": "Lakshmi, Raja Ravi Varma print", "rama_return": "Rama, Sita and Lakshmana return to Ayodhya (17th-century painting)",
         "naraka": "Krishna at Naraka's citadel (1775 folio)", "mahavira": "Mahavira statue, 1470", "golden_temple": "Golden Temple lit for Diwali", "gwalior": "Gurdwara Data Bandi Chhor, Gwalior",
         "tihar": "Kathmandu during Tihar", "london": "Diwali at Trafalgar Square", "sweets": "Diwali sweets", "rangoli": "rangoli", "manuscript": "Sanskrit palm-leaf manuscript", "biruni": "a page in Al-Biruni's hand", "ayodhya_night": "Ram Ki Paidi ghat at night"}
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
    L.append(f"**Face:** {s['expression']}" if s.get("expression") else "")
    seen = []
    for ph in s.get("photos") or []:
        src = ph.get("src")
        if not src: continue
        kind = "AI video clip" if src.startswith("ai/") and os.path.exists(os.path.join(HERE, "assets", src + ".mp4")) else \
               "real footage" if src.startswith("vid/") else "AI still" if src.startswith("ai/") else "real photo"
        k = src.split('/')[-1]; seen.append(f"{NAMES.get(k, k.replace('_', ' '))} ({kind})")
    look = {"map": "3D route map", "map_tabuk": "3D map to Tabuk", "stat": "fact card", "card": "name card", "split": "side-by-side card",
            "screen_split": "check screen, then side-by-side card", "list": "list card", "probe": "investigation timeline", "question": "question card",
            "end": "end card"}.get(s["look"])
    if look: seen.insert(0, look)
    if seen: L.append("**On screen:** " + " → ".join(seen))
    L.append(f"_Direction: {s['direction']}_")
    L.append("")
L += ["---", "Sign-off is the last scene. Sources for every on-screen fact are in `README.md`."]
open(out, "w").write("\n".join(L) + "\n")
print(words, "words,", round(mins, 1), "min")
