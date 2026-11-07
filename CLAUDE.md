# Rahul AI Video Studio — instructions for Claude

Read `HANDOFF.md` first. It has the current state, setup and the next steps.

## What this repo is
A local, script-driven documentary video pipeline for the YouTube channel **Think With Rahul Nishad** (tagline: Think Beyond Headlines!). Claude directs; the code renders. The first production is `samples/fz1073` (flydubai FZ1073 cockpit attack, ~7.6 min, 16:9).

## Rules that always apply
- **Script is the single source of truth:** `samples/fz1073/script.long.json`. `RECORDING_SCRIPT.md` and `STORYBOARD.jpg` are generated from it (`script_to_md.py`, `storyboard.py`). Never hand-edit the generated files.
- **Facts:** attribute every claim ("UAE ke mutabik…"), label claims as CLAIM, show SOURCE lines, never invent numbers. Headcount is "170+" because reports vary 172–182.
- **People:** AI images may show invented faces (Rahul's decision, 7 Nov 2026). Never try to make them look like the real captain, first officer, plumber, dentist or pilots, and never use their photos as references. Any AI image showing a named person's face is labelled "AI RECONSTRUCTION · NOT THE REAL PERSON". The cockpit crash axe may be shown in the attack reconstruction (Rahul's decision, 7 Nov 2026), never touching anyone; no other weapons. After the attack, the captain may be shown injured with restrained bleeding from the back of the head, on his collar and hand (Rahul's decision, 7 Nov 2026; sources say the dentist stopped his bleeding); no open-wound close-ups, no gore, no blood on anyone else. No airline logos in AI images. Cockpit layout: captain in the LEFT seat, first officer in the RIGHT seat, cockpit door in the rear wall behind and between the seats; the attack came from behind the captain's seat; the flight was in daylight (take-off 07:05 Dubai time). Do not name the accused.
- **Images:** real photos only from Wikimedia Commons with CC BY / CC BY-SA / PD licences, credited on screen and in `CREDITS.md`. AI images are labelled "AI RECONSTRUCTION" or "AI ILLUSTRATION". Never use a CC BY-SA photo as an AI reference image.
- **Flow validation gate (Rahul, 7 Nov 2026):** nothing is sent to Google Flow (or any paid image/video tool) until (1) the plan lists every shot with its start image, still prompt and motion prompt, (2) at least two independent reviewer agents have checked it against the real event (cockpit layout, who sits where, door position, time of day, sequence of events), the script line it plays under, continuity with neighbouring shots, layout framing, and Flow feasibility and policy, (3) every FIX is applied and re-reviewed until both say READY, and (4) Rahul has seen the prompts and the start stills and approved them. Free stills may be generated to give reviewers something to check; paid video only after approval.
- **Original footage is read-only.** Takes are only read; all outputs are new files.
- **Commit and push** to branch `claude/awesome-goldberg-6n0u1a` after each meaningful change.

## Key commands (run inside `samples/fz1073`)
- Storyboard check (fast, ~10 s): `python3 storyboard.py`
- Direction video before recording (scratch voice + "YOUR CLIP" slots, ~25 min on a Mac): `.venv/bin/python make_direction.py --work ~/Movies/fz1073-direction`
- Final video from recorded takes: `.venv/bin/python make_long.py --takes <folder> --work <work dir>`
- Regenerate recording script: `python3 script_to_md.py script.long.json RECORDING_SCRIPT.md`
