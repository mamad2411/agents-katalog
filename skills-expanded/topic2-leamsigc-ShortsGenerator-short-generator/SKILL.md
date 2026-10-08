---
name: short-generator
version: 2.0.0
description: |
  Generate YouTube Shorts from a subject with video clips sourced from
  multiple social media platforms (Instagram, Facebook, X/Twitter, TikTok,
  YouTube, Bilibili, Douyin, Kuaishou, Weibo, NicoNico).
  Workflow: generate script → select voice → pick source platforms →
  search for videos by hashtag/keyword across platforms → download →
  preview config → generate final video.

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Question
  - ChromeDevTools
  - WebSearch
---

# Short Generator Skill

Generate YouTube Shorts using video clips sourced from multiple social media platforms.

## Quick Command Format

```
/short-generator <subject> [voice:<voice_id>] [hashtags:<tag1,tag2>] [sources:<platform1,platform2>] [ratio:<9:16|16:9|1:1|4:5|21:9>] [music:<on|off>] [subtitle_position:<pos>]
```

Any missing parameters will be collected interactively.

## Workflow Steps

### Step 1: Parse Input & Validate Environment

Parse the user's command for optional inline params:
- `voice:` — TTS voice ID (default: ask user)
- `hashtags:` — comma-separated search terms/tags (default: ask user)
- `sources:` — comma-separated source platforms (default: ask user)
- `ratio:` — aspect ratio (default: `9:16`)
- `music:` — `on` or `off` (default: ask user)
- `subtitle_position:` — subtitle position (default: `center,bottom`)

Extract the subject (first positional arg after removing all `key:value` tokens).

**Pre-flight check**: Ensure the Flask backend is running on port 8080:
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/models
```
If not running, ask the user to start it (`cd Backend && python main.py`).

Fetch available voices and settings:
```bash
curl -s http://localhost:8080/api/models | python3 -m json.tool
curl -s http://localhost:8080/api/settings | python3 -m json.tool
```

Extract the available voices list and aspect ratios from the response for use in questions.

### Step 2: Generate Script

Call the script generation endpoint:

```bash
curl -s -X POST http://localhost:8080/api/script \
  -H "Content-Type: application/json" \
  -d '{"videoSubject": "<subject>", "extraPrompt": "Make it engaging and viral", "aiModel": "g4f", "scriptTemplate": "viral_shorts"}'
```

**Show the generated script** to the user with clear formatting. Ask if they want to:
- Accept and continue
- Regenerate with a different prompt
- Edit the script manually (let them paste a custom script)

Store the final `script` and the `search_terms` from the response.

### Step 3: Collect Missing Parameters

For each parameter the user didn't provide inline, ask:

1. **Voice**: Ask "Which TTS voice?" with available voices from Step 1. Show voice IDs.
2. **Hashtags/Search Terms**: Ask "What search terms or hashtags should I use?" (e.g., `Messi goal, World Cup 2026, soccer highlights`). Get at least one.
3. **Source Platforms**: Ask "Which platforms to search?" — offer platforms from the reference table below. Default: `instagram,facebook,tiktok,youtube,bilibili,douyin`. Let them pick multiple.
4. **Aspect Ratio**: Ask "Which aspect ratio?" — show options from settings (9:16, 16:9, 1:1, 4:5, 21:9). Default: `9:16`.
5. **Music**: Ask "Add background music?" — `on` or `off`.
6. **Subtitle Position**: Ask "Subtitle position?" — options: `center,bottom`, `center,center`, `center,top`. Default: `center,bottom`.

Collect responses and store them.

### Step 4: Find Video URLs Across Selected Platforms

Use the search terms from Step 3 to find at least 5 video URLs across the user's chosen platforms.

For each platform, use the appropriate search strategy:

#### Instagram
- **Chrome DevTools**: Navigate to `https://www.instagram.com/explore/tags/<hashtag>/`, take snapshot, look for `/reel/` links
- **Web search**: `site:instagram.com/reel <search_terms>`

#### Facebook
- **Chrome DevTools**: Navigate to `https://www.facebook.com/search/videos/?q=<search_terms>`, look for video URLs
- **Web search**: `site:facebook.com/watch <search_terms>`

#### X / Twitter
- **Chrome DevTools**: Navigate to `https://x.com/search?q=<search_terms>&src=typed_query&f=video`, look for video post URLs
- **Web search**: `site:x.com <search_terms> video`

#### TikTok
- **Chrome DevTools**: Navigate to `https://www.tiktok.com/search/video?q=<search_terms>`, look for video URLs (contain `/video/`)
- **Web search**: `site:tiktok.com <search_terms>`

#### YouTube
- **Chrome DevTools**: Navigate to `https://www.youtube.com/results?search_query=<search_terms>`, look for `/watch?v=` links
- **Web search**: `site:youtube.com <search_terms>` — prefer `/shorts/` URLs if available

#### Bilibili (Chinese)
- **Chrome DevTools**: Navigate to `https://search.bilibili.com/all?keyword=<search_terms>`, look for video URLs (contain `/video/`)
- **Web search**: `site:bilibili.com <search_terms>`

#### Douyin (Chinese TikTok)
- **Chrome DevTools**: Navigate to `https://www.douyin.com/search/<search_terms>`, look for video URLs
- **Web search**: `site:douyin.com <search_terms>`

#### Kuaishou (Chinese)
- **Web search**: `site:kuaishou.com <search_terms>`

#### Weibo (Chinese)
- **Web search**: `site:weibo.com <search_terms> video`

