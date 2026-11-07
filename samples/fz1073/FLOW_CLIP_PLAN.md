# FZ1073 animation plan: prompts for approval

Nothing in this file is generated until Rahul approves it. Each clip has two steps: a still (Nano Banana, free) that sets the exact layout, then an 8-second video from that still (Omni 1.2 Flash, 24 credits at 720p).

## What the last batch got wrong (Rahul, 7 Nov 2026)

- The captain sits in the **left** seat (four stripes). The first officer sits in the **right** seat (three stripes). Several stills put the captain on the right.
- The cockpit door is in the rear wall **directly behind and between the two seats**, opening into the forward galley. The stills put a door or handle at the side window.
- The captain was attacked **from behind**: the first officer left his seat, stood behind the captain's seat and attacked him there. The clips showed two seated pilots wrestling side by side.

## Fixed description added to every cockpit prompt

> Boeing 737 MAX 8 flight deck in flight, about 8 am, bright daylight through the windshield. Layout: the captain's seat is on the LEFT, the first officer's seat is on the RIGHT, a throttle pedestal between them, four large landscape displays across the panel, a horn-shaped yoke in front of each seat. The reinforced cockpit door is in the rear wall, directly BEHIND and BETWEEN the two seats, and opens backward into a small forward galley. Captain: South Asian man, early 40s, short black hair, white short-sleeve shirt, four gold stripes. First officer: slim Arab man about 29, short dark hair, white short-sleeve shirt, three gold stripes. Invented faces, not resembling any real person. Photorealistic documentary photo, 16:9, natural colours. No text, no logos, no blood.

## Decision: the axe (Rahul chose Option B, 7 Nov 2026)

The repo rule today is "no weapons in AI images". The UAE Attorney General says the weapon was the cockpit crash axe.

- **Option A (current rule):** the first officer stands behind the captain with his arm raised; the axe is never in frame, and the clip cuts away on the swing.
- **Option B:** the crash axe is visible in his hand, with no contact, no wound and no blood shown.

## Review round 1 (two independent reviewers, 7 Nov 2026): NOT READY

Findings both reviewers agreed on, plus the one disagreement resolved by checking the image:
- Only `closeup_b` passes. `attack_b`, `struggle_a`, `doorhand_a`, `doorhand_b` are mirrored (captain in the right seat). The model mirrors whenever the prompt names seats without saying where they appear in the frame.
- `enter_a/b`: two pilots calmly seated while the plumber enters. Impossible at that moment.
- `restrain_a/b`: forearm across the throat (policy risk); `restrain_b` gives the first officer four stripes.
- Panel drawn as an older 737 with six small screens and round gauges; a 737 MAX has four large landscape displays.
- The first officer is a different face in every shot. Fix with one reference image per character, taken from our own generated stills.
- Every still carries the Flow sparkle watermark in the bottom-right corner; the pipeline must crop it.
- Flow cannot "cut before contact": motion must keep the axe away from the captain for the whole clip, and avoid the words attack, hit, strike, swing, choke, drag, fight, wound, blood.
- Clip slots are 3.6–6 s, so the key action must happen in the first 4 s.
- Which way the 737 flight-deck door swings is not verified, so no shot shows the swing direction.

## Round 2 shots (stills free; reference images attached: captain from `closeup_b`, first officer from `restrain_a`)

Orientation words used in every cockpit still: "Camera looks FORWARD toward the windshield: the captain's seat is on the LEFT of the frame" or "Camera looks AFT toward the rear wall: the captain's seat appears on the RIGHT of the frame". Panel: "four large landscape-format displays in one row, no round gauges".

