"""Search Wikimedia Commons and download licensed photos with attribution.
usage: python commons.py search "<query>" [limit]
       python commons.py get "<File:Title.jpg>" <key>     -> assets/photos/<key>.jpg + credits.json
       python commons.py getvid "<File:Title.webm>" <key> <start s> <seconds>  -> assets/vid/<key>.mp4 (1080p) + credits.json"""
import json, os, re, sys, urllib.parse, urllib.request, urllib.error, html
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "RahulAIVideoStudio/0.1 (local documentary editor; contact via project repo)"}
HERE = os.path.dirname(os.path.abspath(__file__))
OK = re.compile(r"^(CC0|CC BY(-SA)? [0-9.]+|Public domain|PD.*|CC BY [0-9.]+.*)$", re.I)

def api(**p):
    import time
    p.update(format="json", formatversion=2)
    for i in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(2 ** i)
    raise SystemExit("rate limited")

def clean(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def info(titles, thumb=True):
    d = api(action="query", titles="|".join(titles), prop="imageinfo", iiprop="url|size|extmetadata|mime", **({"iiurlwidth": 1920} if thumb else {}))
    out = []
    for pg in d["query"]["pages"]:
        if "imageinfo" not in pg: continue
        ii = pg["imageinfo"][0]; m = ii.get("extmetadata", {})
        out.append({"title": pg["title"], "w": ii["width"], "h": ii["height"], "mime": ii["mime"], "thumb": ii.get("thumburl", ii["url"]), "orig": ii["url"],
                    "page": ii["descriptionurl"], "license": clean(m.get("LicenseShortName", {}).get("value")),
                    "artist": clean(m.get("Artist", {}).get("value")), "desc": clean(m.get("ImageDescription", {}).get("value"))[:160],
                    "date": clean(m.get("DateTimeOriginal", {}).get("value"))[:20]})
    return out

if sys.argv[1] == "search":
    lim = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    d = api(action="query", list="search", srsearch=sys.argv[2] + " filetype:bitmap", srnamespace=6, srlimit=lim)
    titles = [x["title"] for x in d["query"]["search"]]
    for r in (info(titles) if titles else []):
        if r["w"] < 1600 or not r["mime"].startswith("image/"): continue
        flag = "" if OK.match(r["license"]) else "  [CHECK LICENSE]"
        print(f"{r['title']} | {r['w']}x{r['h']} | {r['license']} | {r['artist'][:40]} | {r['date']}{flag}\n    {r['desc'][:130]}")
elif sys.argv[1] == "get":
    r = info([sys.argv[2]])[0]; key = sys.argv[3]
    if not OK.match(r["license"]): sys.exit(f"license not allowed: {r['license']}")
    dst = os.path.join(HERE, "assets", "photos", key + ".jpg"); tmp = dst + ".src" + os.path.splitext(urllib.parse.urlparse(r["orig"]).path)[1].lower()
    import subprocess
    import time
    url = r["orig"].split("?")[0]
    tw = 1920 if r["w"] > 1920 else 1280 if r["w"] > 1280 else None
    if tw:  # Wikimedia asks automated clients to use standard thumbnail widths, not originals
        base = url.rsplit("/", 1)[1]
        url = url.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/") + f"/{tw}px-{base}"
    subprocess.run(["curl", "-sS", "-f", "-A", UA["User-Agent"], "--retry", "3", "--retry-delay", "20", "-o", tmp, url], check=True)
    time.sleep(12)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", tmp, "-vf", "scale='min(3200,iw)':-2", "-q:v", "3", dst], check=True); os.remove(tmp)
    cp = os.path.join(HERE, "assets", "photos", "credits.json")
    cr = json.load(open(cp)) if os.path.exists(cp) else {}
    cr[key] = {k: r[k] for k in ("title", "page", "license", "artist", "date")}
    json.dump(cr, open(cp, "w"), indent=1, ensure_ascii=False)
    print("saved", dst, r["license"], "·", r["artist"])
elif sys.argv[1] == "getvid":
    import subprocess
    r = info([sys.argv[2]], thumb=False)[0]; key, ss, dur = sys.argv[3], sys.argv[4], sys.argv[5]
    if not OK.match(r["license"]): sys.exit(f"license not allowed: {r['license']}")
    os.makedirs(os.path.join(HERE, "assets", "vid"), exist_ok=True)
    dst = os.path.join(HERE, "assets", "vid", key + ".mp4")
    tmp = dst + ".src.webm"; import time
    subprocess.run(["curl", "-sS", "-f", "-L", "-A", UA["User-Agent"], "--retry", "5", "--retry-delay", "30", "--retry-all-errors", "-o", tmp, r["orig"].split("?")[0]], check=True)
    time.sleep(10)
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", ss, "-t", dur, "-i", tmp, "-an",
                    "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", dst], check=True)
    os.remove(tmp)
    if os.path.getsize(dst) < 100000: sys.exit(f"clip came out empty: {dst}")
    cp = os.path.join(HERE, "assets", "photos", "credits.json")
    cr = json.load(open(cp)) if os.path.exists(cp) else {}
    cr["vid/" + key] = {**{k: r[k] for k in ("title", "page", "license", "artist", "date")}, "video": True}
    json.dump(cr, open(cp, "w"), indent=1, ensure_ascii=False)
    print("saved", dst, r["license"], "·", r["artist"])
