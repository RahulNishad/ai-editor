"""Generic sound design driven by the timeline's looks.

usage: python sound2.py <timeline.json> <voice_dir with NN.wav> <out_dir>
Writes voice_n.wav, music.wav, sfx.wav and mix.wav (-14 LUFS target) into out_dir.
Rules follow the channel recipe: dark bed ducked under voice, quieter hook, pulse from the
title to the climax, whooshes on scene changes, booms on reveals, cockpit caution beeps,
a riser into the final question and about one second of music silence before it.
"""
import json, os, subprocess, sys
import numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt

SR = 48000
tl_path, voice_dir, out = sys.argv[1:4]
tl = json.load(open(tl_path)); T = tl["total"]; N = int(T * SR) + SR
rng = np.random.default_rng(7)
t = np.arange(N) / SR
S = tl["scenes"]


def load(p):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def filt(x, f, kind, o=2): return sosfilt(butter(o, f, kind, fs=SR, output="sos"), x)
def first(look): return next((s for s in S if s["look"] == look), None)
def at(s, frac=0.0, off=0.0): return s["start"] + s["dur"] * frac + off


# ---- voice ----
voice = np.zeros(N, np.float32)
for s in S:
    v = load(os.path.join(voice_dir, f"{s['n']:02d}.wav")); i = int(s["vo_at"] * SR)
    voice[i:i + len(v)] += v[:N - i]
voice = filt(voice, 80, "high")
env = sosfiltfilt(butter(2, 3, "low", fs=SR, output="sos"), np.abs(voice))
env = np.clip(env / (np.percentile(env[env > 1e-4], 90) + 1e-9), 0, 1)

# ---- bed ----
bed = np.zeros(N, np.float32)
for f in (73.42, 110.0, 146.83, 174.61):
    for d in (-0.12, 0, 0.12):
        ph = rng.uniform(0, 2 * np.pi)
        for h, a in ((1, 1), (2, .35), (3, .15), (4, .06)):
            bed += a * np.sin(2 * np.pi * (f + d) * h * t + ph * h)
bed = bed / 4 * 0.5 * (0.75 + 0.25 * np.sin(2 * np.pi * t / 9.0))
wind = filt(filt(rng.standard_normal(N).astype(np.float32), 200, "high"), 900, "low") * 0.25 * (0.6 + 0.4 * np.sin(2 * np.pi * t / 13 + 1))
bed = filt(bed + wind, 1800, "low")
g = np.ones(N, np.float32) * 0.5


def ramp(a, b, v0, v1):
    i0, i1 = int(max(a, 0) * SR), int(min(b, T + 1) * SR); g[i0:i1] = np.linspace(v0, v1, max(i1 - i0, 1))


title, dive, q, end = first("plane_cruise"), first("plane_dive"), first("question"), first("end")
if title: ramp(0, title["start"], 0.25, 0.35)
if q:
    ramp(q["start"], q["start"] + 0.95, 0, 0); ramp(q["start"] + 0.95, q["start"] + 2.5, 0, 0.35)
if end: ramp(at(end, 1, -1.6), T + 1, 0.45, 0)
music = bed * g
if title and dive:
    k = np.arange(int(0.35 * SR)) / SR; thump = np.sin(2 * np.pi * 48 * k * (1 - 0.4 * k)) * np.exp(-k * 14)
    bt = title["start"] + 2.0
    while bt < at(dive, 1):
        for off, a in ((0, 1), (0.22, .6)):
            i = int((bt + off) * SR); music[i:i + len(thump)] += 0.55 * a * thump[:N - i]
        bt += 0.85
music *= 1 - 0.62 * env

# ---- sfx ----
sfx = np.zeros(N, np.float32)


def place(sig, when, gain=1.0):
    i = int(max(when, 0) * SR); n = min(len(sig), N - i); sfx[i:i + n] += sig[:n] * gain


def whoosh(d=0.7):
    n = int(d * SR); x = rng.standard_normal(n).astype(np.float32); o = np.zeros(n, np.float32)
    for j in range(0, n, 256):
        f = 300 + 3800 * np.sin(np.pi * j / n) ** 2
        o[j:j + 256] = filt(x[j:j + 256], [max(80, f * .6), min(f * 1.4, 20000)], "band")[:len(o[j:j + 256])]
    return filt(o * np.sin(np.pi * np.linspace(0, 1, n)) ** 2, 6000, "low")


def boom(d=2.5):
    k = np.arange(int(d * SR)) / SR
    return np.sin(2 * np.pi * (38 + 30 * np.exp(-k * 6)) * k) * np.exp(-k * 1.6) + filt(rng.standard_normal(len(k)).astype(np.float32), 180, "low") * np.exp(-k * 4) * 0.6


def riser(d):
    n = int(d * SR); k = np.arange(n) / SR; u = k / d; x = filt(rng.standard_normal(n).astype(np.float32), 400, "high")
    return ((filt(x, 1500, "low") * (1 - u) + filt(x, 7500, "low") * u) * 0.5 + np.sin(2 * np.pi * (110 * np.exp(u * np.log(4))) * k) * 0.4) * u ** 2.2


kk = np.arange(int(0.16 * SR)) / SR; env16 = np.minimum(1, np.minimum(kk, 0.16 - kk) * 80)
beep = np.concatenate([np.sin(2 * np.pi * 1150 * kk) * env16, np.zeros(int(.06 * SR)), np.sin(2 * np.pi * 860 * kk) * env16])


def beeps(a, b, gain):
    x = a
    while x < b: place(beep, x, gain); x += 1.1


for s in S[1:]:
    place(whoosh(), s["start"] - 0.35, 0.5)
for s in S:
    lk, p = s["look"], s.get("params") or {}
    if lk == "plane_cruise": place(boom(), at(s, 0, 1.2), 0.9)
    if lk == "cockpit_alarm": place(boom(), at(s, 0.5), 0.8); beeps(s["start"], at(s, 1, -.2), .07)
    if lk == "plane_dive":
        place(boom(), at(s, 0.08), 1.0)
        n = int(s["dur"] * SR); place(filt(rng.standard_normal(n).astype(np.float32), 700, "low") * np.sin(np.pi * np.linspace(0, 1, n)) ** .7, s["start"], 0.35)
    if lk == "cockpit": beeps(at(s, .55), at(s, 1, -.2), .12)
    if lk == "cockpit_door": beeps(s["start"], at(s, .3), .06)
    if "CLAIM" in (p.get("tag") or ""): place(boom(), at(s, 0.08), 0.7)
if q: place(riser(4.0), q["start"] - 4.0, 0.5)


def w(name, x):
    x = np.clip(x, -1, 1)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", os.path.join(out, name)],
                   input=(x * 32767).astype(np.int16).tobytes(), check=True)


w("voice.wav", voice * 0.9); w("music.wav", music * 0.38); w("sfx.wav", sfx * 0.35)
run = lambda *a: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
run("-i", os.path.join(out, "voice.wav"), "-af", "highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9",
    "-ar", str(SR), os.path.join(out, "voice_n.wav"))
run("-i", os.path.join(out, "voice_n.wav"), "-i", os.path.join(out, "music.wav"), "-i", os.path.join(out, "sfx.wav"),
    "-filter_complex", "[0][1][2]amix=inputs=3:normalize=0,alimiter=limit=0.89", "-ar", str(SR), "-ac", "2", os.path.join(out, "mix.wav"))
print("mix written")