| # | File | Plays under | Still prompt (after the fixed description) | Motion prompt (8 s) |
| --- | --- | --- | --- | --- |
| 1 | `r_attack_behind` | 07 attack, "hamla kiya" | Camera at the closed rear door between the seat backs, looking FORWARD. Captain in the LEFT seat on the left of the frame, seen from behind and the side, both hands on the yoke. Right seat EMPTY. The first officer stands in the gap behind the captain's headrest (left-centre), holding a short red-handled crash axe at chest height, well away from the captain. | The standing man steps closer behind the seat and lifts the red tool slightly; the captain begins to turn his head. The tool never moves toward him; they stay apart. Red light blinks. Slow push-in. |
| 2 | `r_struggle_1` | Teaser; 07 attack | Same camera. Captain in the LEFT seat keeps his LEFT hand on the yoke and twists right, right forearm raised to block. The first officer leans over the captain's seat back from behind, the axe held high and back, not touching him. Right seat EMPTY. | Within 3 s the captain raises his open hand to keep him back, other hand on the yoke; the standing man leans in, the tool held away. The cockpit sways as if pitching down. Handheld. |
| 3 | `r_struggle_2` | 11 door, opening line | `closeup_b` (passed). | The captain grips the yoke tighter and leans forward against the hand on his shoulder; the hand stays on his shoulder. Red light blinks. No camera move. |
| 4 | `r_door_hand` | 11 door, "the door is right there" | Camera just behind the empty RIGHT seat, looking diagonally AFT and to the left. The closed grey door is in the left-centre of the frame in the rear wall. The captain has stood up out of the left seat and stands beside the door on the left of the frame, one hand pressing its lever handle, the other on his seat back, face strained. No wounds. | Within 2 s he presses the lever down with effort; the latch releases and a thin line of bright light appears at the door edge. He leans against the wall, exhausted. (The swing itself is not shown.) |
| 5 | `r_door_open` | 12 plumber | From the forward galley looking INTO the cockpit through the open rectangular door. Both seats EMPTY. The first officer (three stripes, hands empty) stands between the seats, half-turned toward the door. The captain sits slumped on the floor at the left edge of the doorway. The stocky bald passenger in a dark grey t-shirt, seen from behind three-quarters, steps through the doorway toward the first officer. | Within 3 s the passenger steps through and reaches both hands toward the standing man's shoulders; the standing man turns to face him. Handheld, one step behind. |
| 6 | `r_restrain` | 12 plumber, "bahar kheench liya" | From the forward galley looking toward the open cockpit door. The passenger is nearest the camera, back half to us, both arms wrapped around the first officer's CHEST from behind, pinning his upper arms; no arm near the neck. The first officer (three stripes) faces the camera in the doorway, tense, hands empty. Empty seats beyond. | Within 3 s both men step backward together out of the doorway into the galley, sway against the galley counter, then hold still. Handheld. |
| 7 | `r_galley_hold` | 13 dentist | Overhead view of the bright galley floor: the first officer (reference face, three stripes) face-down, face turned to the floor; the bald passenger kneels holding his arms; the dentist (light blue shirt) holds his legs. No other people, no props. | Very small movements: the men shift their weight and hold him still; the dentist looks up. Static overhead camera. |
| 8 | `r_takeover` | 14 landing, "controls sambhaale" | The same two pilots as `approach_b` (reference attached), seen from behind between the seats, camera looking FORWARD, cruise above white clouds. The right-seat pilot reaches to the overhead panel; the left-seat pilot has a hand on the yoke. | The right pilot flips two overhead switches; the left pilot settles his hand on the thrust levers. Calm, steady camera. |

Every motion prompt ends with: "No contact between the tool and anyone. No extra people appear. Camera stays where it is."

## Script timing changes from review (apply once clips are approved)

| Scene | Change |
| --- | --- |
| 01 teaser | dive at 0.20; `r_door_hand` (no flip) at 0.35 instead of `r_door_open`; aisle 0.51; aid 0.61; approach 0.71. |
| 07 attack | `cockpit_max` 0; `r_attack_behind` 0.38; `r_struggle_1` 0.68; drop `r_struggle_2` here. |
| 11 door | `r_struggle_2` 0 (tag CAPTAIN); `r_door_hand` 0.55, flip removed. |
| 12 plumber | `r_aisle` 0; `r_door_open` 0.18; `r_restrain` 0.50; `r_galley_hold` moves to 13. |
| 13 dentist | `r_galley_hold` 0; `r_aid` 0.60; drop `r_aid_close`. |
| 14 landing | map 0; `r_takeover` 0.33; `r_approach` 0.68; `r_apron` 0.86. |

## Clips already generated that stay

`r_aisle`, `r_aid`, `r_dive_1`, `r_dive_window`, `r_approach`, `r_apron` (all passed review; the apron clip is already in the project).

## Cost

Round 2 stills: free. Video for shots 1–8: 8 × 24 = 192 credits, only after both reviewers say READY and Rahul approves.

## Final decision after review rounds 2 and 3 (7 Nov 2026)

