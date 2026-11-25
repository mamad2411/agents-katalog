---
name: fal-ai-video-generation
description: Generate short-form AI videos (text-to-video) using fal.ai — Kling 1.6 and other models. Use when Charles asks for AI-generated video content, short-form clips, Reels, Shorts, or TikToks built from scratch without filming. FAL_KEY is available in /root/.openclaw/.openclaw/.env.
---

# fal.ai Text-to-Video Generation

Generate AI videos using fal.ai's hosted models (Kling, Minimax, etc.).

## What This Skill Does

This skill Generate short-form AI videos (text-to-video) using fal.ai — Kling 1.6 and other models. Use when Charles asks for AI-generated video content, short-form clips, Reels, Shorts, or TikToks built from scratch without filming. FAL_KEY is available in /root/.openclaw/.openclaw/.env.

## Credentials

- **FAL_KEY:** in `/root/.openclaw/.openclaw/.env` — `FAL_KEY=...`
- **Model used (verified):** `fal-ai/kling-video/v1.6/standard/text-to-video`

## Workflow

Generation is async — submit job, poll status, fetch result.

### Step 1 — Submit Job

```python
import urllib.request, json

FAL_KEY = "..."  # read from env
headers = {
    "Authorization": f"Key {FAL_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "Your video description here",
    "duration": "5",       # "5" or "10" seconds
    "aspect_ratio": "9:16" # "9:16" vertical, "16:9" landscape, "1:1" square
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    "https://queue.fal.run/fal-ai/kling-video/v1.6/standard/text-to-video",
    data=data, headers=headers, method="POST"
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    request_id = result["request_id"]
```

### Step 2 — Poll Status

```python
import time

status_url = f"https://queue.fal.run/fal-ai/kling-video/requests/{request_id}/status"
result_url = f"https://queue.fal.run/fal-ai/kling-video/requests/{request_id}"

for attempt in range(40):
    req = urllib.request.Request(status_url, headers={"Authorization": f"Key {FAL_KEY}"})
    with urllib.request.urlopen(req) as resp:
        status = json.loads(resp.read())

    if status["status"] == "COMPLETED":
        req2 = urllib.request.Request(result_url, headers={"Authorization": f"Key {FAL_KEY}"})
        with urllib.request.urlopen(req2) as resp2:
            result = json.loads(resp2.read())
        video_url = result["video"]["url"]
        break
    elif status["status"] in ("FAILED", "CANCELLED"):
        raise Exception(f"Job failed: {status}")

    time.sleep(15)  # Poll every 15 seconds — typical 5s clip takes ~3-4 min
```

### Step 3 — Download

```bash
curl -sL "{video_url}" -o /root/.openclaw/workspace/agents/eric/clips/YYYY-MM-DD/filename.mp4
```

## Timing

- 5-second clip: ~3-4 minutes generation time
- 10-second clip: ~5-7 minutes

## Default Save Path

```
/root/.openclaw/workspace/agents/eric/clips/YYYY-MM-DD/descriptive-name.mp4
```

## Prompt Tips for REI / Social Content

- Lead with visual style: "Dark background, orange glowing accents, cinematic..."
- Mention aspect ratio in prompt: "9:16 vertical format"
- For "Hermes Agent" branding: "futuristic AI control room with holographic screens showing real estate data"
- For social hooks: fast cuts, bold text overlays, tech aesthetic
- Avoid: people's faces (inconsistent), fast motion blur (compression artifacts)

## After Generation

Send directly to Charles via Telegram:
```
MEDIA:/path/to/video.mp4
```
MP4 files play inline in Telegram.

Then offer the full short-form production pipeline:
1. **Add voiceover** — OpenAI TTS (`tts-1-hd`, voice `onyx`) → ffmpeg merge (see `reels-text-overlay` skill)
2. **Add text overlays** — viral Reels format via ffmpeg drawtext (see `reels-text-overlay` skill)
3. **Post via Eric** — Blotato API to Instagram, TikTok, YouTube Shorts (draft mode by default)

## Pitfalls

1. **FAL_KEY location:** `/root/.openclaw/.openclaw/.env` — NOT `/root/.hermes/.env`
2. **Use `urllib` not `requests`** — `requests` lib may not be installed; `urllib` is stdlib
3. **Poll every 15 seconds minimum** — fal.ai queue can be slow; don't hammer it
4. **`duration` must be a string** (`"5"` not `5`) — int causes 422 error
5. **Video URL expires** — download immediately after completion, don't save just the URL
