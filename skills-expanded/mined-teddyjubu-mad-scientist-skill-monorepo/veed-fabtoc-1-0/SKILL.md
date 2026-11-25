---

name: Veed_Fabtoc_1.0
version: "1.0"
description: veed_fabtoc_1.0 lets the user create a talking video by combining one user-provided image with text and audio, which is useful when they want to produce a simple AI avatar-style video without complex video editing software or filming.
  Creates a talking video by combining one user-provided image file and one
  user-provided audio file using the fal AI model veed/fabric-1.0.
authoring_notes:
  - Display name: Veed_Fabtoc_1.0
  - Internally use the fal model endpoint: veed/fabric-1.0
  - Do not hardcode the fal API key in the skill file
  - Read the fal API key from the environment variable FAL_API_KEY
  - FAL_API_KEY is stored in /root/.openclaw/.openclaw/.env

---
Creates a talking/lip-sync video by animating a still image to match a spoken audio track using fal.ai's VEED Fabric 1.0 model.

## What This Skill Does

This skill veed_fabtoc_1.0 lets the user create a talking video by combining one user-provided image with text and audio, which is useful when they want to produce a simple AI avatar-style video without complex video editing software or filming.

## Requirements

- FAL_API_KEY set in `/root/.openclaw/.openclaw/.env` as `FAL_API_KEY=...`
- Python with `fal_client` SDK (v0.13+, already installed in Hermes venv)
- ffmpeg (for trimming long audio)

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| image_file | file | Yes | Source image to animate: jpg, jpeg, png, webp, gif, avif |
| audio_file | file | Yes | Speech/audio to drive lip-sync (mp3, wav, etc.) |
| resolution | string | No | `"720p"` (default) or `"480p"` |

## Errors

- Missing image → `"An image file is required."`
- Missing audio → `"An audio file is required."`
- Bad resolution → `"Resolution must be either 720p or 480p."`
- Generation failed → `"Video generation failed. Try again with a supported image/audio."`

## Workflow

### Step 1 — Validate

```python
import os, mimetypes

if not os.path.isfile(image_path):
    raise ValueError("An image file is required.")
if not os.path.isfile(audio_path):
    raise ValueError("An audio file is required.")
if resolution not in ("720p", "480p"):
    raise ValueError("Resolution must be either 720p or 480p.")
```

### Step 2 — Upload Files via fal_client SDK

The model handles full-length audio (60+ seconds works fine). No trimming needed.

```python
import fal_client

# upload_file works for both images and audio (path strings)
image_url = fal_client.upload_file(image_path)
audio_url = fal_client.upload_file(audio_path)
```

Note: `fal_client.upload_image()` requires a PIL Image object. Just use `upload_file()` for everything — it accepts file paths and works for any type.

### Step 3 — Submit and Poll (submit + raw HTTP status)

CRITICAL: Do NOT use `fal_client.subscribe()` (hangs for 10+ min with no feedback).
Do NOT use `fal_client.run()` (times out on long jobs).
Use `fal_client.submit()` for the request ID, then poll the raw HTTP status endpoint.

```python
import fal_client, json, time, urllib.request, os

# Load key
FAL_KEY = os.environ["FAL_API_KEY"]
auth = {"Authorization": f"Key {FAL_KEY}"}

# Submit — returns immediately with a request ID
handle = fal_client.submit(
    "veed/fabric-1.0",
    arguments={
        "image_url": image_url,
        "audio_url": audio_url,
        "resolution": resolution
    }
)
rid = handle.request_id
print(f"Request ID: {rid}")

# Poll the status endpoint every 10 seconds
status_url = f"https://queue.fal.run/veed/fabric-1.0/requests/{rid}/status"
result_url = f"https://queue.fal.run/veed/fabric-1.0/requests/{rid}"

MAX_POLLS = 120  # ~20 minutes max
for i in range(MAX_POLLS):
    time.sleep(10)
    
    req = urllib.request.Request(status_url, headers=auth)
    with urllib.request.urlopen(req, timeout=15) as resp:
        status = json.loads(resp.read())
    
    state = status.get("status", "unknown")
    
    if state == "COMPLETED":
        req2 = urllib.request.Request(result_url, headers=auth)
        with urllib.request.urlopen(req2, timeout=30) as resp2:
            result = json.loads(resp2.read())
        break
    elif state in ("FAILED", "CANCELLED"):
        raise RuntimeError(f"Job failed: {json.dumps(status, indent=2)}")
    # else: IN_PROGRESS — keep polling
else:
    raise TimeoutError("Job did not complete within 20 minutes")
```

### Step 5 — Extract Video URL

```python
video = result.get("video", {})
video_url = ""
if isinstance(video, dict):
    video_url = video.get("url", "")
elif isinstance(video, str):
    video_url = video
if not video_url:
    video_url = result.get("video_url", "")
```

