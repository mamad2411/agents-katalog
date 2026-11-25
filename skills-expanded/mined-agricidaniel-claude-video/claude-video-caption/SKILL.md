---
name: claude-video-caption
description: >
  Speech-to-text transcription and animated subtitle generation using Whisper and FFmpeg.
  Creates word-by-word animated captions (karaoke-style), SRT/ASS/VTT subtitles,
  burns subtitles into video, extracts existing subtitles, converts between formats,
  and styles captions with custom fonts, colors, and animations. Use when user says
  "caption", "subtitle", "transcribe", "whisper", "SRT", "ASS", "VTT", "burn-in",
  "hardcode subtitles", "word by word", "karaoke", or "add text".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-caption — Transcription and Animated Subtitles

## Pre-Flight

1. Check Whisper is installed: `command -v whisper-ctranslate2 || echo "Run /video setup"`
2. Run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"`
3. Analyze existing subtitle tracks: `ffprobe -v error -select_streams s -show_entries stream=codec_name,codec_type -of json "$INPUT"`

## One-Command Caption Pipeline

For the most common use case (transcribe + animated captions + burn-in):
```bash
bash scripts/caption_pipeline.sh "$INPUT" "$OUTPUT" [language] [style]
```
- `language`: auto (default), en, es, fr, de, ja, zh, etc. (99 languages supported)
- `style`: default, minimal, bold, neon, shadow

## Step-by-Step Manual Pipeline

### Step 1: Extract Audio for Whisper

```bash
ffmpeg -y -i "$INPUT" -vn -ar 16000 -ac 1 -f wav /tmp/claude_video_audio.wav
```

### Step 2: Transcribe with faster-whisper

```bash
# Auto-detect language, word-level timestamps
whisper-ctranslate2 /tmp/claude_video_audio.wav \
  --model large-v3 \
  --output_format json \
  --word_timestamps True \
  --vad_filter True \
  --compute_type int8 \
  --output_dir /tmp/

# For faster transcription (slight accuracy tradeoff)
whisper-ctranslate2 /tmp/claude_video_audio.wav \
  --model large-v3-turbo \
  --output_format json \
  --word_timestamps True \
  --vad_filter True \
  --compute_type float16 \
  --output_dir /tmp/
```

**Model selection**:
| Model | Size | VRAM | Speed | Accuracy | Use Case |
|-------|------|------|-------|----------|----------|
| tiny | 75M | ~1 GB | 32x | Low | Quick drafts |
| base | 142M | ~1 GB | 16x | Fair | Quick subtitles |
| small | 466M | ~2 GB | 6x | Good | General use |
| medium | 1.5B | ~5 GB | 2x | Very good | Quality subtitles |
| large-v3-turbo | 809M | ~6 GB | 8x | Very good | Best speed/accuracy (recommended) |
| large-v3 | 1.5B | ~10 GB | 1x | Best | Professional captioning |

### Step 3: Generate ASS Subtitles with Karaoke Timing

Convert Whisper JSON output to ASS format with word-by-word highlighting.

