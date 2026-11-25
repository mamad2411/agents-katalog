---
name: google-ai-images
description: "Generate images with Google AI (Gemini & Imagen). Models: Gemini 3.1 Flash Image, Gemini 3 Pro Image, Imagen 4 Ultra/Standard/Fast. Capabilities: text-to-image, image editing, style transfer, ad creatives, social media visuals. Supports aspect ratios (1:1, 9:16, 16:9, 4:5, etc.), resolutions up to 4K, and batch generation. Use when: generate image, create visual, ad creative, static creative, banner, social media image, illustration, product mockup, image generation, gemini image, imagen, google ai image, text to image, create image with ai, midjourney alternative, dalle alternative"
allowed-tools: Bash(python3 *),Bash(pip install *),Bash(pip3 install *),Bash(open *)
---

# Google AI Image Generation

Generate images using Google's Gemini and Imagen models via the Google AI API.

## Setup

### 1. Install dependencies

```bash
pip3 install google-genai Pillow
```

### 2. Get API Key

Get your free API key from [Google AI Studio](https://aistudio.google.com/apikey).

```bash
export GEMINI_API_KEY="your-key-here"
```

## Available Models

### Gemini Models (generateContent) -- Recommended

| Model | Model ID | Best For |
|-------|----------|----------|
| Gemini 3.1 Flash Image | `gemini-3.1-flash-image-preview` | Fast, up to 4K, search grounding |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` | Highest quality, advanced reasoning |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Fast creative workflows |

### Imagen Models (predict) -- Dedicated image gen

| Model | Model ID | Best For |
|-------|----------|----------|
| Imagen 4 Ultra | `imagen-4.0-ultra-generate-001` | Highest quality |
| Imagen 4 Standard | `imagen-4.0-generate-001` | Standard quality |
| Imagen 4 Fast | `imagen-4.0-fast-generate-001` | Speed optimized |

## Key Differences

| Feature | Gemini | Imagen |
|---------|--------|--------|
| Input | Text + reference images | Text only |
| Output | 1 image per request | Up to 4 per request |
| Max resolution | 4K | 2K |
| Language | Multilingual (French OK) | English only |
| Image editing | Yes (pass reference images) | No |
| Aspect ratios | 14 options | 5 options |

## Parameters

### Gemini Parameters

| Parameter | Values |
|-----------|--------|
| `aspect_ratio` | `"1:1"`, `"9:16"`, `"16:9"`, `"4:5"`, `"5:4"`, `"4:3"`, `"3:4"`, `"3:2"`, `"2:3"`, `"1:4"`, `"4:1"`, `"1:8"`, `"8:1"`, `"21:9"` |
| `image_size` | `"512px"` (3.1 Flash only), `"1K"`, `"2K"`, `"4K"` |

### Imagen Parameters

| Parameter | Values | Default |
|-----------|--------|---------|
| `number_of_images` | 1-4 | 4 |
| `image_size` | `"1K"`, `"2K"` | `"1K"` |
| `aspect_ratio` | `"1:1"`, `"3:4"`, `"4:3"`, `"9:16"`, `"16:9"` | `"1:1"` |
| `person_generation` | `"dont_allow"`, `"allow_adult"`, `"allow_all"` | `"allow_adult"` |

## Common Ad Creative Sizes

| Format | Aspect Ratio | Use Case |
|--------|-------------|----------|
| Feed (Meta/Insta) | `1:1` | Posts, carrousel |
| Story/Reel | `9:16` | Stories, Reels, TikTok |
| Landscape | `16:9` | YouTube, banners |
| Portrait (Meta) | `4:5` | Feed optimized |

## Usage Patterns

### Pattern 1: Single Image (Gemini -- recommended)

```python
import os, base64
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents="YOUR PROMPT HERE",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="2K",
        ),
    ),
)

for i, part in enumerate(response.candidates[0].content.parts):
    if part.inline_data is not None:
        img_data = base64.b64decode(part.inline_data.data)
        with open(f"output_{i}.png", "wb") as f:
            f.write(img_data)
        print(f"Saved output_{i}.png")
```

### Pattern 2: Batch Generation (Imagen -- up to 4 images)

```python
import os, base64
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="YOUR PROMPT IN ENGLISH",
    config=types.GenerateImagesConfig(
        number_of_images=4,
        aspect_ratio="1:1",
        image_size="2K",
        person_generation="allow_adult",
    ),
)

for i, img in enumerate(response.generated_images):
    img.image.save(f"output_{i}.png")
    print(f"Saved output_{i}.png")
```

### Pattern 3: Image Editing (Gemini with reference)

```python
import os
from google import genai
from google.genai import types
from PIL import Image

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

