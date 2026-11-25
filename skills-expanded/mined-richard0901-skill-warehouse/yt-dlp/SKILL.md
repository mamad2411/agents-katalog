---
name: yt-dlp
description: Download videos and audio from YouTube and thousands of other websites using yt-dlp. Use this skill when the user provides a video URL and wants to download it, extract audio, or asks about downloading videos/audio from websites like YouTube, Bilibili, TikTok, Twitter/X, Vimeo, etc.
---

# yt-dlp Video Downloader

Download videos and audio from YouTube and 1000+ websites.

## Prerequisites

Check if yt-dlp is installed before downloading:

```bash
which yt-dlp && yt-dlp --version
```

If not installed:
```bash
# macOS
brew install yt-dlp ffmpeg

# Or via pip
pip install yt-dlp
```

## Quick Start

When user provides a video URL:

```bash
# Default: best quality video
yt-dlp "URL"

# Audio only (mp3)
yt-dlp -x --audio-format mp3 "URL"

# Specify output directory
yt-dlp -o "~/Downloads/%(title)s.%(ext)s" "URL"
```

## Common Tasks

### Download Video

```bash
# Best quality (default)
yt-dlp "URL"

# Limit to 1080p
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "URL"

# Limit to 720p
yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" "URL"

# List available formats first
yt-dlp -F "URL"
```

### Extract Audio

```bash
# Extract as mp3
yt-dlp -x --audio-format mp3 "URL"

# Extract as m4a (better quality)
yt-dlp -x --audio-format m4a "URL"
```

### Download Playlist

```bash
# Entire playlist
yt-dlp "PLAYLIST_URL"

# Specific items
yt-dlp --playlist-items 1-5 "PLAYLIST_URL"

# Single video only (ignore playlist)
yt-dlp --no-playlist "URL"
```

### Subtitles

```bash
# Download with subtitles
yt-dlp --write-subs --sub-langs en,zh "URL"

# Embed subtitles in video
yt-dlp --embed-subs "URL"
```

### Output Options

```bash
# Custom output path
yt-dlp -o "~/Downloads/%(title)s.%(ext)s" "URL"

# Include uploader in filename
yt-dlp -o "%(uploader)s - %(title)s.%(ext)s" "URL"
```

## Workflow

1. User provides video URL
2. Ask for preferences if not specified:
   - Video or audio only?
   - Quality preference?
   - Output location? (default: current directory)
3. Check yt-dlp is installed
4. Run appropriate command
5. Report download result

## Troubleshooting

```bash
# Update yt-dlp
yt-dlp -U

# Use browser cookies for login-required content
yt-dlp --cookies-from-browser chrome "URL"

# Verbose output
yt-dlp -v "URL"
```