#### Nico Nico Douga (Japanese)
- **Chrome DevTools**: Navigate to `https://www.nicovideo.jp/search/<search_terms>`, look for `/watch/` URLs
- **Web search**: `site:nicovideo.jp <search_terms>`

**Fallback — Ask user**: If automated search finds fewer than 5 URLs, ask the user to provide video URLs directly from any platform.

Collect all URLs into an array. Deduplicate. Ensure at least 5 total.

### Step 5: Download Videos

For each video URL, download via the backend API:

```bash
curl -s -X POST http://localhost:8080/api/instagram/download \
  -H "Content-Type: application/json" \
  -d '{"url": "<video_url>"}'
```

The backend uses `yt-dlp` which supports all the platforms listed above. If a URL fails:
- Log the error and move to the next URL
- Try appending `?` query params or alternate URL formats (e.g., short URL)
- As a last resort, skip that URL and note it to the user

Save each successful download's `filename` into a list. The files are stored at `Backend/static/generated_videos/instagram/<filename>`. Note: even though the directory is named `instagram/`, the backend's `yt-dlp` downloader handles all platforms.

Show progress: "Downloaded 3/5 videos..."

Construct the full paths:
```python
import os
backend_dir = os.path.dirname("Backend")
video_paths = [os.path.join(backend_dir, "static", "generated_videos", "instagram", f) for f in filenames]
```

### Step 6: Show Full Configuration Preview

Show the user a clear preview of everything configured:

```
╔══════════════════════════════════════════╗
║           VIDEO CONFIGURATION            ║
╠══════════════════════════════════════════╣
║ Subject:     <subject>                   ║
║ Voice:       <voice_id>                  ║
║ Aspect:      <ratio>                     ║
║ Music:       <on/off>                    ║
║ Subtitles:   <position>                  ║
║ Sources:     <platforms list>            ║
║ Clips:       <count> videos              ║
╠══════════════════════════════════════════╣
║ Script:                                  ║
║ <first 300 chars of script>...           ║
╚══════════════════════════════════════════╝
```

Ask: "Generate the video with this configuration?" (Yes/No)

### Step 7: Generate Final Video

On confirmation, call the search-and-download endpoint with the downloaded video paths:

```bash
curl -s -X POST http://localhost:8080/api/search-and-download \
  -H "Content-Type: application/json" \
  -d '{
    "search": <search_terms>,
    "script": "<script>",
    "aiModel": "g4f",
    "voice": "<voice_id>",
    "subtitlesPosition": "<subtitle_position>",
    "aspectRatio": "<ratio>",
    "subtitleTemplate": "classic",
    "directVideoPaths": <video_paths>,
    "useMusic": <true/false>
  }'
```

This will use the downloaded videos directly (skipping Pexels search).

### Step 8: Show Result

Show the final video details:
```
✅ Video generated!
   Path: /static/generated_videos/<filename>.mp4
   Open: http://localhost:8080/static/generated_videos/<filename>.mp4
```

Ask if they want to add background music (if not added yet) via:
```bash
curl -s -X POST http://localhost:8080/api/addAudio \
  -H "Content-Type: application/json" \
  -d '{"finalVideo": "<final_video_path>", "songPath": "", "aiModel": "g4f", "musicSource": "library", "aspectRatio": "<ratio>"}'
```

## Parameter References

### Available Voices
Fetch from `GET /api/models` — response contains `data.voices` array.

### Aspect Ratios
| Value | Label |
|-------|-------|
| 9:16 | Shorts/TikTok (default) |
| 16:9 | YouTube |
| 1:1 | Square |
| 4:5 | Instagram |
| 21:9 | Ultra Wide |

### Supported Source Platforms

| Platform | URL Pattern | Country | yt-dlp Support |
|----------|------------|---------|----------------|
| Instagram | `instagram.com/reel/...` | Global | ✅ |
| Facebook | `facebook.com/*/videos/*` or `fb.watch/*` | Global | ✅ |
| X / Twitter | `x.com/*/status/*` | Global | ✅ |
| TikTok | `tiktok.com/@*/video/*` | Global | ✅ |
| YouTube | `youtube.com/watch?v=*` or `youtu.be/*` | Global | ✅ |
| Bilibili | `bilibili.com/video/*` | China | ✅ |
| Douyin | `douyin.com/video/*` | China | ✅ |
| Kuaishou | `kuaishou.com/*` | China | ✅ |
| Weibo | `weibo.com/*` | China | ✅ |
| NicoNico | `nicovideo.jp/watch/*` | Japan | ✅ |

The backend uses `yt-dlp` as its download engine, which supports all of the above platforms natively.

### Subtitle Templates
| Value | Style |
|-------|-------|
| classic | Yellow on black (default) |
| modern_glow | White with cyan glow |
| bold_outline | White with thick black stroke |
| minimal | White with minimal stroke |
| cinematic | Gold on black |
| neon | Magenta on pink |
| social_viral | Orange on black |
| floating | White on black, centered |
| news_ticker | White on red, top |
| karaoke_highlight | Cyan on magenta, top |

## Defaults Summary

| Parameter | Default |
|-----------|---------|
| aiModel | `g4f` |
| scriptTemplate | `viral_shorts` |
| aspectRatio | `9:16` |
| subtitlesPosition | `center,bottom` |
| subtitleTemplate | `classic` |
| sources | `instagram,facebook,tiktok,youtube,bilibili,douyin` |
| useMusic | `false` |
| threads | `4` |
