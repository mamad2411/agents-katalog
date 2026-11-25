---
name: claude-video-audio
description: >
  Audio processing for video files using FFmpeg. Loudness normalization to streaming
  standards (LUFS), noise reduction, audio mixing, extraction, replacement, silence
  detection and removal, equalization, compression, fade effects, format conversion,
  and audio ducking. Use when user says "audio", "normalize", "volume", "loudness",
  "LUFS", "noise", "silence", "extract audio", "replace audio", "mix audio", "equalizer",
  "compress audio", "ducking", or "sidechain".
allowed-tools:
  - Bash
  - Read
---

# claude-video-audio — Audio Processing

## Pre-Flight

1. Run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"`
2. Analyze audio streams: `ffprobe -v error -select_streams a -show_entries stream=codec_name,channels,sample_rate,bit_rate -of json "$INPUT"`

## Loudness Normalization (EBU R128)

Two-pass workflow for accurate normalization:

```bash
# Pass 1: Measure current loudness
ffmpeg -i "$INPUT" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | tail -12
```

Extract `measured_I`, `measured_TP`, `measured_LRA`, `measured_thresh`, `offset` from the JSON output.

```bash
# Pass 2: Apply normalization with measured values
ffmpeg -n -i "$INPUT" -af "loudnorm=I=-14:TP=-1.5:LRA=11:\
measured_I=MEASURED_I:measured_TP=MEASURED_TP:measured_LRA=MEASURED_LRA:\
measured_thresh=MEASURED_THRESH:offset=MEASURED_OFFSET:linear=true" \
  -c:v copy "$OUTPUT"
```

### Target Loudness by Platform

| Platform | Target LUFS | True Peak | Notes |
|----------|------------|-----------|-------|
| YouTube | -14 LUFS | -1.0 dBTP | YouTube normalizes down, not up |
| Spotify | -14 LUFS | -1.0 dBTP | "Loud" mode = -11 LUFS |
| Apple Music | -16 LUFS | -1.0 dBTP | Sound Check |
| Podcast | -16 LUFS | -1.5 dBTP | Conversational clarity |
| Broadcast (EBU R128) | -23 LUFS | -1.0 dBTP | European standard |
| TikTok/Reels | -14 LUFS | -1.0 dBTP | Match YouTube |

## Noise Reduction

**FFT-based** (good for consistent background noise):
```bash
ffmpeg -n -i "$INPUT" -af "afftdn=nf=-25:nt=w" -c:v copy "$OUTPUT"
```
`nf` = noise floor in dB (lower = more aggressive). `nt=w` = white noise model.

**Non-local means** (better quality, slower):
```bash
ffmpeg -n -i "$INPUT" -af "anlmdn=s=7:p=0.002:r=0.002" -c:v copy "$OUTPUT"
```

**Highpass/lowpass** to remove rumble and hiss:
```bash
ffmpeg -n -i "$INPUT" -af "highpass=f=80,lowpass=f=12000" -c:v copy "$OUTPUT"
```

## Silence Detection and Removal

**Detect silence**:
```bash
ffmpeg -i "$INPUT" -af "silencedetect=noise=-30dB:d=0.5" -f null - 2>&1 | grep silence
```
Returns `silence_start` and `silence_end` timestamps.

**Remove silence** (using Auto-Editor — much easier):
```bash
auto-editor "$INPUT" --margin 0.3s -o "$OUTPUT"
```

**Manual silence removal** with FFmpeg:
```bash
ffmpeg -n -i "$INPUT" -af "silenceremove=start_periods=1:start_silence=0.5:start_threshold=-30dB:detection=rms" -c:v copy "$OUTPUT"
```

## Audio Extraction

```bash
# Extract as WAV (lossless)
ffmpeg -n -i "$INPUT" -vn -c:a pcm_s16le audio.wav

# Extract as AAC
ffmpeg -n -i "$INPUT" -vn -c:a aac -b:a 256k audio.m4a

# Extract as MP3
ffmpeg -n -i "$INPUT" -vn -c:a libmp3lame -b:a 320k audio.mp3

# Extract as Opus (most efficient)
ffmpeg -n -i "$INPUT" -vn -c:a libopus -b:a 128k audio.ogg

# Stream copy (fastest, keeps original codec)
ffmpeg -n -i "$INPUT" -vn -c:a copy audio.m4a
```

## Audio Replacement

```bash
# Replace audio track entirely
ffmpeg -n -i video.mp4 -i new_audio.wav -c:v copy -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 "$OUTPUT"

# Mix original audio with new audio (e.g., background music)
ffmpeg -n -i video.mp4 -i music.mp3 -filter_complex \
  "[0:a]volume=1.0[orig];[1:a]volume=0.3[music];[orig][music]amix=inputs=2:duration=first" \
  -c:v copy "$OUTPUT"
```

## Audio Effects

