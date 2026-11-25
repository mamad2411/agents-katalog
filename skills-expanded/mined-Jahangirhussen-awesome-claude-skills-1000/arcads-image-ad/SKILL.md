---
name: arcads-image-ad
description: Generate Meta ad image creatives using Arcads API (ChatGPT Image 2 or Nano Banana models). Use for Facebook ads, Instagram ads, product images, UI mockups, chat screenshots, comparison tables.
---

# Arcads Image Ad Generator

Generate Meta ad image creatives via Arcads External API.

## Models Available

| Model | Best For |
|-------|----------|
| `gpt-image-2` | Typography-heavy: UI mockups, fake chat threads, comparison tables, editorial |
| `nano-banana-2` | Photoreal: lifestyle, handheld products, multi-image blending |
| `nano-banana-pro` | Character consistency, higher quality (costs more) |
| `nano-banana-edit` | Inpainting / editing existing images |

## Constraints

- Aspect ratios: `1:1`, `16:9`, `9:16` ONLY
- Max reference images: 5 (gpt-image-2), 14 (nano-banana)
- Model is LOCKED — never switch mid-task

## Workflow

1. **Preflight** — verify `.env` has `ARCADS_API_KEY`
2. **Input gathering** — prompt, model, aspect ratio, reference images
3. **Prompt rewrite** — match to template library
4. **Credit estimate** — confirm before generating
5. **Generate** — via Python script
6. **Visual QA** — check for text garbling, anatomy errors, brand accuracy
7. **Handoff** — pass to meta-ad-builder for deployment

## API Call

```python
import requests, base64, os

api_key = os.getenv("ARCADS_API_KEY")
auth = base64.b64encode(f"{api_key}:".encode()).decode()

payload = {
    "model": "nano-banana-2",  # or "gpt-image-2"
    "prompt": "Your ad prompt here",
    "aspectRatio": "1:1",
    "referenceImages": []  # optional: list of presigned URLs
}

resp = requests.post(
    "https://external-api.arcads.ai/v2/images/generate",
    json=payload,
    headers={"Authorization": f"Basic {auth}"}
)
print(resp.json())
```

## QA Checklist

- [ ] No garbled text
- [ ] No extra fingers/hands
- [ ] Brand colors correct
- [ ] Text readable at small sizes
- [ ] No merged faces/features

Regenerate up to 2x with refined prompts if issues found.

## Purpose
Generate Meta ad image creatives through the Arcads API (ChatGPT Image 2 or Nano Banana).

## When to use
The user wants ad images for Facebook/Instagram (product images, mockups, comparison tables).

## When NOT to use
- Video ads -> arcads-video.
- Publishing ads -> arcads-meta-ad-builder.

## Edge cases and failure handling
- Model output has garbled text -> regenerate with shorter text or use the other model.
- API error -> report the exact error.

## Example
```text
Product shot with headline overlay for a skincare serum, 1080x1080.
```

## Related skills
arcads-meta-ad-builder, arcads-video, nano-banana-image-ad
