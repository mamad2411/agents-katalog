---
name: chatgpt-image
description: This skill generates images using OpenAI's gpt-image-2 model. Use when users ask to generate photorealistic images, product photos, diagrams, mockups, brand-safe illustrations, or business graphics. Trigger phrases include "chatgpt image", "openai image", "photorealistic image", "product photo", "diagram", "mockup", "brand-safe image".
---

# ChatGPT Image Generation Skill

Generate images using OpenAI's gpt-image-2 model (released April 2026) — optimized for photorealism, instruction-following, near-perfect text rendering, and business-ready assets. Uses O-series reasoning to research, plan, and self-check before rendering. Supports up to 2K natively and 4K with custom dimensions.

## Setup

Requires `OPENAI_API_KEY` env var and `uv` (Python script runner). See [`docs/SETUP_OPENAI.md`](../../docs/SETUP_OPENAI.md) for the full walkthrough (API key creation, billing, env setup).

For Nolty to reach for this skill when the user asks "generate an image" or "draw X", make sure your `TOOLS.md` has the image-generation row pointing at this skill (the shipped `TOOLS.template.md` already includes it).

## Model Strengths

**Best for:**
- **Photorealism** - Skin, fabric, glass, metal render correctly. Lighting instructions stick.
- **Precise instruction following** - Spatial layouts, cutaways, exploded views, ordered elements
- **Brand-safe illustration** - Flat styles with palette discipline, cohesive icon sets
- **Text in images** - Short headlines are legible, good for posters/covers/slides
- **Style transfer** - Applies styles without breaking anatomy or subject identity
- **Business mockups** - Stakeholder-ready visuals, faster than stock + Photoshop

**Limitations:**
- Hands under extreme poses can fail
- Tiny dense text on labels may drift
- Long paragraphs of text will have errors
- No trademark awareness - human review needed for logos

## Usage

When the user requests an image, run this Python script using `uv run`:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///

import base64, os, requests, sys
from datetime import datetime

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Parse arguments
prompt = sys.argv[1] if len(sys.argv) > 1 else "A simple test image"
size = sys.argv[2] if len(sys.argv) > 2 else "1024x1024"
output_path = sys.argv[3] if len(sys.argv) > 3 else f"{datetime.now().strftime('%Y%m%d')}-openai-output.png"

print(f"Generating image with OpenAI gpt-image-2...")
print(f"Prompt: {prompt}")
print(f"Size: {size}")

resp = requests.post(
    "https://api.openai.com/v1/images/generations",
    headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
    json={
        "model": "gpt-image-2",
        "prompt": prompt,
        "size": size
    },
    timeout=120
)
resp.raise_for_status()
b64 = resp.json()["data"][0]["b64_json"]
with open(output_path, "wb") as f:
    f.write(base64.b64decode(b64))
print(f"Wrote {output_path}")
```

## Size Options

Parse size from user request:
- `1024x1024` - Square (default)
- `1536x1024` - Landscape (wide)
- `1024x1536` - Portrait (tall)
- `auto` - Let model choose

User phrases to detect:
- "landscape", "wide", "horizontal" → `1536x1024`
- "portrait", "tall", "vertical" → `1024x1536`
- "square" or no mention → `1024x1024`

## Output Naming

**Marketing content mode** (when working on a post file like `20251218 - Article Title.md`):
- Match the article naming: `20251218 - Article Title - 1.png`
- Increment number for additional images: `- 2.png`, `- 3.png`
- Save in the same folder as the `.md` file
- Check existing files to determine next number

**General mode** (standalone generation):
- Format: `YYYYMMDD-openai-[short-desc].png`
- Save in current working directory
- Extract 2-4 word description from prompt
- Example: `20251218-openai-raccoon-figurine.png`

## Workflow

1. Parse the user's prompt and any size preferences
2. Determine output path based on context (marketing article or general)
3. Write the Python script to a temp file
4. Run with `uv run script.py "prompt" "size" "output_path"`
5. Display the generated image to the user

## Example Prompts That Work Well

**Product photography:**
```
Studio product photo of a matte black ceramic raccoon figurine on a white-to-light-gray seamless background, softbox lighting, 85mm lens look
```

**Diagrams:**
```
Clean exploded view diagram of a smartphone showing internal components, technical illustration style, white background, labeled parts
```

**Marketing graphics:**
```
Flat illustration of a robot and human shaking hands, corporate blue color palette, minimal style, suitable for business presentation
```

**Posters with text:**
```
Modern conference poster with headline "AI Summit 2025" at top, abstract geometric shapes in blue and orange, professional corporate design
```
