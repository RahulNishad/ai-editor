import json, subprocess, sys, numpy as np
from scipy.signal import butter, sosfilt, sosfiltfilt
P = sys.argv[1]; SR = 48000
tl = json.load(open(f"{P}/timeline.json")); T = tl["total"]; N = int(T*SR)+SR
rng = np.random.default_rng(7)
def load(p):
    raw = subprocess.run(["ffmpeg","-loglevel","error","-i",p,"-f","s16le","-ac","1","-ar",str(SR),"-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768
def lp(x,f,o=2): return sosfilt(butter(o,f,'low',fs=SR,output='sos'),x)
def hp(x,f,o=2): return sosfilt(butter(o,f,'high',fs=SR,output='sos'),x)
def bp(x,a,b,o=2): return sosfilt(butter(o,[a,b],'band',fs=SR,output='sos'),x)
t = np.arange(N)/SR
sc = {s["id"]: s for s in tl["scenes"]}
def at(sid, frac=0.0, off=0.0): s=sc[sid]; return s["start"]+s["dur"]*frac+off

# ---- voice ----
voice = np.zeros(N, np.float32)
for s in tl["scenes"]:
    v = load(f"{P}/vo/{tl['voice']}_{s['id']}.wav"); i=int(s["vo_at"]*SR); voice[i:i+len(v)] += v[:N-i]
voice = hp(voice, 80)
# voice envelope for ducking
env = sosfiltfilt(butter(2, 3, 'low', fs=SR, output='sos'), np.abs(voice))
env = np.clip(env/ (np.percentile(env[env>1e-4],90)+1e-9), 0, 1)

# ---- music bed: dark D-minor drone ----
def drone(freqs, det=0.12):
    y = np.zeros(N, np.float32)
    for f in freqs:
        for d in (-det, 0, det):
            ph = rng.uniform(0, 2*np.pi)
            for h, a in ((1,1),(2,.35),(3,.15),(4,.06)):
                y += a*np.sin(2*np.pi*(f+d)*h*t + ph*h)
    return y/len(freqs)
bed = drone([73.42, 110.0, 146.83, 174.61])*0.5
bed *= 0.75 + 0.25*np.sin(2*np.pi*t/9.0)
wind = lp(hp(rng.standard_normal(N).astype(np.float32), 200), 900)*0.25
wind *= 0.6+0.4*np.sin(2*np.pi*t/13+1)
bed = lp(bed + wind, 1800)
# arrangement gain
g = np.ones(N, np.float32)*0.5
def ramp(a,b,v0,v1):
    i0,i1=int(a*SR),int(b*SR); g[i0:i1]=np.linspace(v0,v1,max(i1-i0,1))
ramp(0, at("s01_hook",1), 0.25, 0.35)                       # quieter during hook
ramp(at("s10_question"), at("s10_question",0,0.95), 0.0, 0.0)  # silence before the final question
ramp(at("s10_question",0,0.95), at("s10_question",0,2.5), 0.0, 0.35)
ramp(at("s11_end",1,-1.6), T+1, 0.45, 0.0)
music = bed*g
# low pulse (heartbeat) from title through plunge
pulse = np.zeros(N, np.float32)
k = np.arange(int(0.35*SR))/SR; thump = np.sin(2*np.pi*48*k*(1-0.4*k))*np.exp(-k*14)
p0, p1 = at("s02_title",0,2.0), at("s05_plunge",1)
bt = p0
while bt < p1:
    for off, a in ((0,1),(0.22,.6)):
        i=int((bt+off)*SR); pulse[i:i+len(thump)] += a*thump[:N-i]
    bt += 1.0 if bt < at("s04_attack") else 0.8
music += pulse*0.55
# ducking under voice
duck = 1 - 0.62*env
music *= duck

# ---- SFX ----
sfx = np.zeros(N, np.float32)
def place(sig, when, gain=1.0):
    i=int(when*SR); n=min(len(sig),N-i); sfx[i:i+n]+=sig[:n]*gain
def whoosh(d=0.7):
    n=int(d*SR); x=rng.standard_normal(n).astype(np.float32); out=np.zeros(n,np.float32)
    seg=256
    for j in range(0,n,seg):
        u=j/n; f=300+3800*np.sin(np.pi*u)**2
        out[j:j+seg]=bp(x[j:j+seg+0],max(80,f*.6),min(f*1.4,20000))[:len(out[j:j+seg])]
    e=np.sin(np.pi*np.linspace(0,1,n))**2
    return lp(out*e,6000)
def boom(d=2.5):
    k=np.arange(int(d*SR))/SR
    s=np.sin(2*np.pi*(38+30*np.exp(-k*6))*k)*np.exp(-k*1.6)
    s+=lp(rng.standard_normal(len(k)).astype(np.float32),180)*np.exp(-k*4)*0.6
    return s
def riser(d):
    n=int(d*SR); k=np.arange(n)/SR; x=hp(rng.standard_normal(n).astype(np.float32),400)
    tone=np.sin(2*np.pi*(110*np.exp(k/d*np.log(4)))*k)*0.4
    u=k/d; return ((lp(x,1500)*(1-u)+lp(x,7500)*u)*0.5+tone)*u**2.2
def beep_pair():
    k=np.arange(int(0.16*SR))/SR; a=np.sin(2*np.pi*1150*k)*np.minimum(1,np.minimum(k,0.16-k)*80)
    b=np.sin(2*np.pi*860*k)*np.minimum(1,np.minimum(k,0.16-k)*80)
    return np.concatenate([a,np.zeros(int(.06*SR)),b])
for s in tl["scenes"][1:]:
    place(whoosh(), s["start"]-0.35, 0.5)
place(boom(), at("s02_title",0,1.2), 0.9)
place(boom(), at("s04_attack",0.5), 0.8)
place(boom(), at("s05_plunge",0.08), 1.0)
place(boom(), at("s09_probe",0.22), 0.8)
place(riser(4.0), at("s10_question",0,-4.0+0.0), 0.5)
# cockpit master caution beeps
bp_sig = beep_pair()
def beeps(a,b,every=1.1,gain=.12):
    x=a
    while x<b: place(bp_sig,x,gain); x+=every
beeps(at("s01_hook",.55), at("s01_hook",1,-.2))
beeps(at("s04_attack"), at("s04_attack",1,-.2), gain=.07)
beeps(at("s06_door"), at("s06_door",.3), gain=.06)
# plane wind roar during dive
n=int(sc["s05_plunge"]["dur"]*SR); roar=lp(rng.standard_normal(n).astype(np.float32),700)*np.sin(np.pi*np.linspace(0,1,n))**.7
place(roar, at("s05_plunge"), 0.35)

# ---- write stems ----
def w(name,x):
    x=np.clip(x,-1,1); s=(x*32767).astype(np.int16).tobytes()
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","s16le","-ar",str(SR),"-ac","1","-i","-",f"{P}/audio/{name}.wav"],input=s,check=True)
w("voice", voice*0.9); w("music", music*0.38); w("sfx", sfx*0.35)
print("stems written, length", round(N/SR,1), "s")
