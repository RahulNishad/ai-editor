"""Generate photoreal reconstruction stills locally with FLUX.1-schnell (Apache-2.0) via stable-diffusion.cpp.
usage: /home/user/sdenv/bin/python gen_ai.py [shot ...]      (default: all missing shots)
Writes assets/ai/<shot>.jpg at 1920x1080 and records them in assets/photos/credits.json as AI reconstructions."""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); M = "/home/user/models"
P = json.load(open(os.path.join(HERE, "assets/ai/prompts.json")))
want = sys.argv[1:] or [k for k in P["shots"] if not os.path.exists(os.path.join(HERE, "assets/ai", k + ".jpg"))]
from stable_diffusion_cpp import StableDiffusion
sd = StableDiffusion(diffusion_model_path=f"{M}/flux1-schnell-Q4_K_S.gguf", clip_l_path=f"{M}/clip_l.safetensors",
                     t5xxl_path=f"{M}/t5-v1_1-xxl-encoder-Q4_K_M.gguf", vae_path=f"{M}/ae.safetensors",
                     vae_decode_only=True, n_threads=os.cpu_count(), verbose=False)
cp = os.path.join(HERE, "assets/photos/credits.json"); cr = json.load(open(cp))
for k in want:
    s = P["shots"][k]; t0 = time.time()
    gen = getattr(sd, "generate_image", None) or sd.txt_to_img
    imgs = gen(prompt=f"{s['prompt']}, {P['style']}", width=1024, height=576, sample_steps=4, cfg_scale=1.0, seed=s["seed"])
    raw = os.path.join(HERE, "assets/ai", k + ".png"); imgs[0].save(raw)
    out = os.path.join(HERE, "assets/ai", k + ".jpg")
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", raw, "-vf", "scale=1920:1080:flags=lanczos,unsharp=5:5:0.6", "-q:v", "3", out], check=True)
    os.remove(raw)
    cr["ai/" + k] = {"title": k, "page": "", "license": "AI RECONSTRUCTION", "artist": "FLUX.1-schnell", "date": time.strftime("%Y-%m-%d"), "ai": True}
    json.dump(cr, open(cp, "w"), indent=1, ensure_ascii=False)
    print(f"{k}: {time.time() - t0:.0f}s", flush=True)
