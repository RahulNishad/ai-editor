# Google Flow image pack — FZ1073 reconstructions

Fifteen still images for the moments nobody filmed. The video cuts between two or three images per moment with slow camera moves and crossfades, so they play like footage.

Open Flow: https://labs.google/fx/tools/flow

## How to generate

1. **Aspect ratio 16:9** for every image.
2. **Make 4 variations** of each prompt and keep the most realistic one. Regenerate if hands, faces or cockpit details look wrong.
3. **Keep the characters consistent.** First generate the four "character" images below, then attach the right one as a reference (ingredient) when you make each scene image.
4. **Download** each picked image and **rename it exactly** as listed, e.g. `r_restrain.png`. PNG, JPG or WebP all work.
5. **Upload** all images here in one zip or as files. Any image you skip falls back to a real photo or the 3D version, so the video never breaks.

## Rules so the video stays professional and safe

- **No faces of the real people.** Captain, first officer, plumber, dentist and pilots appear from behind, in silhouette, cropped at the shoulders, or as hands. Real people must not be impersonated.
- **No blood, no weapons, no wounds.** Tension comes from light, framing and body language.
- **No airline logos or livery.** Plain white aircraft, plain cabin. The real flydubai photos stay as real photos elsewhere.
- **References:** only attach `cockpit_max.jpg` (CC BY 4.0, credited in the description) or images you generated yourself.
- **On YouTube upload:** answer "Yes" to *altered or synthetic content*. Each image is labelled "AI RECONSTRUCTION" in the video.

Add this to the end of **every** prompt:

> Photorealistic documentary photograph, shot on a full-frame camera with a 35mm lens at night, natural film grain, realistic low light, slight motion blur, high detail. No text, no logos, no faces visible, no blood.

## Step 1 — character references (not used in the video)

| Name | Prompt |
| --- | --- |
| `ref_captain` | Back view of an airline captain sitting in a cockpit seat, white short-sleeve uniform shirt with four gold stripes on the epaulettes, short black hair, headset around the neck. Face not visible. |
| `ref_firstofficer` | Back view of an airline first officer, white short-sleeve uniform shirt with three gold stripes on the epaulettes, short dark hair, slim build. Face not visible. |
| `ref_plumber` | Back view of a stocky man in his forties in a dark grey t-shirt and jeans, broad shoulders, shaved head, standing in an airliner aisle. Face not visible. |
| `ref_dentist` | Back view of a man in his thirties in a light blue casual shirt with rolled sleeves, kneeling. Face not visible. |

## Step 2 — the fifteen scene images

| File | Scene | Shot |
| --- | --- | --- |
| `r_struggle_1` | 01, 06 | Wide: struggle between the seats |
| `r_struggle_2` | 06 | Close: hands on the controls, red light |
| `r_dive_1` | 08 | Aircraft diving through clouds |
| `r_dive_window` | 08 | Tilted horizon through a cabin window |
| `r_door_hand` | 10 | Captain's hand on the door handle |
| `r_door_open` | 10 | Door opening, light flooding in |
| `r_aisle` | 11 | Passengers rushing up the aisle |
| `r_restrain` | 11 | Plumber pins the first officer |
| `r_galley_hold` | 11 | Several passengers holding him down |
| `r_aid` | 12 | Dentist presses a blanket to the captain's arm |
| `r_aid_close` | 12 | Close-up of hands and the blanket |
| `r_takeover` | 13 | Off-duty pilots take the seats |
| `r_approach` | 13 | Night approach to a desert runway |
| `r_apron` | 13 | Aircraft on the apron at dawn, emergency vehicles |
| `r_window_dawn` | 21 | Sunrise over the wing from a cabin window |

### r_struggle_1
Reference: `cockpit_max.jpg`, `ref_captain`, `ref_firstofficer`.
> Inside a Boeing 737 cockpit at night, seen from directly behind and between the two pilot seats. Red master warning lights glow on the glareshield. The captain on the left and the first officer on the right are grappling across the centre console, shoulders twisted, arms locked, both seats pushed back. Instrument displays glow blue and green, windshield black with faint stars.

