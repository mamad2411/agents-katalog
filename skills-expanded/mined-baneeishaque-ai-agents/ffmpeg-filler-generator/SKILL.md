---
name: ffmpeg-filler-generator
description: Base primitive — generate a filler/transition video segment with black background, centered text overlay, and silent audio, with configurable codecs and duration.
category: Media-Processing
---

# FFmpeg Filler Generator Skill (v1) — Base

This is a **base** skill. It generates a short filler/transition video segment: a black background with centered
text overlay and silent audio track. The video and audio codecs are configurable (defaults: VP9 + Opus for webm
compatibility).

The filler is generated in two stages:

1. **Pillow** — renders the text overlay as a PNG image (black canvas, white + gray centered text, auto-sized font).
2. **ffmpeg** — encodes a `color` source + `anullsrc` silent audio + the overlay PNG into a single video file via
   the `overlay` filter.

The skill is intended to be **composed by higher-level skills** (e.g. meeting-recording merge, podcast editor,
slide-show chapter card generator) that need a transition segment with custom text.

***

## 1. Scope & Intent

- **In scope**: Accept video dimensions, frame rate, audio sample rate, duration, text/subtext, codec selection,
  and an output path. Generate a filler video file with black background, centered text overlay, and silent audio.
- **Out of scope**:
    - Probing source media files for dimensions (caller supplies them).
    - Concatenating filler with other segments (use sibling
      [`ffmpeg-lossless-concat`](../ffmpeg-lossless-concat/SKILL.md)).
    - Any non-filler video generation (slides, animations, transitions other than static text).

***

## 2. Composition Rationale

This skill is a **base** — it owns the generic primitive "generate a static-text filler/transition video segment."
Multiple domain-specific composers reuse this primitive:

- [`webm-recording-merge-with-filler`](../webm-recording-merge-with-filler/SKILL.md) — probes the first recording
  segment for dimensions, then calls this skill's script to generate a "Recording interrupted" filler that matches
  the source codecs, before losslessly concatenating.
- Any future skill that needs a transition card (podcast gap filler, security-camera "no signal" segment, video
  chapter divider) should invoke this skill rather than re-deriving the Pillow + ffmpeg incantation.

The layering test: *"Could a different domain need the same primitive?"* — **YES**. Inlining the filler generation
into a composer would split the SSOT across every consumer.

***

## 3. Environment & Dependencies

### 3.1 Required Tools

- **ffmpeg** 5.0+ — The `color` and `anullsrc` lavfi sources and `overlay` filter must be available. Verify:

  ```bash
  ffmpeg -version | head -1
  ```

- **Python 3.12+** — With **Pillow** (`pip install Pillow`) for text overlay image generation. Verify:

  ```bash
  python3 -c 'from PIL import Image; print("Pillow:", Image.__version__)'
  ```

- **Required ffmpeg encoders** (match your target codecs). For the default VP9 + Opus:

  ```bash
  ffmpeg -encoders 2>/dev/null | grep -q libvpx-vp9 && echo "VP9 encoder OK"
  ffmpeg -encoders 2>/dev/null | grep -q libopus && echo "Opus encoder OK"
  ```

### 3.2 Verification

```bash
which ffmpeg python3
python3 -c 'from PIL import Image; print("Pillow:", Image.__version__)'
ffmpeg -encoders 2>/dev/null | grep -iE "vp9|opus" | head -4
```

If any tool is missing, consult the [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) skill.
If Pillow is missing, install it with `pip install Pillow` or `brew install pillow`.

***

## 4. Protocol

### 4.1 Step 1 — Determine Dimensions

The caller MUST supply the video width, height, and frame rate — these are not probed automatically (the base skill
is domain-agnostic). For webm recordings, use `ffprobe` on a source segment:

```bash
ffprobe -v quiet -print_format json -show_streams source.webm | python3 -c "
import json,sys
d = json.load(sys.stdin)
for s in d['streams']:
    if s['codec_type'] == 'video':
        print(f\"width={s['width']} height={s['height']} fps={s.get('r_frame_rate','30/1')}\")
        break
for s in d['streams']:
    if s['codec_type'] == 'audio':
        print(f\"sample_rate={s.get('sample_rate','48000')}\")
        break
"
```

### 4.2 Step 2 — Run the Filler Generator

```bash
python3 .agents/skills/ffmpeg-filler-generator/scripts/generate_filler.py \
    --width 1920 --height 1080 \
    --fps "30/1" \
    --sample-rate 48000 \
    --duration 3 \
    --text "Recording interrupted" \
    --subtext "— content missing —" \
    --output /path/to/filler.webm
```

The script:

1. Generates a Pillow PNG overlay (black canvas, white primary text + gray secondary text, centered, auto-sized font
   with system font fallback chain).
2. Runs ffmpeg to encode a filler video:
   - `color` source for black background at the specified dimensions, fps, and duration.
   - `anullsrc` for silent audio at the specified sample rate (stereo).
   - The overlay PNG is composited via the `overlay` filter.
   - Encoded with the specified video codec (default `libvpx-vp9`) and audio codec (default `libopus`).
