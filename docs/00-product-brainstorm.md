# Rahul AI Video Studio v2 — Product Brainstorm

Status: discussion draft, 2026-11-06. Nothing here is implemented yet.

## Product vision (Rahul, 7 Nov 2026)

**Rahul AI Video Studio**: an AI-powered local documentary video editor for Mac, running in a local browser.

> Your script. Your footage. Your AI director.

1. Write your script.
2. Upload your recording.
3. Let Claude understand your content.
4. Approve 3D animations.
5. Edit everything on a timeline.
6. Export professional videos.

How the FZ1073 pipeline maps to it today: steps 1 and 3 are `script.long.json` plus Claude's research; step 4 is the direction video (`make_direction.py`) with Google Flow stills, Commons photos and footage, and Claude-rendered cards; steps 2 and 6 are `make_long.py`. Step 5, the editable timeline, is the main piece still to build.

This document reconciles three inputs:

1. The proposed product direction (six screens, multitrack editor, Claude as AI director, Figma Weave for animation, FFmpeg rendering, 16:9 + 9:16 outputs).
2. The earlier Flask MVP and its handoff pack (approval-based storyboard, manual Weave handoff, cutaway-only export, estimated timestamps).
3. The approved editing recipes in the `think-with-rahul-nishad-production` skill (how the videos that actually performed were cut).

Two things were verified live during this session and are treated as facts below:

- **Claude Code in the terminal is the AI director.** There is no separate Claude API agent inside the app. Claude Code already holds the Figma MCP connection, so the app never needs its own MCP client or OAuth flow.
- **What the Figma MCP exposes for Weave today.** `weave_list_tools` returned **zero published workflows** in the account. `weave_find_model` returned direct, runnable models: Veo 3.1 Text-to-Video and Veo 3.1 Image-to-Video. Each run costs about 90 credits, supports 4 s / 6 s / 8 s clips, 720p / 1080p / 4K, and 16:9 or 9:16. Every run is gated behind an explicit cost-approval prompt. Outputs come back as download URLs, so Claude Code can pull them straight into the project folder. `export_video` can also render a Figma motion timeline to MP4.

---

## 0. Update: Claude generates the animation, Figma is optional

Decision from discussion: avoid depending on Figma. Claude both directs and generates.

Proven in `spikes/claude-3d-render`: Claude writes a Three.js scene, headless Chromium renders it frame by frame, FFmpeg encodes it. A 6 s 1080p 3D clip rendered in about 100 s on a 4-CPU container with no GPU and no credits.

What this covers well: 3D data scenes, maps and routes, timelines, counters, charts, headline and document cards, flow diagrams, stylised 3D environments (aircraft, cockpit, city, boardroom), camera moves, particles, parallax. Every number is exact, every clip is editable and re-renderable, any length.

What it does not cover: photoreal footage of people and places. For that, use licensed stock or real footage. A diffusion model such as Veo stays an optional plug-in, not a dependency.

So the generator classes in §1.4 become: **Claude 3D/motion scene (default)**, **template card (same renderer)**, **optional external AI video**.

## 1. What changes versus the original brief

### 1.1 The footage model is multi-take, vertical, and matted
The brief says "upload your MP4". The approved recipe says: one vertical phone clip per scene, in script order, keyed off a lime-green cloth or matted with RVM, composited at ~1.25× onto slowly moving scene backgrounds for the 16:9 long video, and at 1.5× shifted down for Shorts.

Consequences:
- A project has **many takes**, each tagged to a script scene, not one source file. Duplicate takes must be detected.
- The presenter is a **layer**, not the base track. The base track is a background. This is the opposite of the Flask MVP, where the original video was the base and animations were cutaways.
- The 16:9 output is **composed**, never a crop of a vertical. The 9:16 output is also composed from the same layers with different framing. "One master timeline, two output profiles" is correct, but each clip needs per-profile transform (scale, position, crop) rather than a global reframe.
- Matting is a first-class backend job (clean plate, chroma key in YCrCb, RVM as garbage matte, light wrap). It is heavy on CPU/GPU and must run as a background job with cached alpha mattes.

