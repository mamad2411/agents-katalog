---
name: arcads-video
description: Generate AI video ads using Arcads External API. Supports Sora 2, Veo 3.1, Kling 3.0, Grok Video, Seedance 2.0. Use when user wants to create video ads, promotional videos, product videos, or UGC-style videos.
---

# Arcads Video Ad Generator

Generate AI video ads via Arcads External API (`https://external-api.arcads.ai`).

## Setup Required

Add to `.env`:
```
ARCADS_API_KEY=your_key_here
```
Get API key at: https://app.arcads.ai/settings/api

## Supported Video Models

| Model | Best For | Cost |
|-------|----------|------|
| Seedance 2.0 | UGC-style, product showcase | ~0.06¢/sec |
| Kling 3.0 | Image-to-video, cinematic | medium |
| Grok Video | Fast turnaround, cheap | ~0.027¢/sec (cheapest) |
| Sora 2 / Sora 2 Pro | High quality, creative | medium-high |
| Veo 3.1 | Premium quality with audio | ~0.125¢/sec (most expensive) |

## API Endpoint

```
POST https://external-api.arcads.ai/v2/videos/generate
Authorization: Basic base64(API_KEY:)
```

## Mandatory Steps Before Generating

1. **Dialogue approval** — if video has speech, extract spoken lines, count words, confirm fit
2. **Credit cost estimate** — calculate and show cost breakdown, wait for user confirmation
3. **Generation count** — ask how many variations (default: 1)

## Example Request (Seedance 2.0)

```python
import requests, base64, os

api_key = os.getenv("ARCADS_API_KEY")
auth = base64.b64encode(f"{api_key}:".encode()).decode()

payload = {
    "model": "seedance-2-0",
    "prompt": "Professional product ad video...",
    "duration": 5,
    "aspectRatio": "9:16"
}

resp = requests.post(
    "https://external-api.arcads.ai/v2/videos/generate",
    json=payload,
    headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
)
data = resp.json()
video_id = data["id"]
```

## Polling for Result

```python
import time

# For Seedance: poll /v1/assets/{id}
# For others: poll /v1/videos/{id}
poll_url = f"https://external-api.arcads.ai/v1/assets/{video_id}"

while True:
    r = requests.get(poll_url, headers={"Authorization": f"Basic {auth}"})
    status = r.json().get("status")
    if status == "completed":
        print("Video URL:", r.json()["url"])
        break
    elif status == "failed":
        print("Failed:", r.json())
        break
    time.sleep(10)
```

## Critical Rules

- Presigned file URLs are **single-use** — re-upload for each generation
- Seedance: do NOT mix `referenceVideos` + `referenceImages` in same request
- Veo/Sora/Grok: currently reject image inputs — use Kling 3.0 or Seedance for image-to-video
- All errors on Seedance may still charge credits — retry carefully
- Save all output to `outputs/` folder with descriptive names

## Aspect Ratios

- `9:16` — Vertical (TikTok, Instagram Reels, Facebook Stories)
- `16:9` — Horizontal (YouTube, website banners)
- `1:1` — Square (Instagram feed, Facebook feed)

## File Organization

```
outputs/
  videos/
    YYYY-MM-DD/
      project-name-v1.mp4
      project-name-v2.mp4
logs/
  arcads-api.jsonl  ← log every API call here
```

## Pricing Reference

| Model | Per Second |
|-------|-----------|
| Grok Video | ~0.027¢ |
| Seedance 2.0 (img2vid) | ~0.06¢ |
| Seedance 2.0 (vid2vid) | ~0.10¢ |
| Sora 2 | ~0.08¢ |
| Kling 3.0 | ~0.09¢ |
| Veo 3.1 | ~0.125¢ |
