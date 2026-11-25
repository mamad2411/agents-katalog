---
name: ffmpeg-process
description: "Process, transcode, and manipulate media files using FFmpeg available in the sandbox. Input/output through the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "🎬"
---

# FFmpeg Process Skill

FFmpeg is available as a CLI tool inside the sandbox container. Media files should be read from and written to the shared volume at `{{SHARED_VOLUME}}`.

## Transcoding Video

Convert a video file to a different format or codec:

```bash
# Convert to MP4 with H.264 codec
ffmpeg -i {{SHARED_VOLUME}}/input/video.avi \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  {{SHARED_VOLUME}}/output/video.mp4

# Convert to WebM for web delivery
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -c:v libvpx-vp9 -crf 30 -b:v 0 \
  -c:a libopus -b:a 128k \
  {{SHARED_VOLUME}}/output/video.webm
```

## Extracting Frames

Pull individual frames or frame sequences from video:

```bash
# Extract a single frame at 00:01:30
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -ss 00:01:30 -frames:v 1 \
  {{SHARED_VOLUME}}/output/frame.png

# Extract one frame per second
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -vf "fps=1" \
  {{SHARED_VOLUME}}/output/frames/frame_%04d.png

# Extract frames as a thumbnail sheet (4x4 grid)
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -vf "select=not(mod(n\,100)),scale=320:180,tile=4x4" \
  -frames:v 1 \
  {{SHARED_VOLUME}}/output/thumbnail_sheet.png
```

## Merging Audio and Video

Combine separate audio and video tracks:

```bash
# Merge audio onto a video (replace existing audio)
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -i {{SHARED_VOLUME}}/input/narration.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 -shortest \
  {{SHARED_VOLUME}}/output/merged.mp4

# Mix original audio with background music
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -i {{SHARED_VOLUME}}/input/music.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3[a]" \
  -c:v copy -map 0:v -map "[a]" \
  {{SHARED_VOLUME}}/output/mixed.mp4
```

## Extracting Audio

```bash
# Extract audio to MP3
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -vn -c:a libmp3lame -q:a 2 \
  {{SHARED_VOLUME}}/output/audio.mp3

# Extract audio to WAV (lossless, good for Whisper input)
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -vn -c:a pcm_s16le -ar 16000 -ac 1 \
  {{SHARED_VOLUME}}/output/audio.wav
```

## Trimming and Splitting

```bash
# Trim a segment from 00:05:00 to 00:10:00
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -ss 00:05:00 -to 00:10:00 -c copy \
  {{SHARED_VOLUME}}/output/clip.mp4

# Split into 60-second segments
ffmpeg -i {{SHARED_VOLUME}}/input/video.mp4 \
  -c copy -f segment -segment_time 60 \
  -reset_timestamps 1 \
  {{SHARED_VOLUME}}/output/segment_%03d.mp4
```

## Getting Media Info

```bash
# Probe file metadata as JSON
ffprobe -v quiet -print_format json -show_format -show_streams \
  {{SHARED_VOLUME}}/input/video.mp4
```

## File Path Patterns

- `{{SHARED_VOLUME}}/input/` — raw source media files
- `{{SHARED_VOLUME}}/output/` — processed output files
- `{{SHARED_VOLUME}}/temp/` — intermediate processing files (clean up after use)

## Tips for AI Agents

- Always use `ffprobe` first to inspect the input file's codecs, resolution, and duration before processing.
- Use `-c copy` for operations that don't need re-encoding (trimming, merging) — it's dramatically faster.
- For Whisper transcription input, extract audio as 16kHz mono WAV: `-ar 16000 -ac 1`.
- Use `-y` flag to overwrite output files without prompting.
- Set `-loglevel error` to suppress verbose output in automated pipelines.
- For long-running jobs, add `-progress pipe:1` to get machine-readable progress updates.
- Clean up temporary files in `{{SHARED_VOLUME}}/temp/` after processing completes.