### 1.2 Four layout modes, not three placement modes
The brief proposes full-screen cutaway, picture-in-picture, overlay. The approved recipe uses:

| Mode | Meaning | Maps to brief |
| --- | --- | --- |
| **L** | Presenter right, one graphic left explaining his line | Picture-in-picture (inverted: graphic is the inset) |
| **C** | Presenter centred, nothing else | Default |
| **S** | Full-screen establishing shot at chapter start | Full-screen cutaway |
| **F** | Full-screen graphic/storyboard panel, voice continues | Full-screen cutaway with VO |

Proposal: the timeline models **layout mode as a property of a time range**, with smooth slides between modes, and the generated Weave clip or graphic is attached to that range. This is simpler to edit than free-form PiP boxes and matches how the videos were actually cut. Free positioning stays available as an override.

### 1.3 Captions are key phrases, not subtitles
The brief has a SUBTITLES track with lower-third subtitles and an SRT export. The channel's own feedback is "less transcript": 2 to 4 bold words every 4 to 8 seconds, never over the face, one thing on screen at a time.

Proposal: two separate tracks.
- **Key phrases** (burned in, editable, Claude proposes them from the transcript, user approves). This is the default on-screen text.
- **Full subtitles** (SRT only, uploaded to YouTube as closed captions, never burned by default). Generated from the corrected transcript.

### 1.4 Graphics are a bigger category than "3D animation"
Veo produces cinematic video scenes. It cannot reliably produce the things that carried the best videos: bill counters, bar charts with SOURCE lines, deal cards, split "X vs Y", timelines, chapter tags, end cards. Those must be **deterministic templates** rendered in-app, with exact numbers typed in, labelled ILLUSTRATION or SOURCE as the skill requires.

Proposal: three generator classes on the same "scene" object.

| Class | Produced by | Approval | Cost |
| --- | --- | --- | --- |
| Cinematic scene / background | Weave Veo 3.1 (T2V or I2V) via Claude Code | Keyframe first, then video | ~90 credits per clip |
| Data graphic / card | In-app template renderer (HTML → PNG/WebM via headless Chromium, or FFmpeg filters) | Preview in UI | Free |
| Motion graphic | Figma timeline → `export_video` | Preview in Figma | Free |

The "I2V after approving a still" flow is the right approval gate: a still image is cheap and fast to judge, and the approved still becomes the first frame, which also gives style consistency across scenes.

### 1.5 Sound design is part of the product
The approved recipe specifies an ambient bed ducked under voice, whooshes on card entries, booms on reveals, a riser into the key line, music silence before the final question, voice at −14 LUFS. None of this is in the brief. It needs a **music/SFX track** with sidechain ducking and a loudness-normalise step in export. Cue placement can be proposed by Claude from the storyboard (card entries and reveals are already known events).

---

## 2. Revised screens

Keep six screens, but re-scope them.

1. **Projects** — list, create, resume, backups. Also a "Takes inbox": drop a folder of phone clips and the app probes, de-duplicates and orders them.
2. **Script & Takes** — left: script scenes (from the production package or pasted). Right: takes mapped to scenes, transcript per take (faster-whisper, word timestamps), waveform, auto-detected pauses/restarts/stumbles with proposed cuts. Diff between script and spoken words. This replaces "Script & Transcript Editor" and is where most human correction happens.
3. **Storyboard** — Claude's plan per scene: layout mode, generator class, prompt, reference, key phrases, sound cues, duration. Approve / edit / reject per item. Approve-still then approve-video for Weave scenes. Credit spend is shown before approval.
4. **Editor** — multitrack timeline (see §4) with preview.
5. **Look & Sound** — matting quality check (hair/beard crop at 100%), background dimming, palette, fonts (Anton/Inter), caption style, music bed level, ducking, per-profile framing for Shorts.
6. **Export** — long 16:9, Shorts 9:16, SRT, chapters text, thumbnail frame export, edit-plan document, project backup zip. Bitrate target so a 7-minute 1080p stays under 400 MB.

