---
name: openrouter-image-gen
description: Generate images using OpenRouter's API (Flux, Gemini, GPT-5 Image models). Use when the user asks to generate, create, or make an image, thumbnail, illustration, or visual.
---

# OpenRouter Image Generation

Generate images via OpenRouter's chat completions API. Requires `OPENROUTER_API_KEY` in your environment (e.g. `~/.env`, `~/.bashrc`, or exported in shell).

## Quick Start

```bash
curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash-image",
    "messages": [{"role": "user", "content": "YOUR PROMPT HERE"}],
    "modalities": ["image", "text"],
    "image_config": {
      "aspect_ratio": "16:9",
      "image_size": "1K"
    }
  }'
```

## Models (ranked by recommendation)

| Model | Cost | Best For |
|---|---|---|
| `google/gemini-2.5-flash-image` | Cheapest | General purpose, fast, good quality |
| `google/gemini-3.1-flash-image-preview` | Low | Extended aspect ratios, 0.5K size option |
| `google/gemini-3-pro-image-preview` | Mid | Higher quality Gemini |
| `black-forest-labs/flux.2-pro` | Mid | Photorealistic, artistic |
| `black-forest-labs/flux.2-max` | Mid | Highest quality Flux |
| `openai/gpt-5-image-mini` | Mid-high | GPT-level prompt following |
| `openai/gpt-5-image` | Expensive | Best prompt following + reasoning |
| `bytedance-seed/seedream-4.5` | Mid | ByteDance image gen |

**Default model**: `google/gemini-2.5-flash-image` (cheap + good). Use Flux for photorealism, GPT-5 Image for complex prompt following.

## Response Handling

Images come back as base64 data URLs in the response JSON:

```json
{
  "choices": [{
    "message": {
      "images": [{
        "type": "image_url",
        "image_url": {
          "url": "data:image/png;base64,iVBORw0KGgo..."
        }
      }]
    }
  }]
}
```

### Extract and save the image:

```bash
# Parse the base64 data URL from JSON response and save as PNG
echo "$RESPONSE" | jq -r '.choices[0].message.images[0].image_url.url' | sed 's|data:image/png;base64,||' | base64 -d > output.png
```

## Key Parameters

- **modalities**: `["image", "text"]` for multimodal models (Gemini, GPT-5), `["image"]` for image-only (Flux, Seedream)
- **aspect_ratio**: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`
- **image_size**: `0.5K` (Gemini 3.1 only), `1K` (default), `2K`, `4K`

## Image Editing (input an existing image)

Pass a source image as base64 in the user message content array:

```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Make the sky purple"},
    {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
  ]
}
```

## Tips

- For YouTube thumbnails, use `16:9` aspect ratio and `2K` or `4K` size
- Write detailed, specific prompts — describe composition, colors, style, mood
- For multiple variations, make multiple API calls with slightly different prompts
- Flux models are image-only output — use `"modalities": ["image"]`
- Always save the PNG locally before further processing
