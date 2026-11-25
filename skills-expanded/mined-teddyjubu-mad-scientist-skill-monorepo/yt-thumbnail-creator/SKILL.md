---

name: yt-thumbnail-creator
description: yt-thumbnail-creator lets the user create YouTube thumbnails designed to improve click-through rate by combining strong visual hierarchy, readable text, compelling composition, and topic-specific styling, so they can turn a video concept or title into a thumbnail that is built to compete in the feed instead of blending into it.

---
Automates creation of on-brand YouTube thumbnails for Charles Blair's real estate investing channel. Generates 3 high-impact thumbnail variations using Gemini Studio Nano Banana Pro.

## What This Skill Does

This skill yt-thumbnail-creator lets the user create YouTube thumbnails designed to improve click-through rate by combining strong visual hierarchy, readable text, compelling composition, and topic-specific styling, so they can turn a video concept or title into a thumbnail that is built to compete in the feed instead of blending into it.

## Workflow

### 1. Get Video Topic

Ask the user for the video topic or title. This will be used to generate relevant text hooks.

Example: "What's the topic or title of the video this thumbnail is for?"

### 2. Headshot — Already on Server

The headshot is already at `/root/.openclaw/.openclaw/workspace/charles-headshot-matrix.jpg`. Use this directly — do NOT ask the user for it.

If Charles specifically requests using a different photo, ask for it. Otherwise, always use the Matrix glasses headshot above.

### 3. Generate 3 Text Hooks

Based on the video topic and the style guide in `references/channel_style.md`, generate exactly **3 distinct, punchy text hook ideas** — one per thumbnail variation.

**Hook Requirements:**
- Maximum 5-7 words each
- Each hook must differ in angle:
  - Hook 1: Urgency/warning angle
  - Hook 2: Wealth/results angle
  - Hook 3: Education/how-to angle
- All caps for impact words
- Use numbers when relevant ("3 Ways", "$10K")

Read `references/channel_style.md` for style guidance.

**Do NOT ask the user to choose** — all three will be used automatically.

### 4. Generate 3 Thumbnail Variations

Use the **nano-banana Python script** to generate one thumbnail per hook. Each thumbnail uses a distinct visual style.

Read `references/prompt_templates.md` for the exact prompt structure.

**Generation Parameters:**
- Model: `gemini-3.1-flash-image-preview` via Google GenAI Python SDK
- Pass the user's headshot as a reference image (inline_data bytes)
- Use aspect ratio 16:9 (1280×720)
- Follow the variation-specific prompts from `references/prompt_templates.md`

**How to run (Python):**
```python
import os
import sys
sys.path.insert(0, '/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')
# google-genai must be installed: uv pip install google-genai (in hermes venv)

from google import genai
from google.genai import types

API_KEY = os.environ["GOOGLE_API_KEY"]
MODEL = "gemini-3.1-flash-image-preview"
client = genai.Client(api_key=API_KEY)

with open(headshot_path, "rb") as f:
    headshot_bytes = f.read()

response = client.models.generate_content(
    model=MODEL,
    contents=[
        types.Content(parts=[
            types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=headshot_bytes)),
            types.Part(text=prompt)
        ])
    ],
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
)

for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
```

**Run with:** `/root/.hermes/hermes-agent/venv/bin/python3 script.py`
(NOT the openclaw michael venv — that Python 3.14 symlink is broken on this server)

**Variation Mapping:**
- Variation 1 (Hook 1): Bold Warning style (red/black)
- Variation 2 (Hook 2): Gold & Black Power style (gold/black)
- Variation 3 (Hook 3): Street-Level Real Estate style (balanced palette)

**Critical Rules for Every Thumbnail:**
- The headshot subject MUST appear prominently with facial features matching the reference exactly
- **DO NOT include any name, channel name, watermark, or branding text**
- Text overlay must be large, bold, and readable at small sizes
- Color palette: red, yellow/gold, black, white — high contrast
- Output at 1280×720 (landscape, 16:9 aspect ratio)

