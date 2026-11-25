---
name: claude-video-export
description: >
  One-command platform-optimized video export using FFmpeg. Produces ready-to-upload
  files for YouTube, TikTok, Instagram Reels, Instagram Feed, LinkedIn, Web (WebM),
  Podcast (audio-only), and high-quality GIF. Handles resolution, codec, bitrate,
  aspect ratio, and container requirements per platform. Use when user says "export",
  "youtube", "tiktok", "reels", "shorts", "instagram", "linkedin", "web", "webm",
  "gif", "podcast", or "platform export".
allowed-tools:
  - Bash
  - Read
---

# claude-video-export — Platform-Optimized Export

## Pre-Flight

1. Run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"`
2. Run `bash scripts/detect_gpu.sh` for encoder selection
3. Analyze input: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of json "$INPUT"`

## Platform Presets

### YouTube (1080p)

```bash
ffmpeg -n -i "$INPUT" -c:v libx264 -preset slow -crf 18 -profile:v high -level 4.1 \
  -pix_fmt yuv420p -bf 2 -g 30 -movflags +faststart \
  -c:a aac -b:a 384k -ar 48000 "${INPUT%.*}_youtube.mp4"
```

**YouTube 4K**:
```bash
ffmpeg -n -i "$INPUT" -c:v libx264 -preset slow -crf 18 -profile:v high -level 5.1 \
  -pix_fmt yuv420p -movflags +faststart \
  -c:a aac -b:a 512k -ar 48000 "${INPUT%.*}_youtube_4k.mp4"
```

**YouTube NVENC** (5-10x faster):
```bash
ffmpeg -n -hwaccel cuda -hwaccel_output_format cuda -i "$INPUT" \
  -c:v h264_nvenc -preset p5 -tune hq -rc constqp -cq 19 \
  -profile:v high -movflags +faststart \
  -c:a aac -b:a 384k -ar 48000 "${INPUT%.*}_youtube.mp4"
```

### TikTok / Reels / Shorts (9:16 Vertical)

**Center crop** (from 16:9 source):
```bash
ffmpeg -n -i "$INPUT" \
  -vf "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos" \
  -c:v libx264 -crf 20 -preset medium -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 44100 -movflags +faststart \
  -t 180 "${INPUT%.*}_tiktok.mp4"
```
Note: TikTok max 10 min, Reels max 3 min, Shorts max 3 min. The `-t 180` caps at 3 min.

**With padding** (black bars, no crop):
```bash
ffmpeg -n -i "$INPUT" \
  -vf "scale=1080:-2:flags=lanczos,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 20 -preset medium -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart "${INPUT%.*}_vertical.mp4"
```

**With blur background** (cinematic, no black bars):
```bash
ffmpeg -n -i "$INPUT" -i "$INPUT" -filter_complex \
  "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=20[bg];\
   [1:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];\
   [bg][fg]overlay=(W-w)/2:(H-h)/2" \
  -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 128k \
  -movflags +faststart "${INPUT%.*}_tiktok_blur.mp4"
```

### Instagram Feed (Square 1:1)

```bash
ffmpeg -n -i "$INPUT" \
  -vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080:flags=lanczos" \
  -c:v libx264 -crf 20 -preset medium -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart \
  -t 60 "${INPUT%.*}_ig_square.mp4"
```

### Instagram Feed (Portrait 4:5)

```bash
ffmpeg -n -i "$INPUT" \
  -vf "crop=ih*4/5:ih,scale=1080:1350:flags=lanczos" \
  -c:v libx264 -crf 20 -preset medium -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart \
  -t 60 "${INPUT%.*}_ig_portrait.mp4"
```

### LinkedIn

```bash
ffmpeg -n -i "$INPUT" \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 20 -preset medium -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  -fs 200M "${INPUT%.*}_linkedin.mp4"
```
Note: LinkedIn max 200MB / 10 min. The `-fs 200M` caps file size.

### Web (VP9 + Opus for modern browsers)

```bash
ffmpeg -n -i "$INPUT" \
  -c:v libvpx-vp9 -crf 30 -b:v 0 -row-mt 1 \
  -c:a libopus -b:a 128k "${INPUT%.*}_web.webm"
```

### Podcast (Audio-Only)

```bash
# AAC (most compatible)
ffmpeg -n -i "$INPUT" -vn \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:a aac -b:a 128k -ar 44100 "${INPUT%.*}_podcast.m4a"

# MP3 (universal)
ffmpeg -n -i "$INPUT" -vn \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:a libmp3lame -b:a 192k -ar 44100 "${INPUT%.*}_podcast.mp3"
```

### High-Quality GIF

```bash
# Short clip (3 seconds starting at 5s)
ffmpeg -n -ss 5 -t 3 -i "$INPUT" \
  -vf "fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  "${INPUT%.*}.gif"
```

For longer GIFs, consider reducing fps to 10 and scale to 320px width.

### Twitter/X

```bash
ffmpeg -n -i "$INPUT" \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 22 -preset medium -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart \
  -fs 512M -t 140 "${INPUT%.*}_twitter.mp4"
```
Note: Twitter max 512MB / 2:20.

## Platform Specs Quick Reference

| Platform | Max Resolution | Max Duration | Max Size | Aspect Ratio | Codec |
|----------|---------------|-------------|----------|-------------|-------|
| YouTube | 8K | 12 hours | 256 GB | Any (16:9 preferred) | H.264/H.265/AV1 |
| TikTok | 1080x1920 | 10 min | 287 MB | 9:16 | H.264 |
| Instagram Reels | 1080x1920 | 3 min | 250 MB | 9:16 | H.264 |
| Instagram Feed | 1080x1080 | 60s | 250 MB | 1:1 or 4:5 | H.264 |
| LinkedIn | 1920x1080 | 10 min | 200 MB | 16:9 or 1:1 | H.264 |
| Twitter/X | 1920x1200 | 2:20 | 512 MB | Any | H.264 |
| Web (WebM) | Any | Any | Any | Any | VP9/AV1 + Opus |

## Multi-Platform Export

To export for multiple platforms at once, Claude should chain exports sequentially.
Each export is independent — they share the same input but produce separate outputs.

## Output Naming

Auto-generated output names use the pattern: `{input_basename}_{platform}.{ext}`
- `video.mp4` → `video_youtube.mp4`, `video_tiktok.mp4`, `video_ig_square.mp4`

## Reference

Load `references/export-presets.md` for detailed per-platform codec settings, bitrate targets, and container requirements.
