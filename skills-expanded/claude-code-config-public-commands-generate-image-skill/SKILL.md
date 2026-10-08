---
name: generate-image
description: Generate 2K images using Gemini 3 Pro API. Creates high-quality images from text prompts with various aspect ratios.
---

# Gemini 3 Pro Image Generator

Generate 2K resolution images from text prompts using Google's Gemini 3 Pro model (Nano Banana Pro).

## Quick Start

```bash
python ~/.claude/commands/generate-image/scripts/generate_image.py "A beautiful sunset over mountains" -o sunset.png
```

## Prompting Guide

Reference: [Nano Banana Pro Prompting Tips](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)

### Key Elements for Effective Prompts

Include these elements for nuanced creative control:

1. **Subject**: Who or what is in the image? Be specific
   - "a stoic robot barista with glowing blue optics"
   - "a fluffy calico cat wearing a tiny wizard hat"

2. **Composition**: How elements are arranged
   - "centered", "rule of thirds", "close-up", "wide shot"

3. **Action**: What is happening
   - "pouring coffee", "reading a book", "running through rain"

4. **Location**: Where the scene takes place
   - "in a neon-lit Tokyo alley", "on a misty mountain peak"

5. **Style**: Visual aesthetic
   - "photorealistic", "watercolor painting", "retro 80s poster"

### 7 Tips for Best Results

1. **Use Specific Details**: Combine subject, composition, action, location, and style in one prompt

2. **Leverage Real-World Knowledge**: Gemini 3 Pro understands real-world context - reference real places, products, or cultural elements

3. **Translate and Localize**: Generate text in multiple languages for international markets, posters, infographics

4. **Refine with Technical Terms**: Add camera angles, lighting conditions, text integration requirements

5. **Blend Multiple Concepts**: Combine ideas, translate images, generate visuals with embedded text

6. **Maintain Brand Consistency**: Apply designs with consistent styling, drape patterns/logos onto 3D objects while preserving lighting and texture

7. **Know the Limitations**: Complex text rendering and factual diagrams may need iteration

### Example Prompts

**Product Photography:**
```
"Professional product photo of a minimalist smartwatch on white marble surface,
soft studio lighting, slight reflection, centered composition, 8K detail"
```

**Marketing Banner:**
```
"Modern tech startup banner with text 'Innovation Starts Here',
gradient blue to purple background, geometric shapes, clean typography"
```

**Artistic Portrait:**
```
"Cinematic portrait of a jazz musician in a smoky club,
warm amber lighting, shallow depth of field, 1950s New York aesthetic"
```

## Options

- `-o, --output`: Output file path (default: generated_image.png)
- `-a, --aspect-ratio`: Aspect ratio (default: 16:9)
  - Square: 1:1
  - Portrait: 2:3, 3:4, 4:5, 9:16
  - Landscape: 3:2, 4:3, 5:4, 16:9, 21:9

## Examples

```bash
# 16:9 landscape image (default)
python ~/.claude/commands/generate-image/scripts/generate_image.py "Futuristic city skyline at night, cyberpunk aesthetic, neon lights reflecting on wet streets" -o city.png

# Square image for social media
python ~/.claude/commands/generate-image/scripts/generate_image.py "Flat lay of coffee and pastries on wooden table, morning light, cozy cafe aesthetic" -o product.png -a 1:1

# Portrait for mobile
python ~/.claude/commands/generate-image/scripts/generate_image.py "Fashion editorial, model in avant-garde outfit, dramatic studio lighting, high contrast" -o fashion.png -a 9:16
```

## Requirements

- Python 3.8+
- `GEMINI_API_KEY` in `~/.env`

## API Details

- **Model**: gemini-3-pro-image-preview (fixed)
- **Resolution**: 2K (fixed)
- **Endpoint**: Google Generative Language API v1beta
- **Output**: JPEG format

## Troubleshooting

### API Key Not Found
Ensure `~/.env` contains:
```
GEMINI_API_KEY=your_api_key_here
```

### Timeout Errors
The default timeout is 120 seconds. For complex prompts, the API may take longer.

### No Image in Response
Some prompts may be rejected by safety filters. Try rephrasing the prompt.
