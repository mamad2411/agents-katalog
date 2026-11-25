---

name: nano-banana-image-gen
description: Generate images using Gemini 3.1 Flash (gemini-3.1-flash-image-preview) — the nano-banana model. Use for thumbnails, infographics, social graphics, and any image generation task. Always use this instead of the image_generate tool (FLUX). Supports reference image input for face/style matching.
tags: [image-generation, gemini, nano-banana, thumbnails, infographics, design]

---
Generates images using `gemini-3.1-flash-image-preview` (Google's Gemini 3.1 Flash image model — aka "nano-banana"). Always use this for image generation on Charles's system, never the `image_generate` tool (FLUX).

## What This Skill Does

This skill Generate images using Gemini 3.1 Flash (gemini-3.1-flash-image-preview) — the nano-banana model. Use for thumbnails, infographics, social graphics, and any image generation task. Always use this instead of the image_generate tool (FLUX). Supports reference image input for face/style matching.

## Key Facts

- **Model:** `gemini-3.1-flash-image-preview`
- **API Key:** `GOOGLE_API_KEY` from the environment; never paste the live key into this file.
- **Python env:** `/root/.hermes/hermes-agent/venv/bin/python3` (Python 3.11)
- **Package:** `google-genai` — install with `uv pip install google-genai` if missing
- **Template reference:** `/root/.openclaw/workspace/agents/michael/templates/nano_banana_2_template.py`

## CRITICAL: Python Environment

**Use the Hermes venv — NOT the openclaw michael venv.**

The openclaw michael venv uses Python 3.14 via a Homebrew symlink that is broken on this server:
```
/root/.openclaw/workspace/agents/michael/venv/bin/python3 → python3.14 (broken symlink)
```

Always run with:
```bash
/root/.hermes/hermes-agent/venv/bin/python3 your_script.py
```

## Basic Script (Text-to-Image)

```python
import os
import sys
sys.path.insert(0, '/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')

from google import genai
from google.genai import types

API_KEY = os.environ["GOOGLE_API_KEY"]
MODEL = "gemini-3.1-flash-image-preview"
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model=MODEL,
    contents="Your detailed image prompt here",
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
)

for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open("output.png", "wb") as f:
                f.write(part.inline_data.data)
            print(f"Saved output.png ({len(part.inline_data.data):,} bytes)")
```

## With Reference Image (Face/Style Matching)

Use this when generating thumbnails with Charles's headshot or any image-conditioned generation:

```python
import os
import sys
sys.path.insert(0, '/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')

from google import genai
from google.genai import types

API_KEY = os.environ["GOOGLE_API_KEY"]
MODEL = "gemini-3.1-flash-image-preview"
client = genai.Client(api_key=API_KEY)

# Load reference image
with open("/path/to/reference.jpg", "rb") as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model=MODEL,
    contents=[
        types.Content(parts=[
            types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_bytes)),
            types.Part(text="Your detailed prompt referencing the image...")
        ])
    ],
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
)

for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            with open("output.png", "wb") as f:
                f.write(part.inline_data.data)
            print(f"Saved ({len(part.inline_data.data):,} bytes)")
```

## Install google-genai (if missing)

```bash
# Check if installed
/root/.hermes/hermes-agent/venv/bin/python3 -c "from google import genai; print('OK')"

# Install if missing (pip not available — use uv)
cd /root/.hermes/hermes-agent && uv pip install google-genai
```

## Prompt Tips for Best Results

- Specify aspect ratio explicitly: "16:9 landscape, 1280x720"
- Specify dominant colors, mood, layout
- For thumbnails: "large bold all-caps text overlay", "high contrast", "NO watermarks, NO channel name"
- For infographics: list all sections with content, specify background color and accent colors
- Be specific about where the subject should appear (left, right, centered)

## Charles's Headshot Location

**Primary:** `/root/.hermes/image_cache/` — may contain session-cached headshots
**Fallback:** `/root/.openclaw/workspace/agents/mark/headshots/` — reliable saved headshots by hoodie color (black, blue, gray, green, orange, purple, red, white, yellow)
  - File naming: `{color}-hoodie-matrix-glasses.jpg`
  - Subject: **BALD** Black man (no hair), salt-and-pepper goatee, black-framed sunglasses with green Matrix code in lenses

The image_cache path may be stale or contain non-headshot images. Always check if the file exists before using it; fall back to the Mark headshots directory.

## Thumbnail Redesign Workflow (IMPORTANT)

When Charles asks to redesign an existing thumbnail with his headshot:
1. Load the existing thumbnail image from `/root/.hermes/image_cache/`
2. Load Charles's headshot from `/root/.hermes/image_cache/img_9370d1966831.jpg`
3. Prompt MUST specify:
   - Charles is BALD (no hair - this is critical, AI often adds hair)
   - RED hoodie (not orange, not brown)
   - Keep the ORIGINAL thumbnail's text overlays, colors, and layout EXACTLY
   - Only replace the subject's face/head with Charles's headshot
4. Output to `/root/thumbnails/`

Saved headshots by hoodie color: `/root/.openclaw/workspace/agents/mark/headshots/`
(black, blue, gray, green, orange, purple, red, white, yellow)

## Output Paths

- Thumbnails: `/root/thumbnails/`
- Infographics: `/root/thumbnails/` (or specify per task)

## Multi-Image Batch Generation

To generate multiple variations in one script (e.g. 3 thumbnail variations), loop over a list of dicts:

```python
variations = [
    {"filename": "v1.png", "hook": "HOOK TEXT 1", "prompt": "...prompt 1..."},
    {"filename": "v2.png", "hook": "HOOK TEXT 2", "prompt": "...prompt 2..."},
    {"filename": "v3.png", "hook": "HOOK TEXT 3", "prompt": "...prompt 3..."},
]

for var in variations:
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Content(parts=[
                types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_bytes)),
                types.Part(text=var["prompt"])
            ])
        ],
        config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
    )
    # save as above...
```

## YouTube Thumbnail Workflow (3 Variations)

Standard hook angles for Charles's channel:
- Hook 1 (Bold Warning): Urgency — "THE MAD SCIENTIST IS FURIOUS" — red/black, lightning
- Hook 2 (Gold Power): Wealth — "MAD GENIUS MONEY MOVES" — gold/black, luxury
- Hook 3 (Street Level): Education — "WHY THE MAD SCIENTIST SNAPPED" — balanced palette, urban

Always include in thumbnail prompts:
- Subject description: "Black man, salt-and-pepper goatee, brown hoodie, black-framed sunglasses with green Matrix code in lenses"
- "NO channel name, NO watermarks, NO branding text"
- "1280x720, 16:9 landscape, high contrast, readable at small sizes"

## Infographic Generation Workflow (VERIFIED April 2026)

**SEE ALSO:** The `data-infographic-generator` skill contains the full, reusable workflow for data-rich comparison infographics including research-first methodology. Use that skill when generating infographics with verified data.

### Quick Reference for Nano Banana Infographic Generation

#### Aspect Ratios

### Prompt Structure for Infographics
When generating infographics (especially 9:16 mobile format), use this structure:

```
1. Specify aspect ratio: "vertical infographic at 9:16 (1080x1920)"
2. Define ALL sections explicitly with their content:
   - "SECTION 1: [header] - [exact text]"
   - "SECTION 2: [header] - [exact text]"
   - etc.
3. List every product name, brand, or stat that must appear verbatim
4. Specify design style with exact colors (hex codes or descriptive names)
5. End with text rules: "ALL TEXT MUST BE SPELL-CORRECT AND REVERSIBLE"
```

### Section Layout Strategy
- Number sections top-to-bottom for clean reading flow
- Use headers in bold all-caps, body text in sentence case
- Ask for icon bullets or minimalist flat icons for each section
- Specify card-style sections with rounded borders for mobile readability

### Post-Generation Verification
- ALWAYS verify text with vision_analyze after generating
- Check for backwards/mirrored text — if found, regenerate with rephrased prompt
- The model renders text surprisingly well for infographics when content is explicit

## Pitfalls

- **Broken venv:** The openclaw michael Python 3.14 venv symlink is dead. Always use `/root/.hermes/hermes-agent/venv/bin/python3`
- **No pip:** `pip` and `pip3` are not available in the hermes venv. Use `uv pip install` instead
- **MIME type:** Pass `mime_type="image/jpeg"` even for JPG files; use `"image/png"` for PNGs
- **No image returned:** Check `response.text` for error messages; model may have refused the prompt — rephrase
- **FLUX is banned:** Never use the `image_generate` tool. Always use this nano-banana workflow
- **First attempt used FLUX:** Charles corrected this — always default to nano-banana, never image_generate

## Text Verification (CRITICAL for Thumbnails)

Gemini's image model sometimes produces **mirrored, reversed, or backwards text**. Always verify text legibility before delivering thumbnails to Charles:

1. After generating, use `vision_analyze` on the output image asking: "What text appears on this thumbnail? Is it readable and spelled correctly?"
2. If text is backwards or garbled, regenerate with a fresh prompt — sometimes re-running fixes it
3. If text fails repeatedly, try a different text layout in the prompt (e.g., shorter text, single line instead of multi-line, or different colors)
4. **Never deliver a thumbnail without verifying the text is correct** — backwards text is worse than no text and wastes Charles's time
