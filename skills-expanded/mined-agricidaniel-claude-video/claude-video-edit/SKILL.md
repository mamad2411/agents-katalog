---
name: claude-video-edit
description: >
  Video editing operations using FFmpeg: trimming, cutting, splitting, concatenation,
  speed changes, cropping, scaling, rotation, overlays, picture-in-picture, green screen
  removal, video stabilization, transitions, fades, privacy blur, LUT color grading, and
  motion tracking text. Use when user says "trim", "cut", "split", "merge", "concat",
  "speed up", "slow down", "crop", "scale", "rotate", "overlay", "watermark", "pip",
  "green screen", "stabilize", "transition", "fade", "blur face", "privacy", "censor",
  "LUT", "color grade", or "tracking text".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-edit — Video Editing Operations

## Pre-Flight

Before every operation that writes a file:
1. Run `bash scripts/preflight.sh "$INPUT" "$OUTPUT"`
2. If it fails, stop and report the error to the user
3. For encoding operations, run `bash scripts/detect_gpu.sh` to choose encoder

## Operations

### Trimming

**Lossless trim** (keyframe-aligned, instant, no re-encode):
```bash
ffmpeg -n -ss HH:MM:SS -i "$INPUT" -t DURATION -c copy "$OUTPUT"
```
Note: `-ss` BEFORE `-i` for fast seeking. Duration in seconds or HH:MM:SS.

**Frame-accurate trim** (re-encodes, precise to any frame):
```bash
ffmpeg -n -i "$INPUT" -ss HH:MM:SS -t DURATION -c:v libx264 -crf 20 -c:a aac "$OUTPUT"
```
Note: `-ss` AFTER `-i` for frame accuracy. Use when precision matters.

**Remove first/last N seconds**:
- Remove first 10s: `-ss 10 -c copy`
- Remove last 10s: get duration with ffprobe, then trim to `duration - 10`

### Splitting

**Split at specific time**:
```bash
ffmpeg -n -i "$INPUT" -t 60 -c copy part1.mp4
ffmpeg -n -i "$INPUT" -ss 60 -c copy part2.mp4
```

**Split into equal segments**:
```bash
ffmpeg -n -i "$INPUT" -f segment -segment_time 300 -c copy -reset_timestamps 1 "segment_%03d.mp4"
```

**Split at scene boundaries** (load `references/analyze.md` for PySceneDetect):
```bash
scenedetect -i "$INPUT" detect-adaptive -t 3.0 split-video
```

### Concatenation

**Same codec (no re-encode)**:
```bash
printf "file '%s'\n" file1.mp4 file2.mp4 file3.mp4 > /tmp/concat_list.txt
ffmpeg -n -f concat -safe 0 -i /tmp/concat_list.txt -c copy "$OUTPUT"
rm /tmp/concat_list.txt
```

**Different codecs (re-encodes)**:
```bash
ffmpeg -n -i file1.mp4 -i file2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1" "$OUTPUT"
```

### Speed Changes

**Speed up 2x** (with audio pitch correction):
```bash
ffmpeg -n -i "$INPUT" -vf "setpts=0.5*PTS" -af "atempo=2.0" "$OUTPUT"
```

**Slow down 0.5x**:
```bash
ffmpeg -n -i "$INPUT" -vf "setpts=2.0*PTS" -af "atempo=0.5" "$OUTPUT"
```

**Speed factors**: For `atempo`, valid range is 0.5–100.0. For extreme changes, chain: `atempo=2.0,atempo=2.0` = 4x.

**Frame interpolation slow-motion** (AI-generated intermediate frames):
```bash
ffmpeg -n -i "$INPUT" -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:vsbmc=1" "$OUTPUT"
```
Warning: Very slow (~0.05x realtime). Best for short clips.

### Cropping, Scaling, Rotation

**Crop** (width:height:x:y):
```bash
ffmpeg -n -i "$INPUT" -vf "crop=640:480:100:50" "$OUTPUT"
```

**Scale** (keep aspect ratio, even dimensions):
```bash
ffmpeg -n -i "$INPUT" -vf "scale=1280:-2:flags=lanczos" "$OUTPUT"
```

**Scale to exact size with padding** (letterbox):
```bash
ffmpeg -n -i "$INPUT" -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" "$OUTPUT"
```