### r_struggle_2
Reference: `cockpit_max.jpg`, `ref_captain`.
> Close-up inside a dark cockpit lit by flashing red warning light. A pilot's hand in a white uniform sleeve grips the control column hard while another arm pushes against his shoulder. The primary flight display beside it shows a steep nose-down attitude. Shallow depth of field, tense.

### r_dive_1
> A plain white twin-engine narrow-body airliner with no markings, nose pitched steeply down, diving through moonlit night clouds. Shot from a chase position above and to the side. Wingtip navigation lights red and green, cloud wisps streaking past, motion blur.

### r_dive_window
> View through an oval airliner cabin window at night, the horizon steeply tilted, clouds and the wing seen at a sharp angle, the window frame and seat back in the foreground slightly out of focus. Disorienting, dramatic.

### r_door_hand
Reference: `ref_captain`.
> Extreme close-up of a captain's forearm in a white short-sleeve uniform shirt with a gold-striped epaulette, his hand reaching for and gripping the metal handle of a cockpit door, trembling. Only flashing red emergency light. Face not in frame.

### r_door_open
> From inside a dark cockpit looking back at the cockpit door as it swings open, warm white cabin light flooding in through the doorway, the silhouette of a passenger already stepping forward. Strong backlight, dust in the air.

### r_aisle
Reference: `ref_plumber`.
> View down the aisle of a narrow-body airliner at night from mid-cabin looking forward. Cabin lights dimmed, passengers half-standing in their seats. At the front, the cockpit door is open with bright light pouring out, and a stocky man in a dark grey t-shirt is running toward it, seen from behind.

### r_restrain
Reference: `ref_plumber`, `ref_firstofficer`.
> In the cramped forward galley of an airliner, a stocky man in a dark grey t-shirt holds a slim man in a white pilot uniform shirt from behind in a firm chokehold and pulls him backward out of the cockpit doorway onto the galley floor. Both faces turned away from camera. Low warm light, galley carts, overhead panels. Chaotic, photojournalistic.

### r_galley_hold
Reference: `ref_plumber`, `ref_dentist`, `ref_firstofficer`.
> Overhead view of an airliner galley floor: a man in a white pilot shirt pinned face-down, a stocky man in a dark grey t-shirt kneeling on his back holding his arms, a second passenger in a light blue shirt holding his legs. Faces not visible. Harsh overhead cabin light.

### r_aid
Reference: `ref_dentist`, `ref_captain`.
> Inside an airliner galley, an injured captain in a white uniform shirt sits on the floor leaning against a galley cart, a man in a light blue shirt kneels beside him pressing a folded grey airline blanket firmly against the captain's forearm. Framed at chest height so no faces show. Calm, focused, warm light.

### r_aid_close
Reference: `ref_dentist`.
> Close-up of two hands pressing a folded grey airline blanket onto a forearm in a white uniform sleeve, a small yellow oxygen mask lying on the galley floor beside them. No blood, no wounds visible. Shallow depth of field.

### r_takeover
> From behind, two pilots in plain white shirts without stripes slide into the two cockpit seats of a Boeing 737 at night, one reaching for the control column, the other checking the overhead panel. Red light fading, instrument displays bright.

### r_approach
> View from behind two pilots through an airliner cockpit windshield on final approach at night: bright runway approach lights and a lit runway ahead in a flat dark desert. Instrument displays glow. Pilots are dark silhouettes.

### r_apron
> Wide shot at dawn of a plain white narrow-body airliner with no markings parked on a remote desert airport apron, surrounded by fire trucks and ambulances with flashing lights, airstairs at the front door, ground crew walking toward it. Soft orange sunrise, light dust.

### r_window_dawn
> View through an airliner cabin window at sunrise, the wing glowing orange, calm clouds below, a passenger's hand resting on the window frame. Peaceful, hopeful mood.