Generate this Python script inline and run it:
```python
#!/usr/bin/env python3
"""Convert Whisper JSON word timestamps to ASS karaoke subtitles."""
import json, sys

def words_to_ass(json_path, output_path, words_per_line=3, style="default"):
    with open(json_path) as f:
        data = json.load(f)

    # Collect all words with timestamps
    words = []
    for segment in data.get("segments", []):
        for w in segment.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": w["start"],
                "end": w["end"]
            })

    # Style presets (full 23-field ASS V4+ format)
    # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour,
    #         BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing,
    #         Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
    styles = {
        "default":  "Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,1,2,10,10,40,1",
        "bold":     "Default,Impact,24,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,10,10,40,1",
        "minimal":  "Default,Helvetica,18,&H00FFFFFF,&H000000FF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,1,1,0,2,10,10,30,1",
        "neon":     "Default,Arial Black,22,&H0000FFFF,&H00FF00FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,40,1",
        "shadow":   "Default,Georgia,20,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,0,3,2,10,10,40,1",
    }
    style_line = styles.get(style, styles["default"])

    # ASS header
    ass = f"""[Script Info]
Title: claude-video captions
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: {style_line}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def fmt_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    # Group words into lines
    for i in range(0, len(words), words_per_line):
        chunk = words[i:i + words_per_line]
        if not chunk:
            continue
        start = chunk[0]["start"]
        end = chunk[-1]["end"]

        # Build karaoke text with \kf tags
        text_parts = []
        for w in chunk:
            duration_cs = max(1, int((w["end"] - w["start"]) * 100))
            text_parts.append(f"{{\\kf{duration_cs}}}{w['word']}")

        text = " ".join(text_parts)
        ass += f"Dialogue: 0,{fmt_time(start)},{fmt_time(end)},Default,,0,0,0,,{text}\n"

    with open(output_path, "w") as f:
        f.write(ass)

if __name__ == "__main__":
    words_to_ass(sys.argv[1], sys.argv[2],
                 int(sys.argv[3]) if len(sys.argv) > 3 else 3,
                 sys.argv[4] if len(sys.argv) > 4 else "default")
```

### Step 4: Burn Subtitles into Video

```bash
# ASS subtitles (styled, animated)
ffmpeg -n -i "$INPUT" -vf "ass=/tmp/captions.ass" -c:a copy "$OUTPUT"

# SRT subtitles (simple, with basic styling)
ffmpeg -n -i "$INPUT" -vf "subtitles=/tmp/captions.srt:force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2'" -c:a copy "$OUTPUT"
```

## Subtitle Extraction

```bash
# Extract first subtitle track as SRT
ffmpeg -n -i "$INPUT" -map 0:s:0 subtitles.srt

# Extract as ASS
ffmpeg -n -i "$INPUT" -map 0:s:0 subtitles.ass

# Extract all subtitle tracks
ffprobe -v error -select_streams s -show_entries stream=index,codec_name:stream_tags=language -of json "$INPUT"
# Then extract each: ffmpeg -n -i "$INPUT" -map 0:s:INDEX output.srt
```

## Subtitle Format Conversion

```bash
# SRT to ASS
ffmpeg -n -i input.srt output.ass

# ASS to SRT
ffmpeg -n -i input.ass output.srt

# SRT to WebVTT (add "WEBVTT" header)
echo "WEBVTT" > output.vtt && echo "" >> output.vtt && cat input.srt >> output.vtt
```

## Subtitle Timing Adjustment

```bash
# Delay subtitles by 2 seconds
ffmpeg -n -i input.srt -itsoffset 2 output.srt

# For manual offset, edit SRT timestamps with awk or Python
```

## ASS Styling Reference

Key ASS override tags for caption customization:
- `\fn{FontName}` — change font
- `\fs{Size}` — font size
- `\c&HBBGGRR&` — primary color (BGR format, not RGB)
- `\3c&HBBGGRR&` — outline color
- `\bord{Width}` — outline width
- `\shad{Depth}` — shadow depth
- `\fscx{%}\fscy{%}` — scale X/Y (for "pop" animation: `\fscx120\fscy120`)
- `\fad(FadeIn,FadeOut)` — fade timing in ms
- `\kf{Duration}` — karaoke smooth fill (duration in centiseconds)
- `\K{Duration}` — karaoke instant fill
- `\an{Position}` — alignment (1-9 numpad layout, 2=bottom-center, 8=top-center)
- `\pos(x,y)` — absolute position

## Common Presets

**TikTok/Reels style** (large, centered, bold):
```
FontName=Impact,FontSize=28,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=3,Shadow=0,Alignment=2,MarginV=300
```

**YouTube style** (clean, bottom):
```
FontName=Arial,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=40
```

**Podcast/interview** (minimal, lower third):
```
FontName=Helvetica,FontSize=16,PrimaryColour=&H00FFFFFF,BackColour=&H80000000,BorderStyle=4,Alignment=2,MarginV=20
```
