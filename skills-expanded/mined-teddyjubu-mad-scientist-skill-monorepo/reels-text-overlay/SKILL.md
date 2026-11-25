---
name: reels-text-overlay
description: Add AI voiceover and viral-style text overlays to short-form video clips (Reels, Shorts, TikTok). Use after generating or receiving a raw video clip when Charles wants to add narration and/or captions before posting. Covers OpenAI TTS voiceover generation, ffmpeg audio merge, and ffmpeg drawtext overlays in the viral Reels format (big bold white text, black stroke, timed reveals, orange brand accents).
---

# Reels Text Overlay & Voiceover Pipeline

Full production pipeline for taking a raw MP4 and turning it into a polished short-form clip with voiceover and text overlays.

## What This Skill Does

This skill Add AI voiceover and viral-style text overlays to short-form video clips (Reels, Shorts, TikTok). Use after generating or receiving a raw video clip when Charles wants to add narration and/or captions before posting. Covers OpenAI TTS voiceover generation, ffmpeg audio merge, and ffmpeg drawtext overlays in the viral Reels format (big bold white text, black stroke, timed reveals, orange brand accents).

## Prerequisites

- `ffmpeg` installed (available on this machine)
- Montserrat ExtraBold font installed at `/usr/share/fonts/Montserrat-ExtraBold.ttf`
  - If missing: `wget -q "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-ExtraBold.ttf" -O /usr/share/fonts/Montserrat-ExtraBold.ttf && fc-cache -f`
- OpenAI API key available in `/root/.hermes/profiles/eric/.env` as `OPENAI_API_KEY`

## Step 1 — Generate Voiceover (OpenAI TTS)

```python
import urllib.request, json

# Load key
with open("/root/.hermes/profiles/eric/.env") as f:
    for line in f:
        if line.startswith("OPENAI_API_KEY="):
            OPENAI_KEY = line.strip().split("=", 1)[1]
            break

script = "Your voiceover text here — keep it punchy for a 5-10 second clip."

payload = {
    "model": "tts-1-hd",
    "input": script,
    "voice": "onyx",   # Deep, confident male. Options: alloy, echo, fable, onyx, nova, shimmer
    "speed": 1.1       # Slightly faster for social — feels energetic
}

headers = {
    "Authorization": f"Bearer {OPENAI_KEY}",
    "Content-Type": "application/json"
}

req = urllib.request.Request(
    "https://api.openai.com/v1/audio/speech",
    data=json.dumps(payload).encode(),
    headers=headers,
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    audio_data = resp.read()

with open("/path/to/voiceover.mp3", "wb") as f:
    f.write(audio_data)
```

### Voice Guide
| Voice | Character |
|-------|-----------|
| `onyx` | Deep, authoritative male — good for authority/business content |
| `nova` | Warm, energetic female — good for lifestyle/REI content |
| `echo` | Balanced male — neutral, good for explainer style |

## Step 2 — Merge Voiceover with Video

```bash
ffmpeg -y \
  -i /path/to/video.mp4 \
  -i /path/to/voiceover.mp3 \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac \
  -shortest \
  /path/to/video-with-audio.mp4
```

`-shortest` cuts to the shorter of video/audio — prevents silent padding at the end.

## Step 3 — Add Text Overlays (Viral Reels Format)

### The Format (MrBeast / Hormozi style)
- Big hook text at top (first ~1.5s)
- Center reveal with brand name/product (middle)
- Supporting details in gold/accent color
- Power statement full-width
- CTA at bottom last second

### Charles's Brand Colors
- Primary orange: `#FF6B35`
- Gold accent: `#FFB627`
- White text with black 5px border — always

### ffmpeg drawtext Command

```bash
FONT="/usr/share/fonts/Montserrat-ExtraBold.ttf"
INPUT="/path/to/video-with-audio.mp4"
OUTPUT="/path/to/final.mp4"

ffmpeg -y -i "$INPUT" \
  -vf "
    drawtext=fontfile='$FONT':text='YOUR HOOK LINE':fontsize=46:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=80:enable='between(t,0,1.4)',
    drawtext=fontfile='$FONT':text='SECOND HOOK LINE':fontsize=46:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=140:enable='between(t,0,1.4)',
    drawtext=fontfile='$FONT':text='🤖 LABEL':fontsize=50:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=540:enable='between(t,1.5,3.4)',
    drawtext=fontfile='$FONT':text='PRODUCT NAME':fontsize=56:fontcolor='#FF6B35':borderw=5:bordercolor=black:x=(w-text_w)/2:y=600:enable='between(t,1.5,3.4)',
    drawtext=fontfile='$FONT':text='Supporting detail':fontsize=30:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=668:enable='between(t,1.5,3.4)',
    drawtext=fontfile='$FONT':text='Category • Category • Category':fontsize=26:fontcolor='#FFB627':borderw=3:bordercolor=black:x=(w-text_w)/2:y=708:enable='between(t,2.2,3.4)',
    drawtext=fontfile='$FONT':text='POWER STATEMENT — ALL CAPS':fontsize=34:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=1060:enable='between(t,3.5,4.6)',
    drawtext=fontfile='$FONT':text='🔗 LINK IN BIO':fontsize=38:fontcolor='#FF6B35':borderw=4:bordercolor=black:x=(w-text_w)/2:y=1150:enable='between(t,4.0,5.0)'
  " \
  -c:v libx264 -preset fast -crf 18 -c:a copy \
  "$OUTPUT"
```

### Y-Position Guide (720x1280 vertical canvas)
| Zone | Y range | Use for |
|------|---------|---------|
| Top hook | 80-200 | Opening hook text |
| Upper mid | 300-450 | Secondary hook |
| Center | 520-800 | Main reveal / product name |
| Lower mid | 900-1050 | Power statements |
| Bottom | 1100-1200 | CTA / "link in bio" |

### Font Size Guide
| Use | Size |
|-----|------|
| Main headline | 50-60px |
| Sub-headline | 42-50px |
| Body / supporting | 26-34px |
| CTA | 36-42px |

**Note:** First attempt used 72-88px for headlines — Charles flagged as "too big". Scaled down to ~56px for headlines, 30px body. These proportions look correct on a 720x1280 canvas.

## Timing Template (5-second clip)

| Time | Content |
|------|---------|
| 0.0–1.4s | Hook — question or bold statement |
| 1.5–3.4s | Reveal — product/solution name + details |
| 3.5–4.6s | Power statement |
| 4.0–5.0s | CTA |

Scale proportionally for longer clips (e.g., 10s clip: multiply all times by 2).

## Pitfalls

1. **Colon in drawtext text** — escape with `\:` or ffmpeg will error
2. **Emoji rendering** — simple emoji work (🤖 🔗) but complex ones may show as boxes; test first
3. **Long text wrapping** — ffmpeg drawtext does NOT auto-wrap; split into multiple drawtext filters manually
4. **`-shortest` is required** — without it, if voiceover is longer than video, ffmpeg freezes on last frame
5. **Font path must be absolute** — relative paths fail silently and produce no text
6. **CRF 18** = high quality. Use CRF 23 if file size is a concern (still looks great)
7. **`between(t,X,Y)` is inclusive** — slight overlap between segments is fine and looks natural

## Output Path Convention

```
/root/.openclaw/workspace/agents/eric/clips/YYYY-MM-DD/descriptive-name-final.mp4
```

Send to Charles via `MEDIA:/path/to/final.mp4` — plays inline in Telegram.
