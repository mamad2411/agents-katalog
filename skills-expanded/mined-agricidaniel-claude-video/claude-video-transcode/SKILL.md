---
name: claude-video-transcode
description: >
  Video transcoding and codec conversion using FFmpeg with GPU acceleration.
  Converts between H.264, H.265, AV1, VP9, ProRes, and DNxHR. Handles compression,
  quality optimization, two-pass encoding, container remuxing, and batch processing.
  Use when user says "convert", "transcode", "compress", "encode", "change format",
  "h264", "h265", "hevc", "av1", "prores", "mkv to mp4", "reduce file size", "remux",
  "make smaller", "file too big", "shrink video", "smaller file", "video too large",
  "reduce quality", or "change codec". Also trigger when user describes needing a video
  in a different format or wanting to reduce file size for email, upload, or storage.
allowed-tools:
  - Bash
  - Read
---

# claude-video-transcode — Codec Conversion and Compression

## Pre-Flight

1. Run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"`
2. Run `bash scripts/detect_gpu.sh` to determine available encoders
3. Run `bash scripts/estimate_size.sh "$INPUT"` for large files
4. Analyze input: `ffprobe -v error -print_format json -show_format -show_streams "$INPUT"`

## Codec Selection Guide

| Goal | Codec | Encoder (GPU) | Encoder (CPU) | CRF/CQ |
|------|-------|---------------|---------------|---------|
| Best compression (modern) | AV1 | av1_nvenc -cq 30 | libsvtav1 -crf 28 | 28-32 |
| Maximum compatibility | H.264 | h264_nvenc -cq 21 | libx264 -crf 20 | 18-23 |
| Good compression + compat | H.265 | hevc_nvenc -cq 26 | libx265 -crf 24 | 22-28 |
| Web browsers | VP9 | N/A | libvpx-vp9 -crf 30 | 25-35 |
| Professional editing | ProRes | N/A | prores_ks -profile:v 3 | N/A |
| Professional editing | DNxHR | N/A | dnxhd -profile:v dnxhr_hq | N/A |
| No re-encode needed | Copy | -c copy | -c copy | N/A |

**CRF equivalence**: x264 CRF 23 ≈ x265 CRF 28 ≈ SVT-AV1 CRF 30 (similar visual quality, decreasing file size). Each ±6 CRF roughly doubles or halves the bitrate.

## Common Operations

### Simple Compression (H.264, CPU)
```bash
ffmpeg -n -i "$INPUT" -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
```

### GPU-Accelerated (NVENC)

**H.264 NVENC**:
```bash
ffmpeg -n -hwaccel cuda -hwaccel_output_format cuda -i "$INPUT" \
  -c:v h264_nvenc -preset p5 -tune hq -rc constqp -cq 21 \
  -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
```

**H.265 NVENC**:
```bash
ffmpeg -n -hwaccel cuda -hwaccel_output_format cuda -i "$INPUT" \
  -c:v hevc_nvenc -preset p5 -tune hq -rc constqp -cq 26 \
  -spatial-aq 1 -temporal-aq 1 -rc-lookahead 32 \
  -tag:v hvc1 -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
```

**AV1 NVENC** (RTX 40/50 series):
```bash
ffmpeg -n -hwaccel cuda -hwaccel_output_format cuda -i "$INPUT" \
  -c:v av1_nvenc -preset p5 -tune hq -rc constqp -cq 30 \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
```

### AV1 Software (best compression, slow)
```bash
ffmpeg -n -i "$INPUT" -c:v libsvtav1 -crf 28 -preset 6 -pix_fmt yuv420p10le \
  -svtav1-params tune=0 -c:a libopus -b:a 128k "$OUTPUT"
```

### Two-Pass Encoding (target specific bitrate)
```bash
# Pass 1
ffmpeg -y -i "$INPUT" -c:v libx264 -b:v 5M -pass 1 -passlogfile /tmp/ffmpeg2pass \
  -an -f null /dev/null

# Pass 2
ffmpeg -n -i "$INPUT" -c:v libx264 -b:v 5M -pass 2 -passlogfile /tmp/ffmpeg2pass \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"

rm -f /tmp/ffmpeg2pass-0.log /tmp/ffmpeg2pass-0.log.mbtree
```

### Container Remux (no re-encode)
```bash
# MKV to MP4
ffmpeg -n -i input.mkv -c copy -movflags +faststart output.mp4

# MP4 to MKV
ffmpeg -n -i input.mp4 -c copy output.mkv

# Any to WebM (requires VP9/AV1 video + Opus/Vorbis audio — may need re-encode)
ffmpeg -n -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -row-mt 1 \
  -c:a libopus -b:a 128k output.webm
```

### GPU Fallback Pattern
```bash
# Try GPU first, fall back to CPU
ffmpeg -n -hwaccel cuda -hwaccel_output_format cuda -i "$INPUT" \
  -c:v h264_nvenc -preset p5 -tune hq -rc constqp -cq 21 \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT" 2>/dev/null || \
ffmpeg -n -i "$INPUT" \
  -c:v libx264 -crf 20 -preset medium \
  -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
```

### Batch Transcoding
```bash
# Process all MKV files in a directory
for f in /path/to/input/*.mkv; do
  ffmpeg -n -hwaccel cuda -i "$f" \
    -c:v h264_nvenc -preset p5 -cq 21 \
    -c:a aac -b:a 192k -movflags +faststart \
    "/path/to/output/$(basename "${f%.mkv}.mp4")"
done
```

## NVENC Presets

| Preset | Speed | Quality | Use Case |
|--------|-------|---------|----------|
| p1 | Fastest | Lowest | Preview/drafts |
| p3 | Fast | Good | Quick exports |
| p4-p5 | Balanced | Very good | General use (recommended) |
| p6-p7 | Slow | Best | Final delivery |

NVENC supports up to **8 concurrent encoding sessions** on consumer GPUs.

## Container Compatibility

| Container | Video Codecs | Audio Codecs | Notes |
|-----------|-------------|-------------|-------|
| MP4 | H.264, H.265, AV1 | AAC, AC3, MP3 | Always add `-movflags +faststart` |
| MKV | Everything | Everything | Most flexible container |
| WebM | VP8, VP9, AV1 | Vorbis, Opus | Web-optimized |
| MOV | ProRes, H.264, H.265 | AAC, PCM | Apple/editing workflows |
| AVI | H.264, MPEG-4 | MP3, PCM | Legacy, avoid for new content |

## Quality Optimization Tips

- **Always use `-pix_fmt yuv420p`** for maximum compatibility (unless 10-bit needed)
- **Always add `-movflags +faststart`** for MP4 output (moves metadata to beginning for streaming)
- **Use `-tag:v hvc1`** for H.265 in MP4 (required for Apple device playback)
- **Stream copy** (`-c copy`) when only changing container — instant, lossless
- **CRF mode** is almost always better than target bitrate -- let the encoder decide

## Reference

Load `references/transcode.md` for codec comparison tables, two-pass encoding recipes, and container compatibility matrix.