**Volume adjustment**:
```bash
ffmpeg -n -i "$INPUT" -af "volume=1.5" -c:v copy "$OUTPUT"   # 1.5x louder
ffmpeg -n -i "$INPUT" -af "volume=-6dB" -c:v copy "$OUTPUT"   # 6dB quieter
```

**Equalization**:
```bash
# Boost bass, cut muddy mids, add presence
ffmpeg -n -i "$INPUT" -af "equalizer=f=80:t=q:w=1:g=3,equalizer=f=300:t=q:w=2:g=-2,equalizer=f=4000:t=q:w=1:g=2" -c:v copy "$OUTPUT"
```

**Compression** (reduce dynamic range):
```bash
ffmpeg -n -i "$INPUT" -af "acompressor=threshold=-20dB:ratio=4:attack=5:release=50" -c:v copy "$OUTPUT"
```

**Limiter** (prevent clipping):
```bash
ffmpeg -n -i "$INPUT" -af "alimiter=limit=0.95:level=false" -c:v copy "$OUTPUT"
```

**Fade in/out**:
```bash
ffmpeg -n -i "$INPUT" -af "afade=t=in:st=0:d=2,afade=t=out:st=OFFSET:d=2" -c:v copy "$OUTPUT"
```

**Bass boost**: `-af "bass=g=5:f=100:w=0.5"`
**Treble boost**: `-af "treble=g=3:f=4000:w=0.5"`

## Audio Format Conversion

| Codec | FFmpeg Encoder | Recommended Bitrate | Use Case |
|-------|---------------|-------------------|----------|
| AAC | aac | 128-256k | Video, streaming |
| MP3 | libmp3lame | 192-320k | Universal playback |
| Opus | libopus | 96-160k | Best efficiency, WebM |
| FLAC | flac | Lossless | Archival, editing |
| WAV | pcm_s16le | Uncompressed | Editing, processing |
| AC3 | ac3 | 384-640k | Surround sound |

## Channel Layout

```bash
# Stereo to mono
ffmpeg -n -i "$INPUT" -ac 1 -c:v copy "$OUTPUT"

# Mono to stereo (duplicate)
ffmpeg -n -i "$INPUT" -ac 2 -c:v copy "$OUTPUT"

# Extract left channel only
ffmpeg -n -i "$INPUT" -af "pan=mono|c0=FL" -c:v copy "$OUTPUT"
```

## Audio Sync Fix

```bash
# Delay audio by 0.5 seconds
ffmpeg -n -i "$INPUT" -itsoffset 0.5 -i "$INPUT" -map 0:v -map 1:a -c copy "$OUTPUT"

# Advance audio by 0.5 seconds
ffmpeg -n -i "$INPUT" -itsoffset -0.5 -i "$INPUT" -map 0:v -map 1:a -c copy "$OUTPUT"
```

## Audio Ducking (Sidechain Compression)

Automatically lower music volume when speech is present.

**Basic ducking** (voice track ducks music track):
```bash
ffmpeg -n -i video_with_voice.mp4 -i music.mp3 -filter_complex \
  "[0:a]aformat=fltp:44100:stereo[voice];\
   [1:a]aformat=fltp:44100:stereo[music];\
   [music][voice]sidechaincompress=threshold=0.015:ratio=6:attack=200:release=1000:level_sc=1[ducked];\
   [voice][ducked]amix=inputs=2:duration=first:weights=1 0.4[out]" \
  -map 0:v -map "[out]" -c:v copy "$OUTPUT"
```

**Parameters guide**:
| Parameter | Default | Purpose |
|-----------|---------|---------|
| threshold | 0.015 | Voice level that triggers ducking (lower = more sensitive) |
| ratio | 6 | How much to reduce music (higher = more reduction) |
| attack | 200ms | How quickly music ducks down |
| release | 1000ms | How quickly music returns after speech stops |
| weights | 1 0.4 | Voice volume : music volume in final mix |

**Ducking with existing audio streams** (video has voice + separate music file):
```bash
ffmpeg -n -i "$INPUT" -i music.mp3 -filter_complex \
  "[1:a][0:a]sidechaincompress=threshold=0.02:ratio=8:attack=100:release=800[ducked];\
   [0:a][ducked]amix=inputs=2:duration=first:weights=1 0.3[out]" \
  -map 0:v -map "[out]" -c:v copy "$OUTPUT"
```

**Tips**:
- Lower `threshold` (e.g., 0.01) for quieter speech
- Higher `ratio` (e.g., 10-20) for more aggressive ducking
- Shorter `attack` (e.g., 50ms) for spoken word podcasts
- Longer `release` (e.g., 2000ms) for smoother music return
- Adjust `weights` to control the overall voice-to-music balance

## Reference

Load `references/audio.md` for extended EBU R128 loudness details, advanced filter chains, and format-specific audio settings.