3. Cleans up the temporary overlay PNG.
4. Exits 0 on success, 1 on failure (with ffmpeg stderr captured).

#### 4.2.1 Flag Breakdown

| Flag | Purpose |
| :--- | :--- |
| `--width <px>` | Video width in pixels (required). |
| `--height <px>` | Video height in pixels (required). |
| `--fps <rate>` | Frame rate as rational string, e.g. `30/1`, `60/1` (default `30/1`). |
| `--sample-rate <hz>` | Audio sample rate (default `48000`). |
| `--duration <sec>` | Filler duration in seconds (required). |
| `--text <str>` | Primary text displayed on the filler (default "Recording interrupted"). |
| `--subtext <str>` | Secondary subtitle text below the primary (default "— content missing —"). |
| `--codec-video <name>` | Video encoder name (default `libvpx-vp9`). |
| `--codec-audio <name>` | Audio encoder name (default `libopus`). |
| `--output <path>` | Path for the output filler video file (required). |

### 4.3 Step 3 — Verify Output

```bash
# Confirm output exists and is non-empty
ls -lh /path/to/filler.webm

# Check stream parameters
ffprobe -v quiet -show_entries stream=codec_name,width,height /path/to/filler.webm

# Confirm duration matches requested
ffprobe -v quiet -show_entries format=duration /path/to/filler.webm
```

The output file MUST have:

- The requested video codec and dimensions.
- The requested audio codec (or none if `--codec-audio` is empty).
- Duration exactly matching `--duration` (within keyframe-boundary precision).

***

## 5. Edge Cases & Constraints

- **Missing Pillow**: The script imports `PIL` and exits with `ModuleNotFoundError` if Pillow is not installed.
  The error message suggests the install command.
- **No system font found**: The script tries macOS Helvetica, falls back to Linux font paths, then falls back to
  PIL default bitmap font (small, mono, pixelated). The filler is usable but less polished.
- **Very small dimensions** (< 200 px): The auto-sized font may be too large for the canvas; the fallback font
  may produce clipped text. For very small fillers, consider using the `--text` with short strings.
- **Unsupported codec**: If ffmpeg does not have the requested encoder, it exits 1 with an error. Verify encoders
  with `ffmpeg -encoders` before running.
- **Container mismatch**: The output container is determined by the file extension. Ensure the container supports
  the chosen codecs (e.g. `.webm` for VP9 + Opus, `.mp4` for H.264 + AAC).

***

## 6. Prohibited Actions

- The Agent MUST NOT probe source media files inside this base skill — that is the domain of the caller (composer).
- The Agent MUST NOT modify the filler text, font, or styling beyond what the CLI flags expose. If a composer needs
  different styling (e.g. colored background, logo overlay), it should generate its own overlay image and pipe it
  into ffmpeg directly rather than modifying this base script.
- The Agent MUST NOT leave the temporary overlay PNG on disk after the script completes.

***

## 7. Script Reference

[`scripts/generate_filler.py`](./scripts/generate_filler.py) performs:

1. Parse all CLI arguments.
2. Ensure the output directory exists.
3. Call `generate_overlay_image()` which creates a Pillow `Image.new("RGB", (width, height), "black")`, draws
   primary text (white) and subtext (gray) centered, and saves to a temporary `.filler_overlay.png` path.
4. Call `generate_filler()` which runs:

   ```bash
   ffmpeg -y -f lavfi -i "color=c=black:s={w}x{h}:r={fps}:d={dur}" \
          -f lavfi -i "anullsrc=r={rate}:cl=stereo:d={dur}" \
          -i overlay.png \
          -filter_complex "[0:v][2:v]overlay=0:0" \
          -c:v {codec_video} -crf 10 -b:v 0 \
          -c:a {codec_audio} -b:a 256k \
          {output}
   ```

5. Remove the temporary overlay PNG.
6. Exit 0 on success, 1 on failure (ffmpeg stderr captured).

***

## 8. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
| :--- | :--- |
| [`webm-recording-merge-with-filler`](../webm-recording-merge-with-filler/SKILL.md) | Calls `scripts/generate_filler.py --width <w> --height <h> --fps <fps> --sample-rate <rate> --duration <sec> --text "<text>" --subtext "<subtext>" --output <filler.webm>` after probing the first source segment for dimensions. Consumes exit code only; does not parse stdout. |

***

## 9. Related Skills

- [FFmpeg Lossless Concat](../ffmpeg-lossless-concat/SKILL.md) — sibling base skill for lossless concatenation;
  composers often call both skills in sequence (filler-generator then concat).
- [FFmpeg Lossless Split](../ffmpeg-lossless-split/SKILL.md) — sibling base skill for lossless timestamp-based
  splitting; may be used before filling to trim a continuation recording.
- [WebM Recording Merge with Filler](../webm-recording-merge-with-filler/SKILL.md) — composer that invokes this
  base skill as the first stage of its pipeline.
- [WebM Recording Interrupted Recovery](../webm-recording-interrupted-recovery/SKILL.md) — composer that
  transitively uses this skill via the filler-merge composer.
- [System-Wide Tool Management](../system-wide-tool-management/SKILL.md) — installs ffmpeg / Python / Pillow
  if any dependency is missing.
