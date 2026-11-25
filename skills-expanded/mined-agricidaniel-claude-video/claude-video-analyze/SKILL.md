---
name: claude-video-analyze
description: >
  Video analysis and inspection using FFprobe and FFmpeg. Reads metadata, codec info,
  resolution, bitrate, duration, HDR status, keyframe structure, audio loudness,
  scene boundaries, and quality metrics (VMAF, SSIM, PSNR). Use when user says
  "analyze", "inspect", "info", "metadata", "quality", "VMAF", "SSIM", "PSNR",
  "scene detect", "keyframes", "HDR", "bitrate", "ffprobe", or "what codec".
allowed-tools:
  - Bash
  - Read
---

# claude-video-analyze — Video Analysis and Quality Assessment

All analysis operations are **read-only** and safe to auto-execute without confirmation.

## Quick Info (Most Common)

**Full metadata dump** (resolution, codec, duration, bitrate, audio, chapters):
```bash
ffprobe -v error -print_format json -show_format -show_streams -show_chapters "$INPUT"
```

**One-liner summary** (human-readable):
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,r_frame_rate,bit_rate,pix_fmt \
  -show_entries format=duration,size,bit_rate,format_name -of default "$INPUT"
```

## Specific Properties

**Resolution**:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$INPUT"
```

**Duration** (seconds):
```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$INPUT"
```

**Codec**:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=nw=1:nk=1 "$INPUT"
```

**Framerate**:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=nw=1:nk=1 "$INPUT"
```

**Bitrate** (video stream):
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=bit_rate -of default=nw=1:nk=1 "$INPUT"
```

**Pixel format**:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt -of default=nw=1:nk=1 "$INPUT"
```

**Audio info**:
```bash
ffprobe -v error -select_streams a -show_entries stream=codec_name,channels,sample_rate,bit_rate -of json "$INPUT"
```

## HDR Detection

```bash
ffprobe -v quiet -select_streams v:0 -show_entries stream=color_transfer,color_primaries,color_space \
  -of default=nw=1 "$INPUT"
```

| color_transfer | Meaning |
|---------------|---------|
| smpte2084 | HDR10 / Dolby Vision |
| arib-std-b67 | HLG |
| bt709 | SDR |
| Unknown/empty | Likely SDR |

## Keyframe Analysis

**List all keyframe timestamps**:
```bash
ffprobe -v error -select_streams v:0 -skip_frame nokey \
  -show_entries frame=pkt_pts_time -of csv=p=0 "$INPUT"
```

**Count keyframes**:
```bash
ffprobe -v error -select_streams v:0 -skip_frame nokey \
  -show_entries frame=pkt_pts_time -of csv=p=0 "$INPUT" | wc -l
```

**GOP structure** (I/P/B frame distribution):
```bash
ffprobe -v error -select_streams v:0 -show_entries frame=pict_type -of csv=p=0 "$INPUT" | \
  sort | uniq -c | sort -rn
```

## Scene Detection

**FFmpeg native** (fast, basic):
```bash
ffmpeg -i "$INPUT" -vf "scdet=s=1:t=14" -f null - 2>&1 | grep "lavfi.scd.time"
```

**PySceneDetect** (professional-grade, 5 algorithms):
```bash
# Adaptive detection (recommended for most content)
scenedetect -i "$INPUT" detect-adaptive -t 3.0 list-scenes

# Content-aware detection
scenedetect -i "$INPUT" detect-content -t 27.0 list-scenes

# Save scene images and split video
scenedetect -i "$INPUT" detect-adaptive -t 3.0 save-images split-video list-scenes
```

## Audio Loudness Measurement

```bash
ffmpeg -i "$INPUT" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | tail -12
```

Returns: `input_i` (integrated loudness), `input_tp` (true peak), `input_lra` (loudness range).

## Quality Assessment

### VMAF (Netflix perceptual quality, 0-100)

Compares distorted (encoded) vs reference (original):
```bash
ffmpeg -i distorted.mp4 -i reference.mp4 \
  -lavfi "libvmaf=model=version=vmaf_v0.6.1:log_fmt=json:log_path=vmaf_results.json" -f null -
```

| VMAF Score | Quality |
|-----------|---------|
| 93-100 | Excellent (indistinguishable from source) |
| 80-93 | Good (minor artifacts visible on close inspection) |
| 60-80 | Fair (noticeable quality loss) |
| <60 | Poor |

### SSIM and PSNR

```bash
# All three metrics at once
ffmpeg -i distorted.mp4 -i reference.mp4 \
  -lavfi "libvmaf=feature=name=psnr:feature=name=float_ssim:log_fmt=json:log_path=quality.json" -f null -
```

| Metric | Good | Excellent |
|--------|------|-----------|
| PSNR | >30 dB | >40 dB |
| SSIM | >0.95 | >0.98 |

### Optimal CRF Finder

Encode at multiple CRF values, measure VMAF for each, find the quality-size sweet spot:
```bash
for CRF in 18 20 22 24 26 28 30; do
  ffmpeg -y -i "$INPUT" -c:v libx264 -crf $CRF -preset medium "/tmp/crf_test_${CRF}.mp4"
  SIZE=$(stat -c%s "/tmp/crf_test_${CRF}.mp4")
  VMAF=$(ffmpeg -i "/tmp/crf_test_${CRF}.mp4" -i "$INPUT" \
    -lavfi "libvmaf=log_fmt=json:log_path=/tmp/vmaf_${CRF}.json" -f null - 2>&1 | \
    grep -oP 'VMAF score: \K[\d.]+')
  echo "CRF $CRF: ${SIZE} bytes, VMAF: $VMAF"
  rm -f "/tmp/crf_test_${CRF}.mp4" "/tmp/vmaf_${CRF}.json"
done
```

## Bitrate Analysis

**Average bitrate**:
```bash
ffprobe -v error -show_entries format=bit_rate -of default=nw=1:nk=1 "$INPUT" | awk '{printf "%.1f Mbps\n", $1/1000000}'
```

**Per-frame bitrate** (for variable bitrate analysis):
```bash
ffprobe -v error -select_streams v:0 -show_entries packet=size,pts_time -of csv=p=0 "$INPUT" | head -100
```

## Chapter Detection

```bash
ffprobe -v error -print_format json -show_chapters "$INPUT"
```

## Generate Comprehensive Report

For a full video report, run all of the above and format the output. Key sections:
1. File info (name, size, container format)
2. Video stream (codec, resolution, framerate, bitrate, pixel format, HDR status)
3. Audio stream(s) (codec, channels, sample rate, bitrate, loudness)
4. Chapters (if present)
5. Keyframe structure (GOP length, keyframe interval)
6. Recommendations (codec efficiency, loudness compliance, compatibility issues)

## Reference

Load `references/analyze.md` for VMAF/SSIM/PSNR quality metric details, scene detection parameters, and advanced FFprobe recipes.
