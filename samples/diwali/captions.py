"""Voice-synchronised on-screen transcript (mandatory since Nov 2026).

Word-level timings come from the voice track (faster-whisper, word_timestamps=True, Hindi). Each recognised word is
corrected against the recording script (text_dev) only where he actually said the script word; ad-libs follow the voice.
Words are grouped into short phrases (at most 7 words, broken at pauses and sentence marks) and written as an ASS file
in which every word-step is its own event, so the phrase builds up word by word and clears when its last word ends.
"""
import difflib, re

PUNCT = "।॥,.?!;:\"'“”‘’()-–—"
MAX_WORDS = 7
GAP = 0.55          # a pause this long starts a new phrase
HOLD = 0.18         # how long the finished phrase stays after its last word
FONT = "Kohinoor Devanagari"


def _norm(w):
    return re.sub(f"[{re.escape(PUNCT)}\\s]", "", w)


def tidy(words):
    """Whisper word-timing artefacts: a word repeated back to back within 0.35 s, and numbers split into fragments
    (" 26", " ,17", " ,215" -> "26,17,215")."""
    out = []
    for w in words:
        t = w["word"].strip()
        if not t: continue
        if out and _norm(t) and _norm(t) == _norm(out[-1]["word"]) and w["start"] - out[-1]["end"] < 0.35:
            out[-1]["end"] = w["end"]; continue
        if out and (t[0] in ",." and t[1:2].isdigit() or (t[0].isdigit() and out[-1]["word"][-1:] in ",.")):
            out[-1] = dict(out[-1], word=out[-1]["word"] + t, end=w["end"]); continue
        out.append(dict(w, word=t))
    return out


