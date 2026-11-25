---
name: arcads-youtube-thumbnail
description: Generate high-engagement YouTube thumbnails via Arcads Nano Banana 2 image API. Use when user wants YouTube thumbnail, A/B test variations, face-inclusive thumbnail, or branded thumbnail.
---

# YouTube Thumbnail Generator

Generate click-worthy YouTube thumbnails via Arcads Nano Banana 2.

## Prerequisites

- `.env` with `ARCADS_API_KEY`
- Reference files saved locally (NOT chat-pasted images)
- Organized folders:
  ```
  face/       ← 5+ angles of subject's face
  logos/      ← brand logo files
  products/   ← product images
  examples/   ← example thumbnails for style ref
  ```

## Cost

- Single generation: **24 credits**
- Batch of 6: ~144 credits
- Always present as estimates

## 5 Proven CTR Formulas

| Formula | When To Use |
|---------|-------------|
| Face + Text | Personal brand, reaction videos |
| Before/After | Tutorial, transformation content |
| Product Hero | Product review, unboxing |
| Curiosity Gap | "You won't believe..." style |
| Bold Stat | Data-driven, educational content |

## Workflow

1. Gather requirements: concept, subject, brand assets, text overlay, style
2. Verify disk references — STOP if missing (text descriptions alone won't work)
3. Estimate credits and confirm
4. Select CTR formula
5. Compose prompt with character likeness block
6. Generate via batch script
7. Rank results by CTR potential

## Critical Pitfalls

- Reusing file paths causes **HTTP 500** — always upload fresh references
- Minimum image size: **1080px** longest side
- Need **5+ face reference images** from different angles
- Small text garbles — use Nano Banana Pro for better text

## Aspect Ratio

`16:9` for YouTube thumbnails (1280×720px standard)

## Purpose
Generate YouTube thumbnails (incl. A/B variants) with Arcads Nano Banana 2.

## When NOT to use
- Video generation.

## Output requirements
Thumbnail images (variants) and the prompts used.
