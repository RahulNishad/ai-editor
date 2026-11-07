# Handoff — from the cloud session to Claude on Rahul's Mac

Date: 7 Nov 2026. Branch: `claude/awesome-goldberg-6n0u1a` on `RahulNishad/ai-editor`.

## 1. Where things stand

The FZ1073 long video is **ready for Rahul's recording**. Everything except his 23 presenter clips is built and checked.

| Piece | Status | Where |
| --- | --- | --- |
| Research and fact table | Done (pages not opened, see §6) | `samples/fz1073/README.md` |
| Recording script, 23 scenes, Hinglish + Devanagari, face/expression notes | Done | `samples/fz1073/RECORDING_SCRIPT.md` |
| Storyboard showing where Rahul appears | Done | `samples/fz1073/STORYBOARD.jpg` |
| 13 licensed real photos with credits | Done | `samples/fz1073/assets/photos/`, `CREDITS.md` |
| 22 AI images from ChatGPT (15 reconstructions, 7 illustrations), reviewed | Done | `samples/fz1073/assets/ai/` |
| 3D scenes, maps, cards, timeline, captions renderer | Done | `samples/fz1073/comp.html` |
| Merge pipeline: trim, Whisper, re-time, composite, sound, export | Done and tested | `samples/fz1073/make_long.py`, `sound2.py` |
| Preview v2 with scratch voice and clip placeholders | Rendered in the cloud | see §7 |
| Product brainstorm for the future app | Draft | `docs/00-product-brainstorm.md` |
| Proposed improvements to the production skill | Not applied yet | `docs/01-skill-learnings-fz1073.md` |

## 2. One-time setup on the Mac (about 10 minutes)

```bash
brew install ffmpeg node python@3.12
git clone -b claude/awesome-goldberg-6n0u1a https://github.com/RahulNishad/ai-editor.git
cd ai-editor/samples/fz1073
npm install
npx playwright install chromium
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 storyboard.py        # smoke test: should print "23 scenes, about 7.6 min"
```

On macOS the renderer uses the GPU automatically. Set `RENDER_GPU=1` to force it elsewhere.

## 3. Finish the FZ1073 video

0. **Watch the direction video first.** `.venv/bin/python make_direction.py --work ~/Movies/fz1073-direction` renders the whole film with a scratch voice and a "YOUR CLIP nn" slot wherever Rahul appears, with the shot and face note. `direction_timeline.md` lists every clip with its start time. Record to it.

1. **Record** one vertical clip per scene, `01.mp4` … `23.mp4` (retake = `05_2.mp4`, highest number wins), 1080p 30 fps, 2 s silence before and after. Follow `RECORDING_SCRIPT.md` and `STORYBOARD.jpg`.
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

- Claude directs **and** builds the visuals in code; Figma is not used. External AI tools (ChatGPT images now, maybe Flow/Sora later) only fill reconstruction shots.
- Style: Rahul presenter-led, one thing on screen at a time, key-phrase captions not full subtitles, charcoal/white/red, Anton + Inter, source lines on every fact.
- Long video first; the vertical Short is not built yet.
- The product app (React/FastAPI editor, `docs/00-product-brainstorm.md`) waits until the production skill has been improved through a few real videos.

## 6. Open items

1. **Verify sources.** The cloud session could not open news pages; facts came from search summaries. Open each link in `README.md` and fix any mismatch, especially the headcount, the weapon wording and the 9 Oct UAE claims.
2. **Record the 23 clips** and run §3.
3. **Upload the updated skill** `skills/think-with-rahul-nishad-production.zip` at claude.ai (Customize, Skills) once Rahul approves it; it merges `docs/01-skill-learnings-fz1073.md`.
4. **Shorts version** (9:16, 45–75 s) from the same assets.
5. Optional: animate the AI stills (Sora/Flow/Kling) and save as `assets/ai/<same name>.mp4`.

## 7. Gotchas learned the hard way

- Load fonts before drawing to canvas (already handled in `comp.html`), or map labels fall back to a serif.
- Wikimedia rate-limits originals; `commons.py` downloads standard-width thumbnails (1920/1280) with pauses.
- `ffmpeg` inside a `while read` loop eats stdin; scripts use `-nostdin`.
- The scratch Hindi voice (Piper `hi_IN-rohan-medium`) only reads Devanagari; `text_dev` in the script holds it.
- Rendering in the cloud without a GPU took ~1 hour per 8 minutes; on Apple Silicon expect much faster.

## 8. Starter prompt for Claude Desktop (Claude Code) on the Mac

Open Claude Code in the `ai-editor` folder and paste:

```text
Read CLAUDE.md and HANDOFF.md. Do the one-time setup in HANDOFF §2 if it is not done, and run the storyboard smoke test. Then tell me what is left. When I give you my takes folder, run HANDOFF §3, review report.md, show me any CHECK flags and a few frames from final.mp4, and walk me through the publish checklist. Before publishing, open every source in samples/fz1073/README.md with Claude in Chrome and list any fact that differs.
```
