---
name: convert-image-to-jpg
description: Convert local image files from common raster formats into JPG while setting a target DPI (default 96). Use when Codex needs to convert a file or folder of images such as HEIC, HEIF, PNG, TIFF, WebP, BMP, GIF, AVIF, or JPEG into `.jpg` for upload, OCR, archiving, or tools that require JPEG output.
---

# Convert Image to JPG

## Core Goal
- Convert one local image or a directory tree of local images into `.jpg`.
- Write JPG DPI metadata as `96` by default or a caller-provided value.
- Preserve relative directory structure when the input path is a directory.

## Required Tools
- Use `scripts/convert_to_jpg.py`.
- Rely only on Python standard library modules. Do not install Python packages for this skill.
- Prefer `magick` when it is installed.
- Fall back to macOS `sips` when `magick` is unavailable.
- Stop and report the missing dependency when neither backend exists.

## Quick Start
1. Convert one file to a specific JPG path:

```bash
python3 scripts/convert_to_jpg.py \
  --input-path /path/to/image.heic \
  --output-path /path/to/output.jpg
```

2. Convert a directory recursively with custom DPI:

```bash
python3 scripts/convert_to_jpg.py \
  --input-path /path/to/input-images \
  --output-path /path/to/output-images \
  --dpi 300
```

3. Rewrite existing outputs in place or replace previous runs:

```bash
python3 scripts/convert_to_jpg.py \
  --input-path /path/to/input-images \
  --output-path /path/to/output-images \
  --overwrite
```

4. Preview the conversion plan without writing files:

```bash
python3 scripts/convert_to_jpg.py \
  --input-path /path/to/input-images \
  --output-path /path/to/output-images \
  --dry-run
```

## Behavior
- Treat directory input as recursive and keep the same relative subdirectories in the output tree.
- Treat single-file `--output-path` as a directory when it has no `.jpg` or `.jpeg` suffix.
- Convert `.jpg` and `.jpeg` inputs too. Use this to normalize output names or rewrite DPI metadata.
- Default JPG quality to `95`.
- Use the first frame or page when the source format can contain multiple frames, such as GIF or TIFF.
- Refuse ambiguous directory conversions when two source files would map to the same destination `.jpg`.
- Add uncommon extensions with `--extra-extension .ext` when needed.

## Main Arguments
- `--input-path`: source file or source directory
- `--output-path`: output JPG file path or output directory
- `--dpi`: target DPI metadata for the JPG output, default `96`
- `--quality`: JPG quality from `1` to `100`, default `95`
- `--backend`: `auto`, `magick`, or `sips`
- `--extra-extension`: additional directory-scan suffix to include
- `--overwrite`: replace existing outputs
- `--dry-run`: print the plan without converting files
- `--limit`: cap the number of files processed during a quick check

## Script
- `scripts/convert_to_jpg.py`