def correct(words, text_dev):
    """words: [{'start','end','word'}] from Whisper. Returns the same list with 'word' replaced by the script's spelling
    wherever the alignment says he spoke that script word; extra or changed words keep what Whisper heard."""
    words = tidy(words)
    rec = [_norm(w["word"]) for w in words]
    script = text_dev.split()
    scr = [_norm(s) for s in script]
    out = [dict(w, word=w["word"].strip()) for w in words]
    matched = [False] * len(out)
    sm = difflib.SequenceMatcher(None, rec, scr, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): out[i1 + k]["word"] = script[j1 + k]; matched[i1 + k] = True
        elif tag == "replace":
            # whole run first: Whisper splits or merges words ("चब भीस" for "छब्बीस"); if the run sounds like the script span,
            # take the span's words and share the run's time by character count
            rrun, srun = "".join(rec[i1:i2]), "".join(scr[j1:j2])
            if rrun and srun and difflib.SequenceMatcher(None, rrun, srun).ratio() >= 0.5 and abs(len(rrun) - len(srun)) <= max(4, len(srun) // 3):
                t0, t1 = words[i1]["start"], words[i2 - 1]["end"]
                total = sum(len(x) for x in scr[j1:j2]) or 1; acc = 0.0; new = []
                for j in range(j1, j2):
                    a = t0 + (t1 - t0) * acc / total; acc += len(scr[j]); b = t0 + (t1 - t0) * acc / total
                    new.append({"start": a, "end": b, "word": script[j]})
                out[i1:i2] = new; matched[i1:i2] = [True] * len(new)
                continue
            # else pair them up in order; accept the script word when the sounds are close enough
            for k in range(min(i2 - i1, j2 - j1)):
                if difflib.SequenceMatcher(None, rec[i1 + k], scr[j1 + k]).ratio() >= 0.45:
                    out[i1 + k]["word"] = script[j1 + k]; matched[i1 + k] = True
    # ad-libbed words follow the voice, but Whisper's spelling is not his: the script's own vocabulary first, then known slips
    vocab = {_norm(s): s.strip(PUNCT) for s in script}
    for i, w in enumerate(out):
        if matched[i]: continue
        key = _norm(w["word"])
        if key in FIXES:
            out[i]["word"] = FIXES[key]; continue
        best = max(vocab, key=lambda v: difflib.SequenceMatcher(None, key, v).ratio(), default=None)
        if best and len(key) >= 3 and difflib.SequenceMatcher(None, key, best).ratio() >= 0.8:
            out[i]["word"] = vocab[best]
    return out


# Whisper's usual Hindi slips on his voice (recognised -> what he says). Only applied to words the script does not contain.
FIXES = {"गर": "घर", "कवी": "कभी", "कभ": "कब", "जिक": "ज़िक्र", "जिक्र": "ज़िक्र", "आस्ता": "आस्था", "दिपाली": "दिवाली", "पव": "पर्व",
         "बीडियो": "वीडियो", "विडियो": "वीडियो", "इस्कोलर": "स्कॉलर", "दोनो": "दोनों", "इरानिन": "ईरानी", "हाचार": "हज़ार", "मनता": "मान्यता",
         "सुब": "शुभ", "सुप": "शुभ", "सरी": "सारी", "रोसनी": "रोशनी", "हल्दी": "हेल्दी", "दिपावली": "दीपावली", "दिपाओली": "दीपावली", "सेरेव": "सरयू", "सैरेव": "सरयू",
         "आयोद्ध्धा": "अयोध्या", "ऐयूध्या": "अयोध्या", "अध्यावासियों": "अयोध्यावासियों", "लाक": "लाख", "गाटो": "घाटों", "खातो": "घाटों", "तरब": "तरफ़",
         "मुख्ख": "मुख्य", "किस्णा": "कृष्ण", "किस्ना": "कृष्ण", "लच्मी": "लक्ष्मी", "देबी": "देवी", "समसते": "समझते", "समचते": "समझते", "सुर्वाद": "शुरुआत",
         "सुर्वात": "शुरुआत", "कामस्या": "अमावस्या", "कामस्स्या": "अमावस्या", "रीजन": "reason", "कम्पीट": "complete", "कंपीट": "complete",
         "इंपूर्टेंट": "important", "पहुतेंट": "important", "प्रोस्परस": "prosperous", "प्रोसपरस": "prosperous", "अस्थाइ": "अस्थायी", "दोखर्यां": "नौकरियाँ",
         "दंखर्यां": "नौकरियाँ", "कारवार": "कारोबार", "रूपय": "रुपये", "सम्रिदिकी": "समृद्धि की", "चटी": "छठी", "सत्वी": "सातवीं", "सतापदी": "शताब्दी",
         "क्योकि": "क्योंकि", "क्योकी": "क्योंकि", "निरवाडा": "निर्वाण", "अदेरा": "अँधेरा", "कीजिये": "कीजिए"}


def phrases(words):
    """Group corrected words into display phrases: break at pauses and sentence ends; when a phrase reaches MAX_WORDS,
    break at the last comma or small pause inside it rather than mid-thought."""
    out, cur = [], []
    def flush():
        if cur: out.append(list(cur)); cur.clear()
    for w in words:
        if cur:
            gap = w["start"] - cur[-1]["end"]
            ends = cur[-1]["word"][-1:] in "।?!."
            if gap > GAP or ends:
                flush()
            elif len(cur) >= MAX_WORDS:
                cut = None
                for k in range(len(cur) - 1, 2, -1):     # keep at least 3 words in the first part
                    if cur[k - 1]["word"][-1:] in ",;:" or cur[k]["start"] - cur[k - 1]["end"] > 0.22:
                        cut = k; break
                if cut and len(cur) - cut <= MAX_WORDS - 2:
                    out.append(cur[:cut]); del cur[:cut]
                else:
                    flush()
        cur.append(w)
    flush()
    # a one-word tail joins the previous phrase when they are close in time
    i = 1
    while i < len(out):
        if len(out[i]) == 1 and out[i][0]["start"] - out[i - 1][-1]["end"] < GAP and len(out[i - 1]) < MAX_WORDS + 2:
            out[i - 1] += out[i]; del out[i]
        else: i += 1
    return out


def _ts(t):
    t = max(0.0, t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ass(path, phr, offset=0.0, margin_v=170, size=92):
    """One ASS event per word-step: words[0..i] from word i start to word i+1 start; the full phrase holds briefly."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: T,{FONT},{size},&H00FFFFFF,&H00FFFFFF,&H00141414,&H96000000,-1,0,0,0,100,100,0,0,1,3.2,0,2,260,260,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for pi, p in enumerate(phr):
        nxt = phr[pi + 1][0]["start"] if pi + 1 < len(phr) else None
        for i, w in enumerate(p):
            a = p[i]["start"] + offset
            end = p[-1]["end"] + HOLD
            if nxt is not None: end = min(end, nxt - 0.02)      # never stack on the next phrase
            b = (p[i + 1]["start"] if i + 1 < len(p) else end) + offset
            if b - a < 0.04: b = a + 0.04
            text = " ".join(x["word"] for x in p[:i + 1])
            lines.append(f"Dialogue: 0,{_ts(a)},{_ts(b)},T,,0,0,0,,{text}")
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")
    return path


def srt_lines(phr, offset, start_index=1):
    """Proof-readable subtitles: one cue per phrase."""
    from make_long import srt_time
    out, i = [], start_index
    for p in phr:
        out.append(f"{i}\n{srt_time(p[0]['start'] + offset)} --> {srt_time(p[-1]['end'] + offset)}\n{' '.join(w['word'] for w in p)}\n"); i += 1
    return out, i
