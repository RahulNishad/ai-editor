# Flow regeneration pack: correct 737 MAX cockpit, brighter, with faces

Rahul's notes on the first direction video (7 Nov 2026): the images looked dark and far from the real incident, the cockpit was wrong, and AI-generated faces are fine to use.

These prompts replace the four cockpit shots that showed the wrong aircraft, and re-light the darkest scenes. Generate in Flow at 16:9, attach `assets/photos/cockpit_max.jpg` as the reference for every cockpit shot, and save each pick as `assets/ai/<file>.png`. The pipeline swaps it in on the next render.

## Rules for faces

- Faces are allowed. They must be **invented faces**: never try to look like the real captain, first officer, plumber, dentist or pilots, and never use their photos as references.
- Every image that shows the face of a named person is labelled **"AI RECONSTRUCTION · NOT THE REAL PERSON"** in the video.
- Still no blood, no wounds, no weapon close-ups, no airline logos or livery, no readable text.

## Add this to the end of every prompt

> Photorealistic documentary photograph, 35mm lens, natural colour, well exposed with clear detail in faces and the cockpit, soft practical light from the displays and overhead panel, no crushed blacks. Invented faces, not resembling any real person. No text, no logos, no blood.

## What a 737 MAX flight deck looks like

> Boeing 737 MAX 8 flight deck: four large landscape-format displays in one row across the main panel, a control column with a horn-shaped yoke in front of each pilot (no side-sticks), a central throttle pedestal with two thrust levers, a dense overhead panel with toggle switches, and a glareshield with the autopilot panel.

## The four cockpit shots

| File | Scene | Prompt |
| --- | --- | --- |
| `r_struggle_1` | Teaser, 02 hook, 07 attack | Inside a Boeing 737 MAX 8 flight deck at night, seen from between and slightly behind the two seats. The captain on the left, four gold stripes, and the first officer on the right, three gold stripes, grapple across the throttle pedestal, both turned three-quarters so their tense faces are partly visible. Red master caution light on the glareshield, the four displays bright. |
| `r_struggle_2` | 07 attack | Close shot over the captain's shoulder in a 737 MAX 8 cockpit: his hand grips the yoke hard while another arm pushes his shoulder; his face in profile, jaw clenched, lit red by the master caution light; the primary flight display beside him shows a nose-down attitude. |
| `r_takeover` | 14 landing | Inside a 737 MAX 8 cockpit in flight at night, dark sky and stars through the windshield: two off-duty pilots in plain white shirts without stripes take the seats, one gripping the yoke, the other reaching to the overhead panel, both focused, faces lit by the displays. |
| `r_approach` | Teaser, 14 landing | From behind and between the two seats of a 737 MAX 8 cockpit on final approach at night: runway approach lights in a flat dark desert ahead, both pilots' hands on the yoke and thrust levers, the four displays bright, faces seen in three-quarter profile. |

## Brighter versions of the darkest shots (optional)

| File | Prompt change |
| --- | --- |
| `r_door_open` | Same scene, but the cabin light is warm and bright and fills the flight deck; the passenger stepping in is lit from the front, face visible, determined. |
| `r_aisle` | Same scene with cabin lights on: passengers half-standing, worried faces turned toward the front; the plumber running toward the open cockpit door, seen from behind. |
| `r_galley_hold` | Same overhead scene under bright galley light; the faces of the passengers holding him are visible, the pinned man's face turned to the floor. |
| `r_aid` | Same scene, warm bright galley light; the dentist's face visible, calm and focused; the captain's face pale and tired, eyes half open. |
