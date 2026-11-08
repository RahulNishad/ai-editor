# Handoff — FZ1073 on Rahul's Mac

Date: 8 Nov 2026. Branch: `claude/awesome-goldberg-6n0u1a` on `RahulNishad/ai-editor`.

## 1. Where things stand

The FZ1073 long video is **ready for Rahul's recording**. The Mac setup is done, the direction video is rendered, and every visual is reviewed and approved. Only Rahul's 24 clips are missing.

| Piece | Status | Where |
| --- | --- | --- |
| Research and fact table | Done; sources still to open (see §6) | `samples/fz1073/README.md` |
| Recording script, 24 scenes (teaser first), Hinglish + Devanagari, face notes | Done | `samples/fz1073/RECORDING_SCRIPT.md` |
| Storyboard | Done | `samples/fz1073/STORYBOARD.jpg` |
| Direction video (scratch voice, "YOUR CLIP nn" slots) | Rendered, 488 s | `~/Movies/fz1073-direction/out/direction.mp4`, `direction_timeline.md` |
| Licensed real photos and Commons video (cabin, clouds, landing) | Done, credited | `assets/photos/`, `assets/vid/` (`FETCH.sh` re-downloads), `CREDITS.md` |
| Daylight reconstructions from Google Flow, invented faces | Approved by Rahul 7 Nov 2026 | `assets/ai/r_*.jpg`; decisions in `FLOW_CLIP_PLAN.md` |
| Animated moments (aisle run, dive, tilted window, approach, apron) | Approved | `assets/ai/r_*.mp4` (gitignored copies of `flow_clips/`) |
| Merge pipeline: trim, Whisper, re-time, composite, sound, export | Done and tested | `make_long.py`, `sound2.py` |
| Product brainstorm (Rahul AI Video Studio) | Draft | `docs/00-product-brainstorm.md` |

## 2. One-time setup on the Mac (about 10 minutes)

```bash
brew install ffmpeg node python@3.12
git clone -b claude/awesome-goldberg-6n0u1a https://github.com/RahulNishad/ai-editor.git
cd ai-editor/samples/fz1073
npm install
npx playwright install chromium
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 storyboard.py        # smoke test: prints the scene count and length
```

On macOS the renderer uses the GPU automatically. Set `RENDER_GPU=1` to force it elsewhere.

## 3. Finish the FZ1073 video

0. **Watch the direction video first.** `.venv/bin/python make_direction.py --work ~/Movies/fz1073-direction --workers 4` (about 12–15 min) renders the whole film with a scratch voice and a "YOUR CLIP nn" slot wherever Rahul appears, with the shot and face note. `direction_timeline.md` lists every clip with its start time. Record to it.

1. **Record** one vertical clip per scene, `01.mp4` … `24.mp4` (10 on camera, 14 voice only) (retake = `05_2.mp4`, highest number wins), 1080p 30 fps, 2 s silence before and after. Follow `RECORDING_SCRIPT.md` and `STORYBOARD.jpg`.
2. **Put the clips in one folder**, e.g. `~/Movies/fz1073-takes`.
3. **Run:**
   ```bash
   cd ai-editor/samples/fz1073
   .venv/bin/python make_long.py --takes ~/Movies/fz1073-takes --work ~/Movies/fz1073-build --workers 4
   ```
4. **Review** `~/Movies/fz1073-build/out/`:
   - `final.mp4` — 1920×1080, ~6.5 Mbps, −14 LUFS.
   - `report.md` — every take, how much was trimmed, and a CHECK flag where a clip's length does not fit its script (usually a missed or extra line).
   - `subtitles.srt` — Whisper text in Devanagari; proof-read before uploading as YouTube captions.
   - `chapters.txt` — paste into the description.
5. **Publish checklist:** open each source in `README.md` and confirm the facts; paste `CREDITS.md` into the description; in YouTube Studio answer **Yes** to *altered or synthetic content*.

## 4. How the pipeline works

- `script.long.json` → per scene: `layout` (C = Rahul centred over blurred scene, L = Rahul in a right-hand card, F = full-screen graphic with his voice), `look` (3D or template), `photos` (real or AI, with Ken Burns timing), `params`, `phrases`, `source`, `fallback_*`.
- `make_long.py`: picks takes → trims silence/long pauses → conforms to 1080×1920 → Whisper → builds `timeline.long.json` from real take lengths → renders frames with `render.js` + `comp.html` → composites Rahul per layout → `sound2.py` (bed, ducking, booms, riser, −14 LUFS) → exports.
- `ai_assets.py`: `assets/ai/<name>.jpg|png|webp|jpeg` becomes a still; `assets/ai/<name>.mp4` becomes a frame-exact clip. Missing images fall back to the real photo or 3D look.
- `commons.py`: search and download licensed Commons photos (`python3 commons.py search "…"`, `get "File:…" key`).

## 5. Decisions already made (do not re-open without Rahul)

