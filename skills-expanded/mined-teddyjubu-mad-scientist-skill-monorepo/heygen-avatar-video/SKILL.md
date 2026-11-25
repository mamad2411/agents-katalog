---

name: heygen-avatar-video
description: heygen-avatar-video lets the user generate AI avatar talking-head videos using Charles Blair's custom HeyGen avatar, which is useful when they want to create UGC-style content for TikTok, Reels, or YouTube without filming, produce consistent on-brand video content at scale, or quickly turn a script into a finished talking-head video.

---
Generate AI avatar videos using Charles Blair's pre-built HeyGen avatar. Produces 9:16 vertical talking-head videos suitable for TikTok, Instagram Reels, and YouTube Shorts.

## What This Skill Does

This skill heygen-avatar-video lets the user generate AI avatar talking-head videos using Charles Blair's custom HeyGen avatar, which is useful when they want to create UGC-style content for TikTok, Reels, or YouTube without filming, produce consistent on-brand video content at scale, or quickly turn a script into a finished talking-head video.

## Transcription Workflow (NEW)

### Supadata API — Video Transcription

Before generating an avatar video, you can transcribe any YouTube, TikTok, Twitter, or Instagram video using Supadata. Use this to capture the script from existing videos, then optionally rewrite it and feed it to HeyGen.

**API Key:** `sd_5a855a75e509786200517d1f50dd40e7`  
**Base URL:** `https://api.supadata.ai/v1`  
**Auth Header:** `x-api-key: sd_5a855a75e509786200517d1f50dd40e7`

### Request Transcript

```bash
curl -s -X GET "https://api.supadata.ai/v1/transcript?url=VIDEO_URL&text=true&mode=auto" \
  -H "x-api-key: sd_5a855a75e509786200517d1f50dd40e7"
```

**Parameters:**
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | Yes | — | YouTube, TikTok, Twitter, Instagram, or direct file URL |
| `lang` | No | first available | ISO 639-1 language code (e.g., `en`, `es`) |
| `text` | No | `false` | `true` returns plain text; `false` returns JSON with timestamps |
| `mode` | No | `auto` | `native` (fetch existing), `generate` (AI transcription), `auto` (try native, fallback to AI) |

**Response — Success (200):** Plain text transcript (when `text=true`), or JSON with `content` array of `{text, offset, duration, lang}` objects.

**Response — Processing (202):** Returns `{"jobId": "..."}`. Poll with:

```bash
curl -s -X GET "https://api.supadata.ai/v1/transcript/job/JOB_ID" \
  -H "x-api-key: sd_5a855a75e509786200517d1f50dd40e7"
```

### Full Workflow: Transcribe → Rewrite → Avatar Video

1. **Transcribe** — Send video URL to Supadata with `text=true&mode=auto`
2. **Check status** — If 202, poll job endpoint until complete
3. **Optional: Rewrite** — If Charles asks, rewrite the transcript (change tone, shorten, adapt for avatar delivery, etc.)
4. **Generate** — Feed the (rewritten) script to the HeyGen `v2/video/generate` endpoint
5. **Download** — Poll for completion, download the MP4 to `agents/eric/clips/`
6. **Deliver** — Send via Telegram as `MEDIA:/path/to/video.mp4`

**Example end-to-end:**

```bash
# Step 1: Transcribe
TRANSCRIPT=$(curl -s -X GET "https://api.supadata.ai/v1/transcript?url=https://youtu.be/EXAMPLE&text=true&mode=auto" \
  -H "x-api-key: sd_5a855a75e509786200517d1f50dd40e7")

# Step 2: Check for async job
echo "$TRANSCRIPT" | python3 -c "import json,sys; d=json.load(sys.stdin); print('jobId' in d and d.get('jobId') or d)"

# Step 2b: If jobId returned, poll until done
# curl -s "https://api.supadata.ai/v1/transcript/job/JOB_ID" \
#   -H "x-api-key: sd_5a855a75e509786200517d1f50dd40e7"

# Step 3: (Optional) Rewrite the script — use LLM to adapt tone/length

# Step 4: Generate HeyGen avatar video with the script
```

## Credentials

- **API Key:** Stored at `/root/.openclaw/workspace/.secrets/heygen.env` as `HEYGEN_API_KEY`
- **Charles Blair Avatar ID:** `88c37101a7b34c7da97532c24ad6d135`
- **Base URL:** `https://api.heygen.com`
- **Auth header:** `X-Api-Key: {API_KEY}`

## Quick Start

### Generate a Video

