import json, sys, wave
P = sys.argv[1]; voice = sys.argv[2]
d = json.load(open(f"{P}/script.json"))
PRE = {"s02_title": 1.2, "s10_question": 1.0}
POST = {"s11_end": 1.8, "s05_plunge": 0.8, "s04_attack": 0.6}
SOURCES = {
 "s02_title": "PEOPLE ON BOARD: REPORTS VARY, 172–182 · AIRCRAFT: FLIGHTRADAR24",
 "s03_route": "TIMES: FLIGHTRADAR24 (TAKE-OFF 03:05, INCIDENT 05:21 UTC) · ROUTE ILLUSTRATIVE",
 "s04_attack": "SOURCE: UAE ATTORNEY GENERAL VIA WAM, 9 OCT 2026 · WEAPON ACCOUNTS VARY",
 "s05_plunge": "SOURCE: FLIGHTRADAR24 ADS-B DATA AS REPORTED · CHART SIMPLIFIED",
 "s08_landing": "SOURCE: FLYDUBAI STATEMENT; GULF NEWS",
 "s09_probe": "SOURCES: WAM / HAARETZ (9 OCT) · NIA VIA BUSINESS TODAY (10 OCT)",
}
t = 0.0; out = []
for s in d["scenes"]:
    with wave.open(f"{P}/vo/{voice}_{s['id']}.wav") as w: vd = w.getnframes()/w.getframerate()
    pre = PRE.get(s["id"], 0.35); post = POST.get(s["id"], 0.5)
    dur = pre + vd + post
    out.append({**{k: s[k] for k in ("id","look","chapter","phrases")}, "start": round(t,3), "dur": round(dur,3), "vo_at": round(t+pre,3), "vo_dur": round(vd,3), "source": SOURCES.get(s["id"], "")})
    t += dur
json.dump({"fps": d["fps"], "voice": voice, "total": round(t,3), "scenes": out}, open(f"{P}/timeline.json","w"), indent=1)
print(voice, "total", round(t,1), "s,", int(t*d["fps"]), "frames")
