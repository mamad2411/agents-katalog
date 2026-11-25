---
name: kappmaker-image-tools
description: Edit and process existing images for a KAppMaker app — split a grid image into pieces, remove backgrounds, enhance quality, and convert to WebP. Use when the user asks to crop, split, clean up, upscale, remove the background from, or optimise an image they already have.
---

# KAppMaker — Image Tools

## Before running any command

1. **Prerequisites** — `kappmaker --version` (install: `npm i -g kappmaker`). If a credential is
   missing the CLI says so; re-run `kappmaker config init`.
2. **Read `AiGuidelines/` first** — the PRD, positioning and UI spec already answer most questions.


### image-split — Grid Image Splitter

**Syntax**: `kappmaker image-split <source> [options]`

**Options**:
- `--rows <n>` (default: 4)
- `--cols <n>` (default: 4)
- `--zoom <factor>` (default: 1.07)
- `--gap <pixels>` (default: 0)
- `--width <pixels>` (default: 512)
- `--height <pixels>` (default: 512)
- `--output-dir <path>` (default: current directory)
- `--keep <indices>` — Comma-separated tile indices to keep (e.g., `1,3,5`)

**Prerequisites**: None (uses local sharp library).

**Common use cases — ALWAYS pass explicit `--rows`/`--cols`/`--width`/`--height` matching the source grid. The defaults (4×4, 512×512) are tuned for logo grids only — using them on a screenshot grid will produce a wrong split (e.g. 2 half-images each containing a 2×2 sub-grid of screenshots).**

| Use case | Source layout | Recommended args |
|---|---|---|
| Logo grid (from `create-logo`) | 4 rows × 4 cols, 16 cells | defaults are fine, or `--rows 4 --cols 4 --width 512 --height 512` |
| **Marketing screenshot grid (from `generate-image` or fal.ai)** | **2 rows × 4 cols, 8 cells** | **`--rows 2 --cols 4 --width 1284 --height 2778`** |

Note: `generate-screenshots` already splits its own output internally into `appstore/` and `playstore/` directories — you do **not** need to run `image-split` after it. Only run `image-split` on a screenshot grid if the user generated it some other way (e.g. via `generate-image` with `--reference`).

---

### image-remove-bg — Background Removal

**Syntax**: `kappmaker image-remove-bg <source> [--output <path>]`

**Prerequisites**: `falApiKey` (prompted on first use if not set).

---

### image-enhance — Quality Enhancement

**Syntax**: `kappmaker image-enhance <source> [--output <path>]`

**Prerequisites**: `falApiKey` (prompted on first use if not set).

---

### convert-webp — Image to WebP Conversion

**Syntax**: `kappmaker convert-webp <source> [options]`

**Options**:
- `--quality <n>` — WebP quality, 0–100 (default: 75)
- `--recursive` — Search directories recursively (default: false)
- `--delete-originals` — Delete original files after conversion (default: false)
- `--output <dir>` — Output directory (default: same directory as source)

**Prerequisites**: None (uses local sharp library, no API key needed).

**What it does**: Converts PNG, JPG, JPEG, BMP, TIFF, and GIF images to WebP format — similar to Android Studio's built-in converter. Shows before/after file sizes and percentage saved for each file. Works on single files or entire directories (with `--recursive`).

---

## Where this sits in the flow

- **Before this:** **kappmaker-image** or **kappmaker-logo** produced the source image.
- **After this:** —
