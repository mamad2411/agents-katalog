---
name: image-editing
description: Correct workflow for editing existing images on Hermes — AI-powered edits (Gemini Imagen 3) and PIL-based targeted edits (text/date swaps, logo overlays). For generating new images from scratch, use gpt-image-2 instead.
triggers:
  - edit this image
  - change the date
  - swap the background
  - replace text in an image
  - modify this photo
  - remove object from image
  - add text overlay
category: creative
---

# Image Editing on Hermes

## What This Skill Does

This skill Correct workflow for editing existing images on Hermes — AI-powered edits (Gemini Imagen 3) and PIL-based targeted edits (text/date swaps, logo overlays). For generating new images from scratch, use gpt-image-2 instead.

## Decision tree — which approach to use

```
Charles asks to edit an existing image
         │
         ▼
Is it a TARGETED TEXT/DATE change
(e.g. change date, swap a label, add a logo overlay)?
         │
   YES ──┴── NO
    │          │
    ▼          ▼
PIL-based   Gemini Imagen 3 (gemini-image-editor)
targeted    — background swaps, object removal,
edit        style changes, lighting adjustments
```

## Rule: Be honest with Charles about capabilities

**gpt-image-2 cannot edit existing images.** This is a hard API limitation:
- No `/images/edits` endpoint for gpt-image-2
- No reference image input on `/images/generations`
- The OpenAI Python SDK's `.images.edit()` only supports `dall-e-2`
- Charles explicitly uses **Gemini 2.5 Flash** for all image work (per his profile)

**What Charles said this session (2026-05-04):** "Use Google 3.1 Flash Preview" — this is the right model for AI-powered image editing on Hermes. The model `gemini-3.1-flash-preview` does not exist; the working name is `gemini-2.5-flash`.

---

## Approach 1: PIL Targeted Edit (date/text overlays)

**Use when:** Only text or a single element needs changing; the original image style is known; you need pixel-perfect preservation.

**This session's verified working pattern:**

```python
from PIL import Image, ImageDraw, ImageFont

# Load original — keep it untouched
img = Image.open("/root/.hermes/image_cache/img_eae64c391347.jpg")
w, h = img.size

# Find text region by scanning high-contrast bands
# (date text is usually in bottom 25% of thumbnail)
# Check pixel statistics to locate the text area

# Draw new text over the old date region
draw = ImageDraw.Draw(img)

# Use a bold sans-serif font that matches the thumbnail style
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)

# White fill, thick black stroke for readability
outline_color = (0, 0, 0)
fill_color = (255, 255, 255)

# Position where the date appears in the original
new_date = "April 27 - May 4"
x, y = 350, 620  # find exact position from original image analysis

# Stroke width 3-5px for bold outline
stroke_width = 4
draw.text((x, y), new_date, font=font, fill=fill_color,
          stroke_width=stroke_width, stroke_fill=outline_color)

img.save("/tmp/edited_output.png", quality=95)
```

**Key points:**
- Never modify the original — always work on a copy
- Match font size, color, and stroke style to the existing text
- Available fonts: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` (largest, best for thumbnails)
- For Canva-style clean fonts: `/usr/share/fonts/truetype/quicksand/Quicksand-Bold.ttf`
- If the image has a specific brand font you don't have, use PIL to sample the text color from the original region

**Finding the text position:**
```python
# Scan bottom portion for high-contrast (text) regions
for y in range(int(h*0.7), h, 20):
    band = img.crop((0, y, w, min(y+20, h)))
    stat = ImageStat.Stat(band)
    std = max(stat.stddev)  # High stddev = text/detail region
    print(f"y={y}: std={std:.1f}")
```

---

## Approach 2: Gemini Imagen 3 AI Edit

**Use when:** Background replacement, object removal, style changes, complex multi-element edits.

### Correct Python setup for Hermes (fixed)

```python
import sys, base64
sys.path.insert(0, '/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')
import google.genai as genai
from PIL import Image
import io

# Load API key
with open("/root/.hermes/.env") as f:
    for line in f:
        if line.startswith("GOOGLE_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break

genai.configure(api_key=api_key)

# Load and compress image (max 20MB API limit)
img = Image.open("/path/to/input.jpg")
buf = io.BytesIO()
img.save(buf, format='JPEG', quality=85)
image_data = buf.getvalue()

# Gemini 3 flash edit
model = genai.GenerativeModel('gemini-3-flash-preview')
response = model.generate_content([
    {'mime_type': 'image/jpeg', 'data': image_data},
    'Your precise edit instruction: exactly what to change, what to keep'
])

# Extract edited image from response
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        output = base64.b64decode(part.inline_data.data)
        with open("/tmp/edited.png", "wb") as f:
            f.write(output)
        print(f"Saved: {len(output):,} bytes")
```

### Common pitfalls

- **`import google.generativeai`** — WRONG. The installed package is `google.genai`.
- **`response.text()`** — WRONG. Edited images come back as `part.inline_data.data`.
- **No API key** — key is in `/root/.hermes/.env`, line `GOOGLE_API_KEY=...`
- **Image too large** — compress with PIL first, quality=85-90
- **michael venv broken** — use `/root/.hermes/hermes-agent/venv/bin/python3` for all Gemini scripts
- **Prompt too vague** — be specific: "change the date to April 27 - May 4, keep everything else identical"

### Prompt pattern for thumbnail date edit

```
"Edit this YouTube thumbnail image:
1. ONLY change the date text from current date to 'April 27 - May 4' — keep date in same position and style
2. Change the background to dark moody forest green gradient (#1a3d2e to #4a7c5a)
3. Keep ALL other elements exactly the same: the person's headshot, all text overlays, layout, composition"
```

---

## Skill state

**Pinned skills with incorrect docs (do not trust for this workflow):**
- `gpt-image-2` — claims to support edits; does not (API limitation)
- `gemini-image-editor` — has wrong import path (`google.generativeai`) and wrong model name

This `image-editing` skill is the authoritative reference for edit workflows on Hermes.

## Related skills

- `gpt-image-2` — image generation from scratch (not editing)
- `yt-thumbnail-creator` — YouTube thumbnail generation workflow
- `gemini-image-editor` — AI edit skill (correct capabilities, incorrect docs in SKILL.md)