---

## 3. How Claude Code drives the app

Because Claude runs in the terminal, the app is an **engine with a contract**, and Claude Code is a client of that contract. Nothing agentic lives inside the app.

Contract pieces:
- **Project folder is the source of truth.** `project.json` (or SQLite plus exported JSON) holds script, takes, transcripts, storyboard, timeline, approvals, and an append-only `agent-journal.jsonl`.
- **A local HTTP API and a thin CLI** (`rvs` or similar) that Claude Code calls: `rvs analyse`, `rvs storyboard propose`, `rvs scene import <id> <file>`, `rvs timeline propose <patch.json>`, `rvs render --profile long`. The CLI is also what a human can script.
- **Permissions are enforced by the app, not by prompt.** Claude can write to `proposals/`. Only the UI can move a proposal to `approved`. Render refuses unapproved scenes. Original take files are read-only on disk; every derived asset is a new file.
- **Activity panel** is the UI tailing `agent-journal.jsonl`. Claude Code writes journal entries as it works (inspected, transcribed, proposed, waiting for approval). No websocket to Claude needed.
- **A project `CLAUDE.md` plus a skill** tells Claude Code the procedure: read script, call analyse, write storyboard proposal, stop; after approval, run Weave per approved scene with cost confirmation, download outputs by scene ID into `assets/generated/`, import, stop; propose timeline patch, stop.

Permission table, restated for this model:

| Action | Who | Gate |
| --- | --- | --- |
| Probe takes, transcribe, detect pauses | App job, triggered by Claude or UI | None |
| Propose storyboard, key phrases, sound cues, timeline patch | Claude writes a proposal file | None to propose; UI approval to apply |
| Run Weave (spend credits) | Claude Code via Figma MCP | Scene approved in UI + Weave cost prompt |
| Apply cuts / modify presenter footage | App, non-destructive | UI approval of the proposal |
| Render export | App job | UI click |

Open question: should Claude Code be able to apply a timeline patch directly when the user has pre-authorised "small edits" (trim under 1 s, caption text)? Suggest no for v2; keep a single approval path and add trust levels later.

---

## 4. Timeline model

Tracks (top to bottom):

1. Key phrases / cards
2. Graphics & generated scenes (with layout mode L / C / S / F per range)
3. Presenter (matted takes, per-profile transform)
4. Background (Weave scenes or illustrations, dimmed/blurred, slow motion)
5. Voice (from takes, cuts applied, loudness-normalised)
6. Music & SFX (bed with ducking, cue markers)

Operations: trim, split, ripple delete, move, slip, mute/solo, change layout mode, swap asset, edit text in place, undo/redo. Everything is a JSON patch on the timeline document, so undo/redo and Claude proposals share one mechanism.

Preview is the hard part. Real-time compositing of matted video plus moving backgrounds plus text is not feasible in a browser video element.

Proposal: **two-tier preview**.
- **Layout preview** (instant): canvas draws placeholder boxes, the raw take, text and the background still at the current playhead. Good enough for arranging.
- **Proxy preview** (seconds): backend renders a 540p proxy of the selected range with FFmpeg, cached by hash of the inputs. Play that in the video element. Full render only at export.

---

## 5. Technology

Agree with the brief, with notes.

