# Sample: FZ1073 — "34,000 feet par cockpit attack"

A 2:13, 1920×1080, 30 fps sample made entirely in one Claude Code session. No presenter footage, no Figma, no paid generation. It exists to test the pipeline and the channel style, not to publish as is.

## What made it

| Step | Tool | Notes |
| --- | --- | --- |
| Research | Web search (server-side) | News sites were blocked by this cloud environment's network policy, so pages could not be opened directly. See "Before publishing". |
| Script | Claude | Hinglish in Devanagari for the voice, English on-screen text. 11 scenes. |
| Scratch voice | Piper TTS, `hi_IN-rohan-medium` | Placeholder for Rahul's recording. Whisper understood it better than `pratham`. |
| Voice check | faster-whisper `small` | Used to compare the two voices. Same tool will transcribe Rahul's real takes. |
| Visuals | Three.js + HTML overlays, `comp.html` | 3D cockpit, generic 737 (no airline livery), 3D map from Natural Earth via `world-atlas`, cards, timeline. |
| Render | Playwright + headless Chromium, `render.js` | Frame-exact: the page exposes `renderFrame(n)`. |
| Sound | NumPy/SciPy synthesis, `sound.py` | Original drone bed, pulse, whooshes, booms, riser, cockpit caution beeps, ducking under voice. |
| Mix/encode | FFmpeg | Voice loudnorm to −14 LUFS; final mix measured −13.8 LUFS, −2.9 dBFS peak. |

## Rebuild

    npm install
    python3 build_timeline.py . rohan          # after generating vo/rohan_<scene>.wav with piper
    node render.js 0 4000                      # or split into ranges across workers
    python3 sound.py .                         # writes audio/voice.wav, music.wav, sfx.wav
    # mix and mux: see the commands in the session log, or the recap in docs/

## Facts used on screen and in narration

| Claim | Status | How it is phrased | Source (as found via search) |
| --- | --- | --- | --- |
| flydubai FZ1073, Dubai → Tel Aviv, 30 Sep 2026, Boeing 737 MAX 8 | Fact | Stated | Flightradar24 blog/X post; Euronews; Wikipedia |
| Take-off 03:05 UTC, altitude fluctuations 05:21 UTC | Data | "Lagbhag sava do ghante baad" | Flightradar24 timeline |
| People on board | Disputed: 172, 174, 180, 182 | "170 se zyada log" + "Reports vary: 172–182" | ABC, CBC, Wikipedia, AP via search |
| First officer attacked the captain | Official (Saudi MoI preliminary; UAE AG) | "UAE ke Attorney General ke mutabik" | Saudi Interior Ministry via Al Jazeera; UAE AG via WAM |
| Weapon: crash axe | Official claim, accounts vary | Attributed to UAE; on-screen "weapon accounts vary" | UAE AG; Al Jazeera 3 Oct; others say knife |
| First officer: 29, Omani | Official (UAE AG) | Age and nationality only; name not used | UAE AG via WAM, Haaretz 9 Oct |
| Drop from ~34,000 ft to ~15,000 ft within minutes | Data as reported | "Kuch hi minuton mein, kareeb 15,000 feet" | Flightradar24 ADS-B data as reported; durations differ by outlet |
| Captain opened the cockpit door while wounded; "This is the last push, Smit…" | His account as reported | Quote card marked "as reported" | Fox News; CBC interview reports |
| Plumber Yaniv Hayoun pulled the attacker out | Eyewitness/press accounts | Named, role described | AP, WION |
| Dentist Dr Shota Musaev treated the captain | Eyewitness/press accounts | Named, role described | AP, WION |
| Off-duty flydubai pilots Henson Steven and Rowan Tooth landed at Tabuk | Named after UAE honours | Named on card | Gulf News, The Media Line, Ynet |
| UAE AG: plan to crash into Ben Gurion terminal | Official claim | "UAE ka daava hai" + CLAIM tag | WAM, Haaretz, 9 Oct |
| NIA case under Anti-Hijacking Act 2016 and UAPA | Fact | Stated | Business Today, Outlook, 10 Oct |
| UAE: airline's pre-hiring checks found nothing | Official claim; Reuters reports a conflicting Israeli account | Kicker line on the question card | UAE AG; Reuters via search |

Deliberately left out: the first officer's name, any motive beyond the UAE's stated claim, political attributions (Iran links), passenger lawsuits, graphic details, any real photos or airline logos.

## Before publishing

1. Open and read each source page; this session could not. Fix anything that differs.
2. Replace the scratch voice with Rahul's recording. Re-time with Whisper word timestamps.
3. Decide the headcount wording once the official flydubai figure is confirmed.
4. Optional: add presenter shots in L/C layout between scenes, per the approved long-form recipe.