**Rotate** 90° clockwise: `-vf "transpose=1"`
**Rotate** 90° counter-clockwise: `-vf "transpose=2"`
**Rotate** 180°: `-vf "transpose=1,transpose=1"`
**Arbitrary angle**: `-vf "rotate=PI/6:fillcolor=black"`
**Flip** horizontal: `-vf "hflip"` | Vertical: `-vf "vflip"`

### Overlays and Watermarks

**Image watermark** (bottom-right with 10px margin):
```bash
ffmpeg -n -i "$INPUT" -i logo.png -filter_complex "overlay=W-w-10:H-h-10" "$OUTPUT"
```

**Picture-in-picture** (small video in corner):
```bash
ffmpeg -n -i "$INPUT" -i pip.mp4 -filter_complex "[1:v]scale=320:180[pip];[0:v][pip]overlay=10:10" "$OUTPUT"
```

**Text overlay**:
```bash
ffmpeg -n -i "$INPUT" -vf "drawtext=text='My Title':fontsize=48:fontcolor=white:x=(w-tw)/2:y=50:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:box=1:boxcolor=black@0.5:boxborderw=8" "$OUTPUT"
```

**Timed text** (show between 5s and 15s):
```bash
-vf "drawtext=text='Hello':enable='between(t,5,15)':fontsize=36:fontcolor=white:x=10:y=10"
```

### Green Screen (Chromakey)

```bash
ffmpeg -n -i greenscreen.mp4 -i background.mp4 -filter_complex \
  "[0:v]chromakey=0x00FF00:0.1:0.2[fg];[1:v][fg]overlay" "$OUTPUT"
```
Adjust color hex, similarity (0.1), and blend (0.2) for best results.

### Video Stabilization

Two-pass process using vidstab:
```bash
# Pass 1: Analyze motion
ffmpeg -i "$INPUT" -vf vidstabdetect=shakiness=5:accuracy=15:result=/tmp/transforms.trf -f null -

# Pass 2: Apply stabilization + sharpening
ffmpeg -n -i "$INPUT" -vf "vidstabtransform=smoothing=10:input=/tmp/transforms.trf,unsharp=5:5:0.8:5:5:0.3" "$OUTPUT"

rm /tmp/transforms.trf
```
`shakiness` 1-10 (how shaky is source), `smoothing` (higher = smoother camera, may crop edges).

### Transitions

**Cross-fade between two clips** (44+ transition types available):
```bash
ffmpeg -n -i first.mp4 -i second.mp4 -filter_complex \
  "xfade=transition=fade:duration=2:offset=5" "$OUTPUT"
```

**Available xfade transitions**: fade, dissolve, wipeleft, wiperight, wipeup, wipedown, slideleft, slideright, slideup, slidedown, circlecrop, rectcrop, distance, fadeblack, fadewhite, radial, smoothleft, smoothright, smoothup, smoothdown, circleopen, circleclose, vertopen, vertclose, horzopen, horzclose, diagtl, diagtr, diagbl, diagbr, hlslice, hrslice, vuslice, vdslice, pixelize, squeezeh, squeezev, zoomin, fadegrays, wipetl, wipetr, wipebl, wipebr, coverleft, coverright, coverup, coverdown, revealleft, revealright, revealup, revealdown.

**Fade in/out**:
```bash
# Fade in first 2 seconds
ffmpeg -n -i "$INPUT" -vf "fade=t=in:st=0:d=2" -af "afade=t=in:st=0:d=2" "$OUTPUT"

# Fade out last 2 seconds (get duration first with ffprobe)
ffmpeg -n -i "$INPUT" -vf "fade=t=out:st=OFFSET:d=2" -af "afade=t=out:st=OFFSET:d=2" "$OUTPUT"
```

### Color Correction

Load `references/filters.md` for the full filter catalog. Quick reference:

