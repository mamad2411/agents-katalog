---
name: youtube-transcribe
description: Transcribe YouTube videos and extract key information using yt-dlp. Use when the user shares a YouTube URL and wants to transcribe it, summarize it, extract key points, or dump learnings from a video. Triggers on YouTube links (youtube.com/watch, youtu.be) combined with requests to "transcribe", "summarize", "watch", "extract", "key points", "notes from this video", or "what does this video say".
---

# YouTube Transcribe

Transcribe YouTube videos using `yt-dlp` subtitle extraction. Requires `yt-dlp` installed via Homebrew (`brew install yt-dlp`).

## Workflow

### 1. Get Video Metadata

```bash
yt-dlp --print title --print channel --print description --print duration_string "<URL>"
```

Prints title, channel, description, and duration on separate lines.

### 2. Download Subtitles

Try manual subs first (higher quality), fall back to auto-generated:

```bash
# Try manual subs first
yt-dlp --write-sub --sub-lang en --skip-download --sub-format vtt -o "/tmp/yt_transcript" "<URL>" 2>&1

# If no manual subs, use auto-generated
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "/tmp/yt_transcript" "<URL>"
```

- `--skip-download` avoids downloading the actual video
- Output: `/tmp/yt_transcript.en.vtt`
- For other languages, change `--sub-lang` (e.g. `no` for Norwegian)

List available languages if needed:

```bash
yt-dlp --list-subs "<URL>"
```

### 3. Clean VTT into Readable Text

```bash
cat /tmp/yt_transcript.en.vtt | sed '/^$/d' | sed '/^WEBVTT/d' | sed '/^Kind:/d' | sed '/^Language:/d' | sed '/^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]/d' | sed '/^NOTE/d' | sed 's/<[^>]*>//g' | awk '!seen[$0]++'
```

This removes VTT headers, timestamps, NOTE lines, HTML tags, and deduplicates repeated lines. For long transcripts, pipe through `head -N` / `tail -n +N` to read in chunks.

### 4. Clean Up

```bash
rm /tmp/yt_transcript.en.vtt
```

## Notes

- `yt-dlp` version warnings are safe to ignore
- Auto-generated subs lack punctuation and speaker labels; infer from context
- The `awk '!seen[$0]++'` dedup is essential because VTT repeats lines across overlapping cue windows