| Layer | Choice | Note |
| --- | --- | --- |
| Frontend | React + TypeScript + Vite + Tailwind | Fine. |
| Timeline | Custom | Fine. Keep it a pure function of the timeline JSON. |
| Waveform | WaveSurfer.js | Fine; generate peaks on the backend for long takes. |
| Backend | FastAPI | Fine. |
| Storage | SQLite for index; JSON on disk for the project document | JSON on disk keeps the project portable and lets Claude Code read it directly. |
| Jobs | In-process queue with persistent job table | Good enough for one Mac. |
| Transcription | faster-whisper, large-v3 or distil, word timestamps | Hinglish needs a correction pass in the UI. Check Devanagari vs romanised output preference. |
| Matting | RVM (PyTorch, MPS on Apple Silicon) + clean-plate chroma key | Heaviest dependency. Decide if v2 ships with it or with chroma key only. |
| Graphics templates | HTML/CSS templates rendered by headless Chromium to PNG/WebM | Reuses web skills; exact typography control. |
| AI scenes | Weave Veo 3.1 via Figma MCP from Claude Code | No in-app integration needed. |
| Rendering | FFmpeg filter graphs generated from timeline JSON | Build a small compositor module with golden tests. |
| Port | `http://localhost:8787` | Keep. |

Reference inputs from Weave are URLs or an in-chat picker. For image-to-video, Claude Code needs the approved keyframe reachable by Weave. Options: let Weave generate the keyframe itself (so the asset is already in Weave), or upload via the picker. Verify in the first spike.

---

## 6. Roadmap, revised

The brief wants the multitrack editor from the start. Agreed, with the engine built first so the editor has something real to drive.

| Milestone | Deliverable | Done when |
| --- | --- | --- |
| **M0 Spike (1 week)** | Prove the risky bits: FFmpeg compositor for one L-mode shot from a matted take on a moving background; one Weave Veo run end to end from Claude Code into a project folder; faster-whisper word timestamps on a Hinglish take. | Three throwaway scripts, each producing a file. |
| **M1 Engine + Script & Takes** | FastAPI, project folder, takes inbox, transcription, pause/restart detection, script-to-take mapping UI, CLI, agent journal. | A project can be created and fully analysed by Claude Code from the terminal. |
| **M2 Storyboard + Weave** | Proposal/approval model, three generator classes, keyframe-then-video approval, credit display, import by scene ID. | Approved scenes have assets in the project; unapproved scenes cannot be generated. |
| **M3 Editor** | Six-track timeline, layout modes, patch-based undo/redo, two-tier preview. | A full long video can be arranged and previewed. |
| **M4 Render** | Both profiles, per-profile transforms, captions, sound ducking, loudness, SRT, chapters, size target. | Both MP4s pass the operator checklist. |
| **M5 Polish** | Autosave, recovery, backups, template library growth, trust levels for small agent edits. | Resume a project after a crash without loss. |

Matting: M0 proves it; whether it ships in M1 or M4 is a decision (see §7).

---

## 7. Decisions needed before implementation

1. **Footage model.** Confirm the v2 input is multiple vertical takes per scene (approved recipe), with single long 16:9 takes also supported. Or is the plan to move to recording one long 16:9 take?
2. **Matting in v2.** Ship green-screen keying + RVM in v2, or ship C-mode-only (presenter on original background) first and add matting in M4?
3. **Captions default.** Key phrases burned in, full subtitles SRT only. Confirm.
4. **Weave path.** Direct model runs (Veo 3.1 via Claude Code, ~90 credits each) versus publishing Weave workflows first. Direct runs work today with nothing to set up. What credit budget per video is acceptable? That sets how many S/F scenes the storyboard should recommend.
5. **Preview fidelity.** Accept the two-tier preview (instant layout canvas + rendered proxy), or invest in a browser compositor?
6. **Graphics templates for v2.** Which 6 to 8 templates first? Suggested: chapter tag, key phrase, source stat card, bar chart, counter, split X vs Y, headline card (AS PUBLISHED / PARAPHRASED), end card.
7. **Agent trust.** Single approval path for everything Claude proposes in v2, trust levels later. Confirm.
8. **Project format.** JSON on disk as source of truth (portable, Claude-readable) with SQLite as index. Confirm.
