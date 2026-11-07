# Rahul AI Video Studio — instructions for Claude

Read `HANDOFF.md` first. It has the current state, setup and the next steps.

## What this repo is
A local, script-driven documentary video pipeline for the YouTube channel **Think With Rahul Nishad** (tagline: Think Beyond Headlines!). Claude directs; the code renders. The first production is `samples/fz1073` (flydubai FZ1073 cockpit attack, ~7.6 min, 16:9).

## Rules that always apply
- **Script is the single source of truth:** `samples/fz1073/script.long.json`. `RECORDING_SCRIPT.md` and `STORYBOARD.jpg` are generated from it (`script_to_md.py`, `storyboard.py`). Never hand-edit the generated files.
- **Facts:** attribute every claim ("UAE ke mutabik…"), label claims as CLAIM, show SOURCE lines, never invent numbers. Headcount is "170+" because reports vary 172–182.
- **People:** never show the faces of the real people (captain, first officer, plumber, dentist, pilots). No blood, no weapons, no airline logos in AI images. Do not name the accused.
- **Images:** real photos only from Wikimedia Commons with CC BY / CC BY-SA / PD licences, credited on screen and in `CREDITS.md`. AI images are labelled "AI RECONSTRUCTION" or "AI ILLUSTRATION". Never use a CC BY-SA photo as an AI reference image.
- **Original footage is read-only.** Takes are only read; all outputs are new files.
- **Commit and push** to branch `claude/awesome-goldberg-6n0u1a` after each meaningful change.

## Key commands (run inside `samples/fz1073`)
- Storyboard check (fast, ~10 s): `python3 storyboard.py`
- Direction video before recording (scratch voice + "YOUR CLIP" slots, ~25 min on a Mac): `.venv/bin/python make_direction.py --work ~/Movies/fz1073-direction`
- Final video from recorded takes: `.venv/bin/python make_long.py --takes <folder> --work <work dir>`
- Regenerate recording script: `python3 script_to_md.py script.long.json RECORDING_SCRIPT.md`
