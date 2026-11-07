# Flow animation pack — FZ1073 (image-to-video)

Short 5–8 second motion clips made from the stills we already have. Each clip replaces its still in the video: save it as `assets/ai/<file>.mp4` and `ai_assets.py` turns it into frames automatically. A clip shorter than its slot holds on its last frame, so 6–8 s is enough everywhere. Anything you skip keeps the still with its slow camera move.

## How to make each clip in Flow

1. Open the Flow project, pick **Frames to Video** (image-to-video), 16:9, 8 s.
2. Use the **start frame** listed for each clip. The 13 picked Flow stills are saved at full size in `assets/ai/flow/<file>.jpg`, so you can upload those instead of searching the gallery. "Flow #n" is the Flow gallery order from the top (0 = newest). "Repo" means `assets/ai/<file>.jpg` (same picture as the ChatGPT zip).
3. Paste the prompt, then add the **motion suffix** below.
4. Generate 2 variations, keep the one where hands and faces stay hidden and nothing warps. Download, rename exactly as listed, `.mp4`.

**Motion suffix (add to every prompt):**

> Realistic documentary camera, handheld but steady, natural motion blur, 24 fps feel. Keep every face turned away or out of frame for the whole clip. No blood, no wounds, no weapons, no text, no logos. Do not add new people.

**Rules that still apply:** no faces of the real people, no blood or weapons, no airline livery. Each clip is labelled "AI RECONSTRUCTION" in the video, and YouTube's *altered or synthetic content* box is ticked. Flow's cockpits look Airbus-style while the ChatGPT stills show a 737 with yokes, so keep one source per scene.

## Reconstruction clips (priority order)

| # | File | Scene · line it plays under | Start frame | Prompt |
| --- | --- | --- | --- | --- |
| 1 | `r_door_open` | 10 · "Aur darwaaza khul gaya." | Flow #19 | The cockpit door swings fully open toward camera. Warm cabin light floods the dark flight deck, dust drifts in the beam, the silhouetted passenger steps through the doorway and stops. Camera eases back slightly. |
| 2 | `r_aisle` | 11 · "Darwaaza khulte hi aam passengers andar ghuse." | Flow #16 | The stocky man in the dark grey t-shirt runs away from camera down the aisle toward the bright open door. Passengers half-rise from their seats and turn toward the front. Camera follows a few steps behind him, slight shake. |
| 3 | `r_door_hand` | 10 · "This is the last push, Smit…" | Flow #21 | Red emergency light pulses slowly. The captain's hand tightens on the door handle, the knuckles strain, then the handle turns down and the door begins to move. Slow push-in on the hand. |
| 4 | `r_struggle_1` | 01 hook and 06 · "aapka apna co-pilot hi aap par hamla kar deta hai" | Flow #28 | The two pilots strain against each other across the centre console, shoulders twisting, seats rocking slightly. The red master warning lights flash on the glareshield. Slow push-in from behind the seats. |
| 5 | `r_dive_1` | 08 · "plane tezi se neeche girne laga" | Flow #25 | The white airliner pitches further nose-down and drops through the moonlit cloud layer. Cloud streaks rush past, wingtip lights blink. Chase camera falls with it, slight roll. |
| 6 | `r_dive_window` | 08 · "zindagi aur maut ke beech ke pal" | Flow #23 | Through the cabin window the horizon keeps rolling and tilting, cloud tops and city lights slide past fast, the wing flexes. The window frame vibrates slightly. |
| 7 | `r_restrain` | 11 · "chokehold mein pakda, aur cockpit se bahar kheench liya" | Flow #15 | The stocky man pulls the man in the white shirt backward out of the cockpit doorway into the galley, both stumbling two steps toward camera. Faces stay turned toward the cockpit. Short, tense, then still. |
| 8 | `r_galley_hold` | 11 · after the pull-out | Flow #13 | Overhead, almost still: the men on the galley floor hold the pinned man down, a brief shift of weight, then they settle. Very slow push-in from above. |
| 9 | `r_aid` | 12 · "ghayal captain ka khoon rokne mein lag gaye" | Flow #11 | The man in the light blue shirt presses the folded grey blanket more firmly onto the captain's forearm. The captain leans back against the galley cart and breathes slowly. Calm, steady, slow push-in. |
| 10 | `r_aid_close` | 12 · second half | Flow #9 | Close-up: the hands press down on the blanket and hold. The oxygen mask tubing on the floor sways slightly with the aircraft's motion. Shallow focus pulls from hands to mask. |
| 11 | `r_approach` | 13 · "plane ko Saudi Arabia ke Tabuk mein surakshit utaar diya" | Flow #5 | Final approach at night: the runway lights grow larger and slide beneath the nose, the pilots' silhouettes hold steady, a gentle flare, the main lights pass under. Camera locked behind the seats. |
| 12 | `r_takeover` | 13 · "Unhone controls sambhaale" | Repo `r_takeover` | The two pilots in plain white shirts settle into the seats; one grips the controls, the other reaches up and flips switches on the overhead panel. The red warning light fades to normal panel glow. Camera locked behind them. (Flow #6/#7 show a parked jet outside; skip them for this shot.) |
| 13 | `r_apron` | 13 · last beat, after landing | Flow #3 | Dawn on the desert apron: emergency lights flash on the fire trucks and ambulances, ground crew walk toward the airstairs, dust drifts in the low sun. Slow lateral drone drift. |
| 14 | `r_window_dawn` | 21 · "insaan ki himmat hi aakhri suraksha hoti hai" | Flow #1 | The sun rises above the cloud deck, light slides along the wing and turns it gold, the passenger's hand rests still on the window frame. Very slow push-in. Peaceful. |
| 15 | `r_struggle_2` | 06 · "crash axe se … hamla kiya" (under the claim) | Flow #27 | Red light flashes. The pilot's hand clenches on the controls while the other arm pushes harder against his shoulder, the attitude display tilts nose-down. Tight, shallow focus, slight shake. |

## Explainer illustration clips (optional)

| File | Scene | Start frame | Prompt |
| --- | --- | --- | --- |
| `a_globe_flights` | 04 · "Har din duniya mein lakhon log plane mein baithte hain" | Repo | The night Earth turns slowly, new golden flight paths arc between cities and tiny aircraft lights travel along them. Slow orbit. |
| `a_altimeter` | 08 · altitude drop | Repo | The altimeter needles unwind fast, a red warning reflection flickers on the glass. Locked close-up, slight vibration. No readable numbers. |
| `a_door_lock` | 09 · "sirf andar se khulte hain" | Repo | The heavy deadbolt slides shut with a solid stop and the keypad light stays red. Slow push-in. |
| `a_axe` | 07 · "crash axe ek zaroori emergency tool hai" | Repo | Slow rack focus from the cockpit seat to the axe resting in its wall bracket, side light sweeping across it. The axe never moves and no one touches it. |
| `a_alps` | 17 · Germanwings | Repo | Slow, quiet drone drift over the snowy Alpine ridges at dawn, low clouds moving in the valleys. Somber. |

## After downloading

```bash
cd samples/fz1073
cp ~/Downloads/r_door_open.mp4 assets/ai/   # repeat per clip, exact names
python3 storyboard.py                        # quick check that every scene still resolves
```

If a clip looks wrong in the cut, delete the `.mp4` and its frame folder `assets/ai/<file>/`, and the still comes back.
