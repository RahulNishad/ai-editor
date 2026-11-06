"""Resolve AI reconstruction sources: Flow MP4 -> frame sequence, still JPG, or drop (fall back to real photo)."""
import os, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30

def _frames(key):
    mp4 = os.path.join(HERE, "assets", "ai", key + ".mp4"); d = os.path.join(HERE, "assets", "ai", key)
    if not os.path.exists(mp4): return 0
    if not os.path.isdir(d) or os.path.getmtime(d) < os.path.getmtime(mp4):
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(os.path.join(d, "*.jpg")): os.remove(f)
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", mp4, "-vf",
                        f"fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080", "-q:v", "3",
                        os.path.join(d, "%05d.jpg")], check=True)
    return len(glob.glob(os.path.join(d, "*.jpg")))

def _still(key):
    """Accept a Flow download as .jpg/.jpeg/.png/.webp and conform it to a 1920x1080 jpg."""
    base = os.path.join(HERE, "assets", "ai", key); jpg = base + ".jpg"
    for ext in (".png", ".webp", ".jpeg", ".JPG", ".PNG", ".jpg"):
        src = base + ext
        if os.path.exists(src) and (ext != ".jpg" or not os.path.exists(base + ".ok")):
            tmp = base + ".tmp.jpg"
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", src, "-vf",
                            "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080", "-q:v", "2", tmp], check=True)
            os.replace(tmp, jpg); open(base + ".ok", "w").close()
            if ext != ".jpg": os.remove(src)
            return True
    return os.path.exists(jpg)

def resolve(photos):
    out = []
    for p in photos or []:
        src = p.get("src")
        if src and src.startswith("ai/"):
            key = src[3:]; n = _frames(key)
            if n: out.append({**p, "video": n}); continue
            if _still(key): out.append(p); continue
            continue  # not generated yet: drop, earlier real photo stays on screen
        out.append(p)
    if out and out[0].get("at", 0) > 0 and not any(x.get("src") for x in out): return []
    return out