Save outputs to:
- `./thumbnails/thumbnail_1.png`
- `./thumbnails/thumbnail_2.png`
- `./thumbnails/thumbnail_3.png`

Create the `thumbnails/` directory if it doesn't exist.

### 5. Deliver All 3 Variations

Send all three thumbnail images to the user simultaneously.

**For each thumbnail, include:**
- The image file
- Its hook text
- Its variation style name

Example format:
```
**Variation 1: Bold Warning**
Hook: "STOP Losing Money on This!"
[thumbnail_1.png]

**Variation 2: Gold & Black Power**
Hook: "How I Made $10K This Month"
[thumbnail_2.png]

**Variation 3: Street-Level Real Estate**
Hook: "3 Steps to Your First Deal"
[thumbnail_3.png]
```

## Bundled Resources

- **`references/channel_style.md`**: Visual style guide for the channel's thumbnails — variation definitions, color palettes, design rules
- **`references/prompt_templates.md`**: Prompt structure for generating thumbnails with Gemini Studio Nano Banana Pro — includes variation-specific prompts

## Image Generation — Use gpt-image-2 Skill

**CRITICAL UPDATE (2026-05-16):** Charles has moved his primary image generation to **OpenAI GPT Image 2** (`gpt-image-2`). This skill should be updated to use `gpt-image-2` for all thumbnail generation.

For thumbnails: load `gpt-image-2` skill and run its generation script directly. Do NOT use `image_generate` tool (FAL — out of credit) or nano-banana-image-gen (old Gemini fallback).

```bash
uv run /root/.hermes/skills/gpt-image-2/scripts/generate_image.py \
  --prompt "<full prompt>" \
  --filename /tmp/thumbnails/thumbnail_N.png \
  --size 1536x1024 \
  --quality high
```

Sizes: `1024x1024` (square), `1536x1024` (16:9 landscape, e.g. YouTube thumbnails), `1024x1536` (9:16 portrait).

After generation, deliver via `hermes-send-file "/tmp/thumbnails/thumbnail_N.png" "caption"` to Charles's Telegram DM.

## Legacy Reference (Gemini — DEPRECATED)

The following section documents the old Gemini-based workflow. Kept for reference only — do NOT use for new thumbnails.

### Old Workflow (DEPRECATED — Use gpt-image-2 Above)

~~Model: `gemini-3.1-flash-image-preview` via Google GenAI Python SDK~~
~~API Key: `GOOGLE_API_KEY` from `~/.hermes/.env`; never paste the live key into docs.~~

~~Run with: `/root/.hermes/hermes-agent/venv/bin/python3 script.py`~~

**Deprecated variation mapping (use gpt-image-2 instead):**
- Variation 1 (Hook 1): Bold Warning style (red/black)
- Variation 2 (Hook 2): Gold & Black Power style (gold/black)
- Variation 3 (Hook 3): Street-Level Real Estate style (balanced palette)

## Dependencies

- **Model**: `gpt-image-2` via OpenAI API (primary, current)
- **Python runtime**: Use `/root/.hermes/hermes-agent/venv/bin/python3` (Python 3.11)
- **Install google-genai if missing**: `uv pip install google-genai` (uv is available; pip/pip3 are NOT)
- **Reference template**: `/root/.openclaw/workspace/agents/michael/templates/nano_banana_2_template.py`
- **DO NOT use `image_generate` tool** (FAL — out of credit). Always use `gpt-image-2` skill.

## Face Preservation Guidance

Gemini `gemini-3.1-flash-image-preview` **re-interprets** reference faces rather than pasting them directly. It may alter glasses (add Matrix reflections, reshape frames), shift facial features, or change skin texture.

**Default approach: Try direct Gemini first** — pass the headshot as `inline_data` reference and generate all 3 variations directly. Charles often prefers or accepts the stylized result (confirmed successful across multiple sessions).

