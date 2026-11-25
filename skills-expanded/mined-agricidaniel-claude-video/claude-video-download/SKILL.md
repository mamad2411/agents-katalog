---
name: claude-video-download
description: >
  Video downloading via yt-dlp with format selection, quality control, subtitle
  download, audio-only extraction, and playlist support. Downloads from YouTube,
  Vimeo, Twitter, TikTok, and 1000+ other sites. Use when user says "download video",
  "download from youtube", "yt-dlp", "grab video", "save video", "download audio",
  "download playlist", or provides a video URL to download.
allowed-tools:
  - Bash
  - Read
---

# claude-video-download — Video Downloading via yt-dlp

## Pre-Flight

1. Check yt-dlp is installed: `command -v yt-dlp || echo "Run /video setup"`
2. Confirm user owns or has rights to download the content

## Important: Content Rights

Always remind the user:
- Only download content you own or have permission to use
- Respect copyright and platform terms of service
- Downloaded content is for personal use unless otherwise licensed

## Common Operations

### List Available Formats (no download)

```bash
yt-dlp -F "URL"
```
Shows all available video and audio formats with resolution, codec, bitrate, and file size.

### Best Quality Download

```bash
# Best video + best audio, merged to MP4
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"
```

### Specific Resolution

```bash
# 1080p max
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"

# 720p max
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
  --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"

# 4K
yt-dlp -f "bestvideo[height<=2160]+bestaudio" \
  --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"
```

### Audio-Only Download

```bash
# Best audio as MP3
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "%(title)s.%(ext)s" "URL"

# Best audio as M4A (AAC)
yt-dlp -x --audio-format m4a -o "%(title)s.%(ext)s" "URL"

# Best audio as WAV (lossless)
yt-dlp -x --audio-format wav -o "%(title)s.%(ext)s" "URL"

# Best audio as Opus (most efficient)
yt-dlp -x --audio-format opus -o "%(title)s.%(ext)s" "URL"
```

### Download with Subtitles

```bash
# Download video + all available subtitles
yt-dlp --write-subs --sub-langs all -o "%(title)s.%(ext)s" "URL"

# Download video + auto-generated subtitles
yt-dlp --write-auto-subs --sub-langs en -o "%(title)s.%(ext)s" "URL"

# Download subtitles only (no video)
yt-dlp --write-subs --sub-langs en --skip-download -o "%(title)s.%(ext)s" "URL"

# Embed subtitles into MP4
yt-dlp --write-subs --sub-langs en --embed-subs \
  --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"
```

### Download with Metadata

```bash
# Embed thumbnail and metadata
yt-dlp --embed-thumbnail --embed-metadata \
  --merge-output-format mp4 -o "%(title)s.%(ext)s" "URL"
```

### Playlist Download

```bash
# Download entire playlist
yt-dlp -o "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s" "PLAYLIST_URL"

# Download specific range from playlist
yt-dlp --playlist-start 5 --playlist-end 10 \
  -o "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s" "PLAYLIST_URL"

# Download playlist as audio only
yt-dlp -x --audio-format mp3 \
  -o "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s" "PLAYLIST_URL"
```

### Clip Download (specific time range)

```bash
# Download only a portion (requires ffmpeg)
yt-dlp --download-sections "*00:01:00-00:02:00" -o "%(title)s_clip.%(ext)s" "URL"
```

## Output Templates

| Template | Example Output |
|----------|---------------|
| `%(title)s.%(ext)s` | Video Title.mp4 |
| `%(uploader)s - %(title)s.%(ext)s` | Channel - Title.mp4 |
| `%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s` | 2026-01-15 - Title.mp4 |
| `%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s` | Playlist/001 - Title.mp4 |

## Video Info (No Download)

```bash
# Print video info as JSON
yt-dlp --dump-json "URL" | jq '{title, duration, view_count, upload_date, resolution}'

# Just print title and duration
yt-dlp --print "%(title)s (%(duration_string)s)" "URL"
```

## Rate Limiting and Safety

```bash
# Limit download speed (be nice to servers)
yt-dlp --limit-rate 10M -o "%(title)s.%(ext)s" "URL"

# Sleep between downloads in a playlist
yt-dlp --sleep-interval 5 --max-sleep-interval 15 -o "%(title)s.%(ext)s" "PLAYLIST_URL"
```

## Supported Sites

yt-dlp supports 1000+ sites including: YouTube, Vimeo, Twitter/X, TikTok, Instagram, Reddit, Twitch, Dailymotion, SoundCloud, Bandcamp, and many more. Run `yt-dlp --list-extractors` for the full list.
