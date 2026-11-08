# Sample: Diwali — "1,000 saal se bhi purani roshni"

A 4-minute (about 620 words) Diwali history-and-wishes video for Think With Rahul Nishad, built with the same pipeline as `samples/fz1073` (the Python, JS and HTML files here are copies; `node_modules` and `.venv` are symlinks to the fz1073 ones).

Written on Diwali day, 8 November 2026. 14 scenes: 4 with Rahul on screen (hook, reflection, wishes, plus two right-card scenes), 8 voice-only over photos and cards.

## Facts used on screen and in narration

| Claim | Status | How it is phrased | Source |
| --- | --- | --- | --- |
| Diwali (Lakshmi Puja) 2026 is Sunday 8 November; Dhanteras 6 Nov; Govardhan Puja 9 Nov; Bhai Dooj 10 or 11 Nov | Panchang; sources agree on 8 Nov, differ on the last two days | "Panchang ke mutabik"; card says "later dates vary by panchang" | [Dekho Panchang](https://dekhopanchang.com/en/festivals/diwali), [ePanchang](https://www.epanchang.com/blog/when-is-diwali-2026), [Time Out India](https://www.timeout.com/india/news/diwali-2026-when-is-dhanteras-diwali-and-bhai-dooj-110226) |
| Earliest textual references: Nilamata Purana (Kashmir) and Harsha's play Nagananda, 6th–7th century CE; Padma and Skanda Purana | Scholarly summary (P. K. Gode, 1945) | "Scholars ke mutabik" | [JSTOR Daily, A History of Diwali](https://daily.jstor.org/a-history-of-diwali) (opened) |
| Al-Biruni mentions the festival, c. 1030 CE | Scholarly summary | "Saal 1030 ke aas-paas" | JSTOR Daily (opened) |
| Seasonal/harvest explanation; scholars disagree on a single origin | Interpretation (a 1916 account quoted by Gode) | "Kai itihaaskaar maante hain", "ek purani vyakhya" | JSTOR Daily (opened) |
| Rama's return to Ayodhya; "deepavali" = row of lamps | Tradition | "Kaha jaata hai" | Ramayana tradition; JSTOR Daily |
| Lakshmi Puja; Naraka Chaturdashi (Krishna kills Narakasura); main Deepavali day in South India | Tradition / scripture | "Bhagavata Purana ke mutabik" | Bhagavata Purana book 10; Hobson-Jobson (1903) via JSTOR Daily |
| Jain: Mahavira's nirvana | Tradition | Stated as tradition; the 527 BCE date was dropped as unverifiable | JSTOR Daily (Gode: "2,400 years ago") |
| Sikh Bandi Chhor Divas: Guru Hargobind released from Gwalior Fort, 1619, with 52 kings | Tradition; prisoner count varies | "Kaha jaata hai, 52 rajaon ko" | [utsav.gov.in](https://utsav.gov.in/view-event/bandi-chhorh-diwas), [Religion News Service](https://religionnews.com/2023/11/10/bandi-chhor-divas-celebrated-at-diwali-has-a-history-and-values-of-its-own/) |
| Kali Puja in Bengal, Tihar in Nepal on the same nights | Common knowledge | Stated | Zee News, travel guides (weak); confirm before publishing |
| Ayodhya Deepotsav, 19 Oct 2025: 26,17,215 diyas on 56 ghats, drone-counted, Guinness World Record | Official (All India Radio) | Stated with the exact number | [newsonair.gov.in](https://www.newsonair.gov.in/uttar-pradesh-lights-26-lakh-diyas-sets-guinness-world-record-at-ayodhya) (opened), [Deccan Herald](https://www.deccanherald.com/amp/story/india%2Futtar-pradesh%2Fayodhya-deepotsav-new-world-record-with-2617-lakh-diyas-2128-people-performing-aarti-together-3769719) |
| Diwali 2025 trade ₹6.05 lakh crore (₹5.40 lakh crore goods + ₹65,000 crore services); 50 lakh temporary jobs | CLAIM: traders' body estimate | "CAIT ka daava hai", "sarkari aankda nahi"; card tagged CLAIM | [Business Today, 21 Oct 2025](https://www.businesstoday.in/india/story/diwali-2025-sales-hit-rs-605-lakh-crore-87-of-consumers-chose-indian-made-products-cait-report-499067-2025-10-21) (opened); [CAIT press release PDF](https://cait.in//images/press-release/pdf_1761808629.pdf) |

Deliberately left out: Diwali as a public holiday abroad and the New York school holiday (2023) — cut for length; the governor's release is at [governor.ny.gov](https://www.governor.ny.gov/news/governor-hochul-signs-legislation-making-diwali-school-holiday) if a longer cut wants it. Also left out: firecracker and pollution debates (a different video), and any comparison between faiths.

## Visuals

All real photos are from Wikimedia Commons (`assets/photos/`, credits in `CREDITS.md`): a diya close-up, Diwali lamps in West Bengal, Raja Ravi Varma's Lakshmi (PD), a 17th-century Malwa painting of Rama's return (PD), a 1775 Bhagavata Purana folio of Krishna at Naraka's citadel (PD, Cleveland Museum of Art), a 1470 Mahavira statue (CC0), the Golden Temple on Diwali, Kathmandu during Tihar, Diwali sweets, a rangoli. Spare: Gurdwara Data Bandi Chhor (Gwalior), Trafalgar Square Diwali.

Animation: see `FLOW_CLIP_PLAN.md`. Nothing is generated until the prompts pass the two-reviewer gate and Rahul approves them.

## Build

```bash
cd samples/diwali
python3 script_to_md.py script.long.json RECORDING_SCRIPT.md
.venv/bin/python storyboard.py
.venv/bin/python make_direction.py --work ~/Movies/diwali-direction --workers 4
.venv/bin/python make_long.py --takes ~/Movies/diwali-takes --work ~/Movies/diwali-build --workers 4
```

## Before publishing

1. Open each source above once more and confirm the on-screen numbers (especially the 26,17,215 count and the CAIT figures).
2. Paste `CREDITS.md` into the description.
3. If any AI illustration is used, tick "altered or synthetic content" in YouTube Studio.