**If Charles requests exact face preservation** (especially with glasses), fall back to the Hybrid PIL Workflow below.

## Verification Step (CRITICAL — never skip)

Before delivering any thumbnail to Charles, ALWAYS verify the output:

```bash
# Use vision_analyze on each generated thumbnail:
# Ask: "What text appears on this thumbnail? Is it readable and spelled correctly? Any backwards or mirrored text?"
```

If text is garbled, backwards, or unreadable — regenerate with a fresh prompt (sometimes re-running fixes it) or try shorter text.

## Hybrid Approach — AI backgrounds + PIL compositing
Use when Charles needs his exact face preserved:
1. Use Gemini to generate decorative background elements only (no faces, no text)
2. Use PIL/Pillow to composite the exact unmodified headshot onto the background
Run with: `/root/.hermes/hermes-agent/venv/bin/python3 your_script.py`

## Hybrid PIL Workflow — Fallback for Exact Face Preservation

When the user explicitly needs their exact unaltered face on the thumbnail (not stylized by AI):

1. **Generate AI backgrounds** (decorative elements, gradients, shapes — NO faces, NO text)
2. **Use PIL to composite everything**: exact headshot + text overlays

```python
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1280, 720
headshot = Image.open(headshot_path).convert('RGBA')

# Generate backgrounds with Gemini (no faces, no text in prompts)
# Then composite with PIL:

def paste_face_with_stroke(face_img, bg, x, y, stroke_width=8, stroke_color=(255,255,255)):
    target_w = 380
    ratio = target_w / face_img.width
    target_h = int(face_img.height * ratio)
    scaled_face = face_img.resize((target_w, target_h), Image.LANCZOS)
    sw = stroke_width * 2
    bg.paste(Image.new('RGBA', (target_w+sw, target_h+sw), stroke_color), (x-stroke_width, y-stroke_width))
    bg.paste(scaled_face, (x, y), scaled_face)

def draw_outlined_text(draw, text, pos, font, fill_color, outline_color=(0,0,0), outline_width=8):
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx*dx + dy*dy <= outline_width*outline_width:
                draw.text((pos[0]+dx, pos[1]+dy), text, font=font, fill=outline_color)
    # Drop shadow
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 16:
                draw.text((pos[0]+dx+4, pos[1]+dy+4), text, font=font, fill=(0,0,0,180))
    draw.text(pos, text, font=font, fill=fill_color)

# Build thumbnail
bg = Image.new('RGB', (W, H), background_color)
draw = ImageDraw.Draw(bg)
paste_face_with_stroke(headshot, bg, face_x, face_y, stroke_width=10)
draw_outlined_text(draw, "TEXT HERE", (text_x, text_y), FONT_SIZE, text_color)
bg.save(output_path, quality=95)
```

## Pitfalls

- The michael venv (`/root/.openclaw/workspace/agents/michael/venv`) symlinks to a broken Python 3.14 path — use the hermes venv instead
- `pip` and `pip3` are not available — use `uv pip install google-genai` to add packages
- Always pass the headshot as `inline_data` in the same `Content` block as the prompt text
- The `response_modalities=["IMAGE", "TEXT"]` config is required or no image is returned
- Headshot background does NOT need to be pre-removed — Gemini handles compositing in the prompt
- **CRITICAL: Gemini DOES NOT truly composite faces.** When given a headshot as reference, the model *re-interprets* it rather than pasting it. This means glasses get altered (Matrix reflections added, frames reshaped), lenses become asymmetrical, bridges melt into skin, and facial features shift. This is a fundamental limitation of `gemini-3.1-flash-image-preview`.
- **If the user needs their exact face preserved (especially with glasses), use the Hybrid PIL Workflow below.**

## Hybrid PIL Workflow (Preserves Exact Face)

When Gemini's compositing mangles the face (common with glasses), fall back to this method:

### Step 1: Generate AI Backgrounds Only (no face, no text)