- Claude directs **and** builds the visuals in code; Figma is not used. Reconstruction shots come from Google Flow (Nano Banana stills free, Veo video paid).
- **Flow validation gate:** no paid Flow generation until two independent reviewer agents say READY and Rahul approves the prompts and start stills (full rule in `CLAUDE.md`).
- Mostly stills, a few animated moments. Daylight (attack about 08:21 local), bright cockpit, correct 737 MAX layout: captain left seat, door behind and between the seats, attack from behind.
- Invented AI faces are allowed, labelled "AI RECONSTRUCTION · NOT THE REAL PERSON"; never resemble the real people.
- Crash axe may be shown (Option B), never touching anyone. Injured captain after the attack: restrained blood on the back of the head, collar and hand, no open wounds (Rahul, 7 Nov 2026).
- Name tags only on stills, not on moving clips. Flow and Veo watermarks are blurred with `delogo`, not cropped.
- Style: presenter-led, one thing on screen at a time, key-phrase captions, charcoal/white/red, Anton + Inter, source lines on every fact.
- Long video first; the vertical Short is not built yet. The product app waits until the skill has been proven on a few real videos.

## 5b. Second video: Diwali (started 8 Nov 2026)

`samples/diwali/`: 14-scene, ~4-minute script (`script.long.json`), `RECORDING_SCRIPT.md`, `STORYBOARD.jpg`, 15 licensed Commons photos with `CREDITS.md`, research table in `README.md`, and four proposed Flow clips in `FLOW_CLIP_PLAN.md` (not generated; the gate applies). Rahul recorded the 14 clips on 8 Nov 2026 (HDR phone takes on the lime green cloth); `make_long.py` now converts HLG to SDR and keys the cloth out (`key_presenter.py`), matting him onto the scenes with no card. Final: `~/Movies/diwali-build/out/final.mp4` (6:28, 325 MB, -14 LUFS) with `subtitles.srt`, `chapters.txt`, `report.md`. Same commands as fz1073, run inside `samples/diwali`; add `--key on` if the cloth is not auto-detected. The word-synced on-screen transcript (`captions.py`) is on by default. A vertical Short comes from the same build: `.venv/bin/python make_short.py --build ~/Movies/diwali-build --work ~/Movies/diwali-short` (scenes 1, 6, 9, 11, 13; about 2:25). Whisper runs the `medium` model by default (downloaded 8 Nov 2026; `small` misheard too much Hindi).

## 5c. Third video: Panchkula school case (started 8 Nov 2026)

`samples/panchkula/`: 24-scene, 1,193-word (~8.5 min) investigative script on the Panchkula school assault and the parenting question, written in its own session (commit 5a75de4). Children never identified; causes framed as lines of inquiry. `README.md` lists the blocked outlets (India Today, HT, Indian Express, TOI, NDTV) and the NCERT 81% figure (via Scroll/PTI) as pre-publish checks. Storyboard renders; direction video not yet rendered; four Flow clips proposed, not generated.

## 6. Open items

1. **Record the 24 clips** against the direction video and run §3.
2. **Verify sources.** Open each link in `README.md` (Claude in Chrome) and fix any mismatch, especially the headcount, the weapon wording and the 9 Oct UAE claims.
3. **Known limits** in the approved stills: panels drawn as an older 737 layout, axe drawn hammer-like. Fix only if Rahul asks, through the gate.
4. **Upload the updated skill** `skills/think-with-rahul-nishad-production.zip` at claude.ai once Rahul approves it.
5. **Shorts version** (9:16, 45–75 s) from the same assets.

## 7. Gotchas learned the hard way

- Load fonts before drawing to canvas (already handled in `comp.html`), or map labels fall back to a serif.
- Wikimedia rate-limits originals; `commons.py` downloads standard-width thumbnails (1920/1280) with pauses.
- `ffmpeg` inside a `while read` loop eats stdin; scripts use `-nostdin`.
- The scratch Hindi voice (Piper `hi_IN-rohan-medium`) only reads Devanagari; `text_dev` in the script holds it.
- Rendering in the cloud without a GPU took ~1 hour per 8 minutes; on this Mac the direction video takes 12–15 min with `--workers 4`.
- Homebrew's plain `ffmpeg` has no `drawtext`; `storyboard.py` uses `ffmpeg-full` when installed.
- macOS file names are case-insensitive: `ai_assets.py` checks `os.path.samefile` before replacing a still, or `.JPG` deletes `.jpg`.
- Commons originals often fail (error 56/429); `commons.py getvid` uses the 1080p/720p transcodes.
- Only one session should edit `samples/fz1073` at a time; two sessions rendering the same files mix half-finished edits.

## 8. Starter prompt for Claude Desktop (Claude Code) on the Mac

Open Claude Code in the `ai-editor` folder and paste:

```text
Read CLAUDE.md and HANDOFF.md. Do the one-time setup in HANDOFF §2 if it is not done, and run the storyboard smoke test. Then tell me what is left. When I give you my takes folder, run HANDOFF §3, review report.md, show me any CHECK flags and a few frames from final.mp4, and walk me through the publish checklist. Before publishing, open every source in samples/fz1073/README.md with Claude in Chrome and list any fact that differs.
```
