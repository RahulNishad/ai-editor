"""Key Rahul's green-cloth takes without a halo: clean-plate chroma distance, not a global colour.

usage: python key_presenter.py <in.mp4 (SDR, 1080x1920)> <out.mov (ProRes 4444 with alpha)> [--bg 0x14161b] [--preview out.jpg]

Recipe (from the production skill):
1. Clean plate per frame: the cloth colour sampled from the frame border (left, right and top strips) and
   interpolated across the frame, so uneven lighting does not need a wide key.
2. Alpha = distance from the clean plate in YCrCb, chroma weighted fully and luma x0.25, ramped 9 -> 26.
3. Small erosion plus a blur on the matte; edge colour from just inside the edge; green spill clamped.
"""
import argparse, subprocess, sys
import numpy as np
from scipy import ndimage

W, H = 1080, 1920
FF = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
STRIP = 70       # border strip width used as the cloth sample
RAMP = (9.0, 26.0)


def is_green(ycc):
    """Lime cloth measured on the SDR takes: Cb 93-97, Cr 128-132. Skin: Cr 141-163. Shirt: Cb 141. So cloth = low Cb and Cr near neutral."""
    return (ycc[..., 2] < 112) & (ycc[..., 1] < 138)


def _fill_rows(samples, valid):
    """Rows whose border strip is not cloth (his arms reach the edge) take the nearest valid row above, else below."""
    out = samples.copy(); last = None
    for i in range(len(out)):
        if valid[i]: last = out[i]
        elif last is not None: out[i] = last
    nxt = None
    for i in range(len(out) - 1, -1, -1):
        if valid[i]: nxt = out[i]
        elif nxt is not None and not valid[:i + 1].any(): out[i] = nxt
    return out


def clean_plate(ycc):
    """Interpolate trusted border samples across the frame: per row, blend the left and right strip medians; above
    the head, blend with the top strip."""
    L, R, T = ycc[:, :STRIP], ycc[:, -STRIP:], ycc[:STRIP]
    left = _fill_rows(np.median(L, axis=1), is_green(L).mean(axis=1) > 0.6)
    right = _fill_rows(np.median(R, axis=1), is_green(R).mean(axis=1) > 0.6)
    top = np.median(T, axis=0)
    x = np.linspace(0, 1, W)[None, :, None]
    plate = left[:, None, :] * (1 - x) + right[:, None, :] * x
    y = np.linspace(0, 1, H)[:, None, None]
    wtop = np.clip(1 - y * 4, 0, 1)
    plate = plate * (1 - wtop) + top[None, :, :] * wtop
    return ndimage.uniform_filter(plate, size=(61, 61, 1), mode="nearest")


def matte(ycc, plate):
    d = ycc - plate
    dist = np.sqrt(0.25 * d[..., 0] ** 2 + d[..., 1] ** 2 + d[..., 2] ** 2)
    a = np.clip((dist - RAMP[0]) / (RAMP[1] - RAMP[0]), 0, 1)
    strong = (ycc[..., 2] < 105) & (ycc[..., 1] < 136)      # unmistakably cloth, whatever the plate says (sunlit folds)
    a[strong] = 0.0
    core = ndimage.binary_erosion(a > 0.95, iterations=3)
    a = ndimage.gaussian_filter(a, 1.2)
    a[core] = 1.0
    a[ndimage.binary_erosion(strong, iterations=2)] = 0.0
    return a


def despill(rgb, a):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    lim = np.maximum(r, b) * 1.05 + 6
    spill = np.clip(g - lim, 0, None)
    g2 = g - spill
    out = np.stack([r + spill * 0.35, g2, b + spill * 0.35], axis=-1)
    return np.clip(out, 0, 255)


def ycc_from_rgb(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cr = (r - y) * 0.713 + 128
    cb = (b - y) * 0.564 + 128
    return np.stack([y, cr, cb], axis=-1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--preview", default="")
    ap.add_argument("--frames", type=int, default=0, help="stop after n frames (tests)")
    a = ap.parse_args()
    dec = subprocess.Popen([FF, "-loglevel", "error", "-i", a.src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-i", a.src, "-map", "0:v", "-map", "1:a?", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
                            "-c:a", "copy", a.dst], stdin=subprocess.PIPE)
    n = 0
    while True:
        buf = dec.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        ycc = ycc_from_rgb(rgb)
        al = matte(ycc, clean_plate(ycc))
        rgb2 = despill(rgb, al)
        out = np.dstack([rgb2, al * 255]).astype(np.uint8)
        enc.stdin.write(out.tobytes())
        if a.preview and n == 0:
            bg = np.full_like(rgb2, (20, 22, 27), dtype=np.float32)
            comp = rgb2 * al[..., None] + bg * (1 - al[..., None])
            subprocess.run([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-i", "-", "-frames:v", "1", a.preview],
                           input=comp.astype(np.uint8).tobytes())
        n += 1
        if a.frames and n >= a.frames: break
        if n % 300 == 0: print(f"  keyed {n} frames", flush=True)
    enc.stdin.close(); dec.stdout.close(); dec.wait(); enc.wait()
    print(f"keyed {n} frames -> {a.dst}")


if __name__ == "__main__":
    main()