ref_image = types.Part.from_image(Image.open("input.jpg"))

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=["Add bold white text overlay saying 'ATELIER GRATUIT'", ref_image],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="1:1"),
    ),
)

for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        import base64
        img_data = base64.b64decode(part.inline_data.data)
        with open("edited.png", "wb") as f:
            f.write(img_data)
```

### Pattern 4: Batch Ad Creatives Generator

Use this pattern to generate multiple ad creatives from a list of prompts and save them organized in folders.

```python
import os, base64, time
from google import genai
from google.genai import types
from pathlib import Path

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Configuration
MODEL = "gemini-2.0-flash-exp"
OUTPUT_DIR = Path("creatives")
ASPECT_RATIO = "1:1"  # Change per format: "9:16" for stories, "4:5" for feed
IMAGE_SIZE = "2K"

def generate_creative(prompt: str, filename: str, aspect_ratio: str = ASPECT_RATIO):
    """Generate a single ad creative and save it."""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=IMAGE_SIZE,
            ),
        ),
    )

    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            img_data = base64.b64decode(part.inline_data.data)
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"Saved {output_path}")
            return str(output_path)
    return None

# Example: Generate creatives for multiple ad angles
creatives = [
    {
        "prompt": "YOUR PROMPT 1",
        "filename": "angle1_feed.png",
        "aspect_ratio": "1:1",
    },
    {
        "prompt": "YOUR PROMPT 2",
        "filename": "angle2_story.png",
        "aspect_ratio": "9:16",
    },
]

for creative in creatives:
    generate_creative(
        prompt=creative["prompt"],
        filename=creative["filename"],
        aspect_ratio=creative.get("aspect_ratio", ASPECT_RATIO),
    )
    time.sleep(1)  # Rate limiting
```

## Prompting Tips for Ad Creatives

### Structure d'un bon prompt

```
[STYLE] + [SUJET PRINCIPAL] + [TEXTE A AFFICHER] + [AMBIANCE/COULEURS] + [COMPOSITION]
```

### Exemples de prompts pour Meta Ads

**Statement Ad (texte bold):**
```
Minimalist social media ad, dark gradient background (#1a1a2e to #16213e),
bold white sans-serif text centered saying "L'IA EST LA PLUS GRANDE OPPORTUNITE DE 2026",
subtle blue glow effect, clean modern design, no clutter,
professional marketing aesthetic
```

**Person + Context:**
```
Professional photo of a confident young man in his 30s working on a laptop
in a modern bright office, warm lighting, slight smile,
wearing smart casual clothing, shallow depth of field,
cinematic color grading, editorial photography style
```

**Before/After Split:**
```
Split image ad creative: left side shows a tired office worker in grey cubicle
(desaturated, cold tones), right side shows same person working freely
from a beautiful terrace with laptop (warm, vibrant colors),
bold arrow or dividing line in the center,
clean sans-serif text at bottom
```

**Data/Stats Visual:**
```
Clean infographic style ad, dark premium background,
large glowing number "50 000 EUR/mois" in bold gold text,
subtle AI circuit pattern in background,
small text below saying "Deviens Integrateur IA",
modern minimalist design, Meta ads format
```

## REST API (curl) -- Alternative without Python

### Gemini

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "YOUR PROMPT"}]}],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {"aspectRatio": "1:1", "imageSize": "2K"}
    }
  }' | python3 -c "
import sys, json, base64
r = json.load(sys.stdin)
for i, part in enumerate(r['candidates'][0]['content']['parts']):
    if 'inlineData' in part:
        with open(f'output_{i}.png', 'wb') as f:
            f.write(base64.b64decode(part['inlineData']['data']))
        print(f'Saved output_{i}.png')
"
```

### Imagen

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [{"prompt": "YOUR PROMPT IN ENGLISH"}],
    "parameters": {
      "sampleCount": 4,
      "aspectRatio": "1:1",
      "personGeneration": "allow_adult"
    }
  }' | python3 -c "
import sys, json, base64
r = json.load(sys.stdin)
for i, pred in enumerate(r.get('predictions', [])):
    with open(f'imagen_{i}.png', 'wb') as f:
        f.write(base64.b64decode(pred['bytesBase64Encoded']))
    print(f'Saved imagen_{i}.png')
"
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `API key not valid` | Check your key at https://aistudio.google.com/apikey |
| `SAFETY` block | Rephrase prompt, avoid violent/sexual content |
| `quota exceeded` | Wait or upgrade plan, Gemini free tier = 15 RPM |
| `model not found` | Check model ID spelling, some are in preview |
| Imagen returns empty | Prompt may have been filtered; try simpler prompt |
