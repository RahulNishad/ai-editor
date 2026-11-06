# Google Flow prompt pack — FZ1073 reconstructions

Eight short clips for the moments nobody filmed. Generate them in Google Flow, download the MP4s, rename them exactly as listed, and upload them here. The video pipeline places them automatically.

## Settings for every clip

- **Model:** Veo 3 (Quality if your plan allows, otherwise Fast).
- **Aspect ratio:** 16:9. **Length:** 8 seconds.
- **Audio:** Any sound Veo adds is ignored. The pipeline uses your voice and its own music.
- **Best workflow:** First make a still with Flow's image tool and approve it. Then use **Frames to Video** with that still as the first frame. Stills are faster to judge and keep the look consistent.
- **Generate 2 to 4 variations** of each, keep the most realistic one.

## Rules so the video stays professional and safe

1. **No faces of the real people.** Captain, first officer, plumber, dentist and pilots are shown from behind, in silhouette, as hands, or out of focus. Real people must not be impersonated.
2. **No blood, no weapon close-ups.** Tension comes from light, motion and framing.
3. **No airline logos or livery** in reconstructed scenes. Plain white aircraft. The real flydubai photos stay as real photos elsewhere in the video.
4. **Reference photos:** only upload `assets/photos/cockpit_max.jpg` (CC BY 4.0, credit GeoMancer448 in the description) or public-domain images. Do not upload the CC BY-SA photos as references.
5. **Disclose on upload:** in YouTube Studio, answer "Yes" to *altered or synthetic content*. The video also labels each clip "AI RECONSTRUCTION".

Add this line to the end of every prompt:

> Photorealistic documentary reconstruction, shot on a full-frame cinema camera, 35mm lens, natural film grain, realistic low light, subtle handheld movement. No text, no logos, no faces visible, no blood.

## The eight clips

| File | Used in scene | What it shows |
| --- | --- | --- |
| `r_struggle.mp4` | 01 hook, 06 attack | Struggle between the pilot seats, red alarm light |
| `r_dive.mp4` | 08 plunge | Plain airliner diving through night clouds |
| `r_door_hand.mp4` | 10 door | Captain's hand pulling the cockpit door handle |
| `r_aisle.mp4` | 11 plumber | Door bursts open, passengers rush forward |
| `r_restrain.mp4` | 11 plumber | Passenger pins the first officer to the galley floor |
| `r_aid.mp4` | 12 dentist | Passenger presses a blanket to the captain's arm |
| `r_approach.mp4` | 13 landing | Night approach to a desert runway |
| `r_apron.mp4` | 13 landing | Aircraft on the apron at dawn, emergency vehicles |

### r_struggle.mp4
- **Mode:** Frames to Video, or Ingredients to Video with `cockpit_max.jpg` as the cockpit reference.
- **Prompt:** Inside a Boeing 737 flight deck at night, camera behind and between the two pilot seats. Red master warning lights flash on the glareshield. Two pilots in white short-sleeve uniform shirts suddenly grapple between the seats, shoulders and arms colliding, the seats shake. Instrument screens glow blue and green, the windshield is black with faint stars. Camera shakes, the horizon on the display tilts.
- **Avoid:** faces turning toward camera, weapons, blood.

### r_dive.mp4
- **Mode:** Text to Video.
- **Prompt:** A plain white twin-engine narrow-body airliner with no markings pitches nose-down and dives steeply through moonlit night clouds. Shot from a chase position slightly above and to the side. Clouds rush past, wingtip navigation lights blink red and green, heavy motion blur, the camera struggles to keep up.
- **Avoid:** airline logos, explosions, smoke, fire.

### r_door_hand.mp4
- **Mode:** Frames to Video.
- **Prompt:** Extreme close-up inside a dim cockpit lit only by flashing red emergency light. A pilot's forearm in a white short-sleeve uniform shirt with gold-striped epaulette reaches out, trembling, grabs the metal cockpit door handle and pulls hard. The door begins to swing open and warm cabin light spills across the hand. Shallow depth of field.
- **Avoid:** face in frame, blood, wounds.

### r_aisle.mp4
- **Mode:** Text to Video.
- **Prompt:** View down the aisle of a narrow-body airliner at night from mid-cabin, looking forward. Cabin lights dimmed, passengers in their seats. The cockpit door at the far end flies open and bright light floods out. Two men jump up from the front rows and rush toward it. Overhead bins, seat backs, motion blur. Camera pushes forward urgently.
- **Avoid:** recognisable faces, airline branding on seats.

### r_restrain.mp4
- **Mode:** Text to Video.
- **Prompt:** Cramped forward galley of an airliner, low warm light. A strong man in a casual dark t-shirt holds a man in a white pilot uniform shirt from behind in a firm hold and pins him down to the galley floor. Another passenger helps hold his arms. Seen from behind and above, faces turned away. Galley carts and overhead panels around them. Handheld, chaotic, fast.
- **Avoid:** faces, blood, punching, weapons.

### r_aid.mp4
- **Mode:** Text to Video.
- **Prompt:** Inside an airliner galley, an injured pilot in a white uniform shirt sits on the floor leaning against a galley cart. A passenger kneels beside him and presses a folded grey airline blanket firmly to his forearm, another hand holds a small oxygen mask nearby. Only hands, arms and torsos in frame. Calm, focused, warm cabin light.
- **Avoid:** blood, wounds, faces.

### r_approach.mp4
- **Mode:** Text to Video.
- **Prompt:** View from behind two pilots through an airliner cockpit windshield on final approach at night. Bright runway approach lights and a lit runway ahead in a dark, flat desert landscape. Instrument displays glow. The aircraft descends steadily, runway grows closer. The pilots are silhouettes.
- **Avoid:** faces, city skylines, mountains.

### r_apron.mp4
- **Mode:** Text to Video.
- **Prompt:** Wide shot at dawn of a plain white narrow-body airliner with no markings parked on a remote desert airport apron. Fire trucks and ambulances with flashing lights surround it, ground crew walk toward the aircraft, airstairs attached to the front door. Soft orange sunrise, light dust in the air, slow camera push-in.
- **Avoid:** airline logos, smoke, damage, crowds of journalists.

## Upload

Put the eight MP4 files in one zip, or attach them directly, and send them here. You can send them together with your recorded clips `01.mp4` to `23.mp4`, or separately. Missing reconstruction clips fall back to the real photos, so nothing breaks if one is not ready.