- **Brightness/contrast**: `-vf "eq=brightness=0.06:contrast=1.2:saturation=1.3"`
- **Tone curves preset**: `-vf "curves=preset=lighter"` (also: darker, increase_contrast, vintage, etc.)
- **Color balance**: `-vf "colorbalance=rs=0.3:gs=-0.1:bs=0.0"`
- **3D LUT**: `-vf "lut3d=file=my_lut.cube"`
- **Grayscale**: `-vf "colorchannelmixer=.3:.4:.3:0:.3:.4:.3:0:.3:.4:.3"`
- **Blur**: `-vf "gblur=sigma=10"`
- **Sharpen**: `-vf "unsharp=5:5:1.0:5:5:0.0"`
- **Denoise**: `-vf "hqdn3d=4:3:6:4.5"` (fast) or `-vf "nlmeans=s=3.5:p=7:r=15"` (best quality)

### Contact Sheet / Thumbnail Grid

```bash
ffmpeg -n -i "$INPUT" -vf "select=not(mod(n\,100)),scale=320:180,tile=4x4" -frames:v 1 contact_sheet.png
```

### Extract Single Frame

```bash
ffmpeg -n -ss 00:01:30 -i "$INPUT" -frames:v 1 -q:v 2 thumbnail.jpg
```

### Privacy Blur (Face/Region Censoring)

**Blur entire face region** (static coordinates — use ffprobe or MediaPipe to find face bounding box):
```bash
ffmpeg -n -i "$INPUT" -vf "delogo=x=200:y=100:w=150:h=150" "$OUTPUT"
```

**Box blur a region** (more control):
```bash
ffmpeg -n -i "$INPUT" -filter_complex \
  "[0:v]crop=150:150:200:100,boxblur=10[blur];[0:v][blur]overlay=200:100" "$OUTPUT"
```

**Blur with time range** (only blur between 5s and 15s):
```bash
ffmpeg -n -i "$INPUT" -filter_complex \
  "[0:v]split[main][copy];[copy]crop=150:150:200:100,boxblur=10[blur];[main][blur]overlay=200:100:enable='between(t,5,15)'" "$OUTPUT"
```

**Full-frame blur** (for B-roll background):
```bash
ffmpeg -n -i "$INPUT" -vf "boxblur=20:5" "$OUTPUT"
```

For AI-powered face detection + tracking blur across frames, use `python3 scripts/face_tracker.py`
with MediaPipe BlazeFace (CPU, no VRAM needed). The face_tracker outputs bounding boxes per frame
that can drive the overlay blur coordinates.

### LUT Color Grading

**Apply a .cube LUT file**:
```bash
ffmpeg -n -i "$INPUT" -vf "lut3d=file=my_grade.cube" "$OUTPUT"
```

**Apply with intensity control** (blend between original and graded):
```bash
ffmpeg -n -i "$INPUT" -filter_complex \
  "[0:v]split[a][b];[b]lut3d=file=my_grade.cube[graded];[a][graded]blend=all_mode=normal:all_opacity=0.7" "$OUTPUT"
```

**Common LUT sources**: Download .cube files from sites like lutify.me, filtergrade.com, or
create custom LUTs in DaVinci Resolve. Place LUT files alongside the project or use absolute paths.

**Supported formats**: `.cube` (most common), `.3dl`, `.dat`, `.m3d`

### Motion Tracking Text Overlay

**Static text that follows a position** (manual keyframes):
```bash
ffmpeg -n -i "$INPUT" -vf "drawtext=text='Label':fontsize=24:fontcolor=white:\
x='if(lt(t,5),100+t*20,200)':y='if(lt(t,5),50+t*10,100)':\
fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:\
box=1:boxcolor=black@0.5:boxborderw=4" "$OUTPUT"
```

**Text with expression-based movement** (smooth sine wave):
```bash
ffmpeg -n -i "$INPUT" -vf "drawtext=text='Moving Text':fontsize=36:fontcolor=white:\
x='w/2-tw/2+50*sin(t*2)':y='h/2-th/2+30*cos(t*2)':\
fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" "$OUTPUT"
```

For complex tracking (follow a face or object through a video), combine `scripts/face_tracker.py`
bounding box output with per-frame drawtext coordinates. Export face centers from the tracker,
then generate a drawtext filter with frame-by-frame x/y expressions.

## Output Naming Convention

When user doesn't specify output name, derive it from input:
- `video.mp4` → `video_trimmed.mp4`, `video_stabilized.mp4`, `video_2x.mp4`, etc.
- For batch: `video_001.mp4`, `video_002.mp4`, etc.