Rahul's direction: mostly still images, only a few animated moments.

| Moment | Used as | Source | Review |
| --- | --- | --- | --- |
| Attack from behind (teaser, hook, 07) | still | `flow_r2/attack_a3.jpg` (stripe fix of attack_a) | both PASS as a still |
| Struggle | dropped | `struggle_a3` rejected: three arms, a hand on the yoke | aviation REJECT |
| Hand on captain's shoulder (11) | still | `flow_fix/closeup_b.jpg` | both PASS |
| Captain at the door handle (teaser, 11) | still | `flow_r2/doorhand_b.jpg`, no flip | both PASS |
| Plumber enters (12) | still | `flow_r2/enter_b.jpg` | both PASS |
| Restraint (12) | still | `flow_r2/restrain_b.jpg` | PASS as a still |
| Galley hold (13) | still | `flow_r2/galley_b.jpg` | both PASS |
| First aid (teaser, 13) | still | `flow_day/aid_a.jpg` | PASS |
| Takeover (14) | still | `flow_r2/takeover_b.jpg` | both PASS |
| Aisle run, dive, tilted window, approach, apron | animated (existing clips) | `assets/ai/r_*.mp4` | start frames PASS; clips checked frame by frame |

Rejected clips from the first batch (struggle, yoke, door handle, door open, galley hold, takeover, first aid) stay archived in `assets/ai/flow_clips/` and are not used.

Pipeline fixes from round 3: Flow sparkle and Veo marks are blurred with `delogo` in `ai_assets.py` (no crop, framing unchanged); name tags render again on stills; tag positions and source-box positions corrected.

Known limits for the final cut: the panels are drawn as an older 737 layout, not the MAX's four large screens, and the crash axe is drawn hammer-like.

## Round 4: injured captain after the attack (Rahul, 7 Nov 2026)

Rahul asked to show the captain injured and bleeding from the back of the head in every shot after the attack. Restrained: blood on the back of the head, collar and hand, no open-wound close-ups. All are free still EDITS of already-approved images, so faces and layout stay the same.

| File | Base (approved) | Edit prompt |
| --- | --- | --- |
| `r_struggle_2` | `flow_fix/closeup_b` | Keep everything identical. Add a realistic injury: dark red blood matted in the hair at the back of the captain's head, running down the back of his neck onto his white collar, a few drops on his shoulder board. No open wound visible. |
| `r_door_hand` | `flow_r2/doorhand_b` | Keep everything identical. The captain is injured: blood matted in the hair at the back of his head, running down his neck and staining the back of his white collar and shirt; a smear of blood on the hand holding the lever. Pale, strained face. No open wound visible. |
| `r_door_open` | `flow_r2/enter_b` | Keep everything identical. The captain slumped at the doorway is injured: blood in his hair at the back of his head and down his neck, his white collar and shirt shoulder stained red, one hand pressed to the back of his head with blood on the fingers. No open wound visible. |
| `r_aid` | `flow_day/aid_a` | Keep everything identical. The captain is injured: blood stains on his white collar and the back of his neck from a head injury; the dentist presses the folded grey blanket to the back of the captain's head instead of his arm, a little blood soaking into it. No open wound visible. |

### Round 4 review result (7 Nov 2026): READY after three rounds

| File | Installed from | Round 1 | Fix applied | Final |
| --- | --- | --- | --- | --- |
| `r_struggle_2` | `flow_inj/closeup_inj2.jpg` | blood at temple, spatter | blood only behind the ear, one trickle, smear on knuckles | both PASS |
| `r_door_hand` | `flow_inj/doorhand_inj3.jpg` | too graphic (face, temple, big collar smear) | back of head only, soft collar stain, smear on hand | both PASS |
| `r_door_open` | `flow_inj/enter_inj3.jpg` | blood on forehead and face | face clean, neck smear, collar stain | both PASS |
| `r_aid` | `flow_inj/aid_inj2.jpg` | blanket at temple, collar blood on wrong side | blanket behind the head, right collar, fingertips | both PASS |

Not applied: the continuity reviewer asked to seat the first officer in `r_door_open`; kept standing, because he had left his seat for the attack and the plumber pulled him out from between the seats. All edits were free (Nano Banana); no paid video.

Rahul approved the four injured-captain stills on 7 Nov 2026.
