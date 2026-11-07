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

## Shots to regenerate

| # | File | Scene, line | Still prompt (after the fixed description) | Motion prompt for the 8 s clip |
| --- | --- | --- | --- | --- |
| 1 | `r_attack_behind` | 07 attack, "hamla kiya" | Camera at the right side of the cockpit looking left and slightly back: the captain sits in the LEFT seat facing forward, hands on the yoke; the first officer has left the right seat and stands BEHIND the captain's seat, between the seats and the closed cockpit door, his arm raised (Option A: hand out of frame; Option B: holding a red-and-black crash axe). | The captain senses movement and starts to turn his head; the first officer's raised arm comes down toward him; cut before contact. Red master caution light starts flashing. Handheld, slight shake. |
| 2 | `r_struggle_1` | Teaser, 02 hook, 07 attack | From behind and between the seats looking forward: the captain in the LEFT seat keeps his left hand on the yoke and twists right, his right arm raised to block the first officer, who stands behind and above him between the seats. Red master caution light. | The captain fends him off with one arm while holding the yoke with the other; the first officer leans in; the horizon outside tilts as the nose drops. |
| 3 | `r_struggle_2` | 07 attack, close | Close over the captain's left shoulder in the LEFT seat: his hand grips the yoke, another man's hand grabs his right shoulder from behind; his face in profile, pained and determined; the PFD shows nose-down. | His grip tightens and he pulls back on the yoke; the hand from behind pulls at his shoulder; the caution light blinks. |
| 4 | `r_door_hand` | 11 door, "the door is right there" | Inside the cockpit, camera low near the first officer's seat looking BACK at the rear wall: the closed reinforced door directly behind the seats; the hurt captain has half-risen from the LEFT seat and reaches back with one hand to the door's lever handle. | He turns the handle; the door unlatches and swings backward into the bright galley; light floods in. |
| 5 | `r_door_open` | 11 door, 12 plumber | View from the forward galley looking INTO the cockpit through the open door: the two seats ahead, the windshield beyond; the stocky bald passenger in a dark grey t-shirt steps through the doorway into the cockpit. | He rushes in through the door toward the seats; the cockpit is bright with daylight. |
| 6 | `r_restrain` | 12 plumber | Forward galley just behind the open cockpit door: the stocky bald passenger holds the first officer from behind and pulls him back out through the doorway into the galley. | He pulls him two steps back into the galley; the first officer resists, then loses balance. (Kept calm and non-violent; the first wording was blocked by Flow.) |

## Clips that look right and stay (unless Rahul says otherwise)

| File | Clip | Why it can stay |
| --- | --- | --- |
| `r_aisle` | Plumber runs up the aisle | Cabin only; door at the front centre of the aisle. |
| `r_aid` | Dentist presses blanket on captain's arm | Galley only. |
| `r_dive_1` | Jet diving over desert | Exterior. Needs a check that it reads as a 737 MAX (split-tip winglets, two engines). |
| `r_dive_window` | Tilted window view | Cabin window only. |
| `r_takeover` | Off-duty pilots take the seats | Check: both are off-duty pilots, so the left and right seats are both plausible. |
| `r_approach` | Landing approach at Tabuk | Same check as the takeover. |
| `r_apron` | Jet on the apron | Exterior, not yet downloaded. |

## Cost

Six new stills: free. Six clips at 24 credits each: 144 credits. Each clip is shown to Rahul as a still first; the video is generated only after the still is approved.