### Step 6 — Download

```python
import urllib.request
if output_path and video_url:
    req = urllib.request.Request(video_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    with open(output_path, "wb") as f:
        f.write(data)
```

## Full Example

```python
import os, json, time, fal_client, urllib.request

def create_talking_video(image_path, audio_path, resolution="720p", output_path=None):
    if not os.path.isfile(image_path):
        raise ValueError("An image file is required.")
    if not os.path.isfile(audio_path):
        raise ValueError("An audio file is required.")
    if resolution not in ("720p", "480p"):
        raise ValueError("Resolution must be either 720p or 480p.")

    # Upload via fal_client SDK (works for any file type)
    image_url = fal_client.upload_file(image_path)
    audio_url = fal_client.upload_file(audio_path)

    FAL_KEY = os.environ["FAL_API_KEY"]
    auth = {"Authorization": f"Key {FAL_KEY}"}

    # Submit — get request ID
    handle = fal_client.submit(
        "veed/fabric-1.0",
        arguments={
            "image_url": image_url,
            "audio_url": audio_url,
            "resolution": resolution
        }
    )
    rid = handle.request_id

    # Poll raw HTTP status endpoint
    status_url = f"https://queue.fal.run/veed/fabric-1.0/requests/{rid}/status"
    result_url = f"https://queue.fal.run/veed/fabric-1.0/requests/{rid}"

    MAX_POLLS = 120
    for i in range(MAX_POLLS):
        time.sleep(10)
        req = urllib.request.Request(status_url, headers=auth)
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = json.loads(resp.read())
        state = status.get("status", "")
        if state == "COMPLETED":
            req2 = urllib.request.Request(result_url, headers=auth)
            with urllib.request.urlopen(req2, timeout=30) as resp2:
                result = json.loads(resp2.read())
            break
        elif state in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"Job failed: {status}")
    else:
        raise TimeoutError("Job did not complete within 20 minutes")

    # Extract video URL
    video = result.get("video", {})
    video_url = ""
    if isinstance(video, dict):
        video_url = video.get("url", "")
    elif isinstance(video, str):
        video_url = video
    if not video_url:
        video_url = result.get("video_url", "")

    # Download immediately (URLs expire)
    if output_path and video_url:
        req = urllib.request.Request(video_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        with open(output_path, "wb") as f:
            f.write(data)
        return {"local_path": output_path, "video_url": video_url}

    return {"video_url": video_url, "content_type": "video/mp4"}
```

## Usage

When the user provides exactly:
1. One image file (photo with a face works best)
2. One audio file (speech/voiceover)

Then:
- Animate the image to match the speech audio
- Use fal model `veed/fabric-1.0`
- Default to `720p` unless `480p` is requested
- Download immediately and deliver via Telegram as `MEDIA:/path/to/video.mp4`

## Pitfalls

1. FAL_API_KEY is in `/root/.openclaw/.openclaw/.env` — NOT `/root/.hermes/.env`
2. DO NOT use raw HTTP for file uploads (`queue.fal.run/fal.storage/upload` = 404). Always use `fal_client.upload_file(path)` — works for both images and audio.
3. DO NOT use `fal_client.subscribe()` — it silently hangs for 10+ minutes with no feedback, no timeout, no error.
4. DO NOT use `fal_client.run()` with tight timeouts — it uses subscribe() under the hood and will also hang/timed-out on longer jobs.
5. CORRECT approach: `fal_client.submit()` to get a request ID, then poll raw HTTP status endpoint `https://queue.fal.run/veed/fabric-1.0/requests/{rid}/status` every 10s.
6. Parameter name is `arguments=` not `input=` when using `fal_client.submit()`.
7. Audio length: the model handles full 60+ second clips fine. Tested 60s audio, generated ~55 MB video in ~11.5 minutes. No trimming needed — but long audio means longer generation time.
8. Image must contain a clear forward-facing photo with a visible face.
9. Audio should be clear speech — lip sync depends on it.
10. Response structure: `result["video"]["url"]` first, then `result.get("video_url")` as fallback.
11. Video URLs expire — download immediately.
12. `resolution` is a string — use `"720p"` not `720`.
13. Model endpoint is `veed/fabric-1.0` (not `fal-ai/veed/fabric-1.0`). Verified: returns 422 validation errors on bad params, not 404, so it exists.

## Default Save Path

```
/root/.openclaw/workspace/agents/eric/clips/YYYY-MM-DD/talking-video-DESCRIPTION.mp4
```

## HTTP API Reference

```
POST https://queue.fal.run/veed/fabric-1.0
Authorization: Key ${FAL_API_KEY}
Content-Type: application/json

{
  "input": {
    "image_url": "<uploaded-image-url>",
    "audio_url": "<uploaded-audio-url>",
    "resolution": "720p"
  }
}
```