```python
import urllib.request, json, time

HEYGEN_KEY = open("/root/.openclaw/workspace/.secrets/heygen.env").read().split("=",1)[1].strip()
AVATAR_ID = "88c37101a7b34c7da97532c24ad6d135"
VOICE_ID = "16e17a9c75554c68b586c2ac343619f7"  # Default English male voice

headers = {"X-Api-Key": HEYGEN_KEY, "Content-Type": "application/json"}

payload = {
    "video_inputs": [{
        "character": {
            "type": "avatar",
            "avatar_id": AVATAR_ID,
            "avatar_style": "normal"
        },
        "voice": {
            "type": "text",
            "input_text": "YOUR SCRIPT HERE",
            "voice_id": VOICE_ID,
            "speed": 1.0
        }
    }],
    "dimension": {"width": 720, "height": 1280},
    "aspect_ratio": "9:16"
}

req = urllib.request.Request(
    "https://api.heygen.com/v2/video/generate",
    data=json.dumps(payload).encode(),
    headers=headers,
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())

video_id = result["data"]["video_id"]
print(f"Video ID: {video_id}")
```

### Poll for Completion

```python
for attempt in range(30):
    req = urllib.request.Request(
        f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
        headers={"X-Api-Key": HEYGEN_KEY}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())["data"]
    
    status = data.get("status")
    print(f"[{attempt+1}] {status}")
    
    if status == "completed":
        print(f"URL: {data['video_url']}")
        break
    elif status == "failed":
        print(f"Error: {data.get('error')}")
        break
    
    time.sleep(10)
```

### Download and Deliver

```bash
curl -sL "{video_url}" -o /root/.openclaw/workspace/agents/eric/clips/YYYY-MM-DD/video.mp4
```

Then send via Telegram: `MEDIA:/path/to/video.mp4`

## Key API Endpoints

| Action | Method | Endpoint |
|--------|--------|----------|
| List avatars | GET | `/v2/avatars` |
| List voices | GET | `/v2/voices` |
| Generate video | POST | `/v2/video/generate` |
| Check status | GET | `/v1/video_status.get?video_id=ID` |
| List videos | GET | `/v1/video.list` |

## Important Notes

- **Render time:** 60-180 seconds typically. Poll every 10 seconds.
- **Max script length:** 5,000 characters per video
- **Voice:** Default voice `16e17a9c75554c68b586c2ac343619f7` is a solid English male. Charles can get his own voice cloned in HeyGen settings for an exact match.
- **Aspect ratio:** Always use `9:16` (720x1280) for TikTok/Reels/Shorts
- **Avatar style:** Use `"closeUp"` for 9:16 vertical videos — `"normal"` causes letterboxing (renders a 16:9 crop centered in the vertical frame with white bars top and bottom). Always use `"closeUp"` for TikTok/Reels/Shorts.
- **Output:** Save to Eric's clips folder `agents/eric/clips/YYYY-MM-DD/`

## Workflow: Recreate a TikTok/YouTube Short

1. Browse to the URL with browser tools — take a vision screenshot
2. Extract: topic, script style, text overlays, format
3. Write a new script matching the tone and structure
4. Generate with HeyGen using Charles Blair avatar
5. Download the MP4
6. Add text overlays with ffmpeg (see reels-text-overlay skill)
7. Deliver via Telegram

## Pitfalls: Getting the Script from YouTube Shorts

YouTube aggressively blocks bot access to Shorts — sign-in walls appear on:
- Browser automation (even headless)
- yt-dlp (HTTP 400 "Sign in to confirm you're not a bot")
- youtube-transcript-api (times out or errors on bot-flagged IPs)

**If YouTube blocks access, ask Charles to:**
- Paste the transcript/script directly into chat, OR
- Send a screenshot of the video with captions visible

Do NOT waste multiple retries on youtube-transcript-api or yt-dlp for Shorts — they will all hit the same bot wall. Ask Charles immediately.

## Post-Production: Add Text Overlays

After generating, pipe through ffmpeg for viral-style text overlays:

```bash
FONT="/usr/share/fonts/Montserrat-ExtraBold.ttf"
ffmpeg -y -i input.mp4 \
  -vf "
    drawtext=fontfile='$FONT':text='HOOK TEXT':fontsize=46:fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=80:enable='between(t,0,2)',
    drawtext=fontfile='$FONT':text='MAIN POINT':fontsize=56:fontcolor='#FF6B35':borderw=5:bordercolor=black:x=(w-text_w)/2:y=600:enable='between(t,2,4)',
    drawtext=fontfile='$FONT':text='🔗 LINK IN BIO':fontsize=38:fontcolor='#FF6B35':borderw=4:bordercolor=black:x=(w-text_w)/2:y=1150:enable='between(t,4,6)'
  " \
  -c:v libx264 -preset fast -crf 18 -c:a copy output.mp4
```

Font sizing guide (learned from trial/error):
- Hook/CTA text: 38-46px (NOT 60-88px — too big)
- Section titles: 50-56px
- Body/subtitle: 26-34px
- Always use `borderw=4` black stroke for readability

## Save API Key

```bash
echo "HEYGEN_API_KEY=sk_V2_..." >> /root/.openclaw/workspace/.secrets/heygen.env
```
