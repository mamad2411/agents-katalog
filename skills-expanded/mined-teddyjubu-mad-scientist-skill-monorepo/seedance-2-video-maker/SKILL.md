---
name: seedance-2-video-maker
description: Generate videos using Seedance 2.0 via KIE.AI API - text-to-video, image-to-video, and multimodal reference-to-video with camera controls and audio generation
category: creative
---

# Seedance 2 Video Maker

Generate professional videos using ByteDance's Seedance 2.0 model through the KIE.AI API platform.

## What This Skill Does

This skill Generate videos using Seedance 2.0 via KIE.AI API - text-to-video, image-to-video, and multimodal reference-to-video with camera controls and audio generation.

## When to Use

- User wants to create a video from a text description (text-to-video)
- User wants to animate an image (image-to-video)
- User wants to create a video with reference frames (first/last frame control)
- User wants multimodal video with reference images, videos, and audio
- ANY video generation task involving Seedance 2

## API Details

- **Create Task Endpoint:** `POST https://api.kie.ai/api/v1/jobs/createTask`
- **Query Task Endpoint:** `GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId={taskId}`
- **Model Name:** `bytedance/seedance-2`
- **Auth:** `api-key: YOUR_KEY` (raw API key in header, no "Bearer" prefix)
- **API Key:** `066d348a94f6199a57e134ded5c579aa`
- **Key location:** `/root/.openclaw/.openclaw/.env` as `KIE_AI_API_KEY`

## Steps

### 1. Create the Video Task

Send a POST request to create the generation task:

```python
import urllib.request, json, time

data = json.dumps({
    'model': 'bytedance/seedance-2',
    # Optional: 'callBackUrl': 'https://your-server.com/callback',
    'input': {
        'prompt': 'Your detailed video description here (3-2500 chars)',
        'first_frame_url': 'https://example.com/first-frame.jpg',  # Optional - for image-to-video
        'last_frame_url': 'https://example.com/last-frame.jpg',     # Optional - for first&last frame mode
        'reference_image_urls': ['https://example.com/ref.jpg'],     # Optional - max 9 images
        'reference_video_urls': ['https://example.com/ref.mp4'],     # Optional - max 3 videos
        'reference_audio_urls': ['https://example.com/ref.mp3'],     # Optional - max 3 audios
        'return_last_frame': False,     # Optional - returns last frame as image
        'generate_audio': False,         # Optional - generates audio for video (higher cost)
        'resolution': '720p',            # 480p or 720p (default)
        'aspect_ratio': '16:9',          # 1:1, 4:3, 3:4, 16:9, 9:16, 21:9, adaptive
        'duration': 8,                   # 4-15 seconds
        'web_search': False              # Use online search for prompt context
    }
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.kie.ai/api/v1/jobs/createTask',
    data=data,
    headers={
        'Authorization': 'Bearer 066d348a94f6199a57e134ded5c579aa',
        'Content-Type': 'application/json'
    },
    method='POST'
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read().decode())
task_id = result['data']['taskId']
```

### 2. Poll for Task Completion

Use exponential backoff to check task status:

```python
import time

max_attempts = 30
base_delay = 10

for attempt in range(max_attempts):
    time.sleep(base_delay * (2 ** min(attempt, 3)))  # Max 80s between polls
    
    req = urllib.request.Request(
        f'https://api.kie.ai/api/v1/jobs/recordInfo?taskId={task_id}',
        headers={'Authorization': 'Bearer 066d348a94f6199a57e134ded5c579aa'}
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode())
    
    state = data.get('data', {}).get('state')
    
    if state == 'success':
        # Parse resultJson for video URLs
        result_json = json.loads(data['data']['resultJson'])
        video_urls = result_json.get('resultUrls', [])
        print(f"SUCCESS! Video URLs: {video_urls}")
        break
    elif state == 'fail':
        print(f"FAILED: {data['data'].get('failMsg', 'Unknown error')}")
        break
    elif state in ['waiting', 'queuing', 'generating']:
        print(f"Progress: {state} (attempt {attempt + 1})")
    else:
        print(f"Unknown state: {state}")
```

## Video Generation Modes

### Text-to-Video
Only provide a `prompt` - no input images needed.

### Image-to-Video (First Frame)
Provide `first_frame_url` + `prompt` to animate a static image.

### Image-to-Video (First & Last Frames)
Provide both `first_frame_url` AND `last_frame_url` to control start and end frames.

### Multimodal Reference-to-Video
Use `reference_image_urls`, `reference_video_urls`, and `reference_audio_urls` together. Note: These three modes CANNOT be used simultaneously.

## Important Notes

- **Prompt length:** Must be 3-2500 characters
- **Duration:** Videos are 4-15 seconds long
- **Resolution:** 480p is faster, 720p is higher quality
- **Audio:** Enabling `generate_audio` increases cost
- **URL Expiration:** Generated content URLs expire after ~24 hours - download immediately
- **Callbacks:** For production use, provide `callBackUrl` instead of polling
- **Max 3 reference videos:** Total duration of all reference videos must not exceed 15 seconds
- **Image requirements:** JPEG, PNG, WebP, BMP, TIFF, GIF - aspect ratio 0.4-2.5, 300-6000px, <30MB each
- **Video requirements:** MP4, MOV - 480p or 720p, 2-15s duration, <50MB each, 24-60 FPS
- **Audio requirements:** WAV, MP3 - 2-15s duration, <15MB each

## Known Issues

- **"generate playground failed, task id is blank":** Server-side error on KIE.AI platform. Retry after a few minutes. If persistent, the platform may be experiencing issues.
- **Double-encoded input:** The `input` field must be a proper JSON object, not a string. Test with Python's `json.dumps()` to ensure correct serialization.

## Error Codes

- **200:** Success
- **401:** Unauthorized - check API key
- **402:** Insufficient Credits
- **422:** Validation Error - check parameters
- **429:** Rate Limited
- **500:** Server Error
- **501:** Generation Failed

## Example Usage

```python
# Text-to-video example
response = create_seedance_video(
    prompt="A timelapse of a bustling city street at night with neon signs reflecting on wet pavement, cinematic lighting, smooth camera pan right",
    resolution="720p",
    aspect_ratio="16:9",
    duration=8,
    generate_audio=False
)

# Image-to-video example
response = create_seedance_video(
    prompt="The ocean waves start moving, clouds drift across the sky, and birds begin to fly",
    first_frame_url="https://example.com/beach-photo.jpg",
    resolution="720p",
    aspect_ratio="9:16",  # Vertical for TikTok/Reels
    duration=5
)
```