Prompt Gemini with backgrounds explicitly marked `NO PEOPLE, NO FACE, NO TEXT`. Generate 3 distinct backgrounds.

```
Generate a 16:9 YouTube thumbnail background design in MrBeast style.
NO PEOPLE, NO FACE, NO TEXT at all.
Bright red background with diagonal black shadow stripes...
```

### Step 2: Composite with PIL (Face + Text)

Use Pillow to paste the exact unaltered headshot and overlay text:

```python
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1280, 720

# Load headshot (exact, unmodified)
headshot = Image.open(headshot_path)
face = headshot.resize((480, int(headshot.height * 480 / headshot.width)), Image.LANCZOS)

# Load AI background
bg = Image.open(bg_path).resize((W, H)).convert('RGBA')

# Helper: paste with white stroke
def paste_with_stroke(img, pos, bg, stroke_width=8):
    sw, sh = img.size
    mask = Image.new('L', (sw + stroke_width*2, sh + stroke_width*2), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0,0), mask.size], radius=30, fill=255)
    stroke = Image.new('RGBA', mask.size, (255,255,255))
    canvas = Image.new('RGBA', mask.size, (0,0,0,0))
    canvas.paste(stroke, mask=mask)
    face_mask = Image.new('L', img.size, 0)
    draw2 = ImageDraw.Draw(face_mask)
    draw2.rounded_rectangle([(0,0), img.size], radius=20, fill=255)
    img_rgba = img.convert('RGBA')
    temp = Image.new('RGBA', img.size, (0,0,0,0))
    temp.paste(img_rgba, (0,0), face_mask)
    canvas.paste(temp, (stroke_width, stroke_width), temp)
    bg.paste(canvas, (pos[0]-stroke_width, pos[1]-stroke_width), canvas)

# Paste face on left (MrBeast style)
paste_with_stroke(face, (20, (H - face.height) // 2), bg)

# Add outlined text
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 92)
def draw_outlined_text(draw, text, pos, font, fill, outline=(0,0,0), width=8):
    for dx in range(-width, width+1):
        for dy in range(-width, width+1):
            if dx*dx + dy*dy <= width*width:
                draw.text((pos[0]+dx, pos[1]+dy), text, font=font, fill=outline)
    draw.text(pos, text, font=font, fill=fill)

draw = ImageDraw.Draw(bg)
draw_outlined_text(draw, "ONE-CLICK", (560, 120), font, (255,255,255), width=8)
draw_outlined_text(draw, "REHAB", (560, 240), font, (255,220,0), width=8)
draw_outlined_text(draw, "ESTIMATOR", (560, 360), font, (255,255,255), width=8)

bg.convert('RGB').save(output_path, quality=95)
```

**Why this works:** The headshot is never sent to the AI — it's loaded directly and pasted as a real image. The AI only generates the background (where it excels), and PIL handles the face (where the AI fails).

### Available Fonts
- `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` — DejaVu Sans Bold (largest, best for thumbnails)
- Check other locations: `/usr/share/fonts/truetype/liberation/`, `/usr/share/fonts/google-noto/`

## Delivery Notes

- `hermes-send-file` always sends to Charles's Home channel (597734298), NOT the current DM/chat.
- To deliver images directly in the current Telegram DM, use `MEDIA:/absolute/path/to/file.png` in responses.
- For PDF reports, use `hermes-send-file "/path" "caption"` (Home channel is correct for reports).

## Multiple Title Variations Workflow

When Charles asks for thumbnails for multiple titles (not the default 3 variation set):
- Generate ONE thumbnail per title (not 3 per title)
- Each thumbnail should match the title's theme/style (e.g., Augusta theme for Augusta-related titles)
- Verify every thumbnail with `vision_analyze` before delivery — ask "What text appears? Is it readable? Any backwards text? Are Matrix glasses visible?"
- Deliver all at once via `MEDIA:/path` to the current chat
