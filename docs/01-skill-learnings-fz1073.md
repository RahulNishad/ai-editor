# Skill learnings from the FZ1073 sample run

Proposed additions to the `think-with-rahul-nishad-production` skill. Not applied yet; review first.

## New section: "Claude-rendered visuals (no external AI video)"

- Default generator for illustrations is Claude-authored code: Three.js scenes and HTML cards rendered frame by frame in headless Chromium, encoded with FFmpeg. No credits, exact numbers, any length, re-renderable.
- Every page exposes `window.renderFrame(frame)` and sets `window.__ready`; time comes from the frame number only. Seed all randomness.
- Load fonts with `document.fonts.load()` before drawing to any canvas, or labels fall back to a serif.
- Reusable looks proven here: cockpit interior with live PFD/ND/EICAS screens and master-warning light; generic airliner (no livery) with cloud deck; 3D tilted map with glowing route, incident pulse and diversion curve; altitude counter with simplified ADS-B chart; quote card; hero cards; four-node investigation timeline; question card; end card.
- Air-crash and attack stories: reconstruct with silhouettes, instruments, alarms and doors. No blood, no weapon close-ups, no faces.
- Tag every reconstruction "ILLUSTRATION · RECONSTRUCTION" and every map "ROUTE ILLUSTRATIVE" or "APPROX. POSITION".

## New section: "Scratch voice and pacing"

- When Rahul has not recorded yet, build the cut on a Piper `hi_IN-rohan-medium` scratch voice so pacing can be judged. Write the voice script in Devanagari, spelling English words phonetically (e.g. "कॉकपिट", "यू ए ई").
- Measured pace: about 2.1 words per second. A 280-word script runs about two minutes.
- Check intelligibility by running the scratch voice through faster-whisper.

## Research rule additions

- When outlets disagree on a number, use wording that is true across all of them ("170 se zyada") and show the range on screen ("Reports vary: 172–182").
- Name official figures by role ("UAE ke Attorney General ke mutabik"). Use an accused person's age and nationality from the official statement, not their name, unless the story needs it.
- If the environment blocks news sites, say so in the deliverable and list the pages that must be opened before publishing.

## Sound recipe, now measured

- Bed: D-minor drone plus filtered wind, about −30 LUFS; ducked about 60 percent under voice.
- Voice: compressed, loudnorm to −14 LUFS. Final mix target −14 LUFS, true peak under −1.5 dBFS.
- Booms on the title reveal and three story reveals, pulse from title to the climax, riser into the final question, about one second of music silence before it.

## Environment notes for cloud sessions

- Hugging Face model downloads need `huggingface.co` and `us.aws.cdn.hf.co`, and `HF_HUB_DISABLE_XET=1`.
- faster-whisper's bundled PyAV can fail to open files; decode with FFmpeg to 16 kHz float and pass the array.
- YouTube pages are bot-checked from cloud sessions; ask for the MP4 or the subtitle file instead.
