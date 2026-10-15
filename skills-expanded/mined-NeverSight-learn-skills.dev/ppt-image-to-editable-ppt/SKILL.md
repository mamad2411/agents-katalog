---
name: ppt-image-to-editable-ppt
description: Convert PPT slide screenshots or exported slide images into editable PowerPoint decks. Use when Codex needs to extract image/icon/material assets from one or many slide images as separate PNGs, rebuild the slides with editable text boxes, native shapes, and movable picture objects, batch-process multiple page images, and merge the reconstructed pages into a complete .pptx file.
---

# PPT Image To Editable PPT

## Overview

Use this skill to turn slide images into a reconstructed, editable PowerPoint deck. The workflow is two-stage: first extract visual materials as PNG assets, then rebuild each page as PPT-native text, shapes, lines, and images.

This skill is for screenshots or exported slide pages, not for editing an existing native `.pptx` file. If a source `.pptx` exists, prefer editing that deck directly.

## Required Posture

Recreate the slide, do not screenshot it. Text must be editable PowerPoint text except for logos, seals, wordmarks, and decorative calligraphy that are better treated as visual assets. Icons and images must be separate picture objects. Simple frames, cards, circles, separators, and rules should be native shapes/lines.

For Chinese academic slides, preserve institution marks and purple/gray visual systems carefully. Use the original image as the visual reference, not as a full-slide background in the final deck.

## Workflow

1. Create a workspace beside the source images:
   - `assets/page_###/` for extracted PNGs
   - `layouts/page_###.layout.json` for editable reconstruction specs
   - `output/` for final PPTX files
   - `scratch/` for previews, reports, and temporary files

2. Inspect each source image:
   - record image dimensions
   - inventory all non-text visual materials
   - inventory all editable text
   - identify repeated templates across pages

3. Extract visual assets:
   - create an asset manifest JSON
   - run `scripts/asset_cropper.py`
   - inspect `_contact_sheet.png`
   - iterate until no obvious visual material is missing

4. Rebuild each slide:
   - create a layout JSON using source-image pixel coordinates
   - use editable text boxes for ordinary text
   - use native PPT shapes/lines for simple geometry
   - use the extracted PNGs for icons, logos, line art, photos, and complex decoration
   - build PPTX with `scripts/build_pptx_from_layout.py`

5. Batch and merge:
   - build representative pages first
   - for a deck, create one layout JSON per page
   - combine layouts with `scripts/combine_layouts.py`
   - export one final PPTX

6. QA:
   - run `scripts/inspect_pptx.py`
   - render or preview the saved PPTX when available
   - compare the preview against the source images
   - report output PPTX path, asset folder path, preview/report paths, and unresolved fidelity differences

## Read These References As Needed

- `references/asset-manifest.md`: asset crop manifest format and extraction modes.
- `references/layout-json.md`: editable PPT layout JSON schema.
- `references/reconstruction-sop.md`: full per-slide and batch checklist.

Read `asset-manifest.md` before writing crop manifests. Read `layout-json.md` before writing layout JSON. Read `reconstruction-sop.md` for batch jobs or when the slide is visually dense.

## Script Commands

Use the active Python environment. If `python-pptx` is missing, install it into that environment:

```bash
python -m pip install python-pptx
```

For image work, Pillow and NumPy are required. The Codex bundled workspace Python usually includes them.

Extract assets:

```bash
python /path/to/skill/scripts/asset_cropper.py \
  --manifest page_002.assets.json \
  --out-dir assets/page_002 \
  --contact-sheet
```

Build one or more slides from layout JSON:

```bash
python /path/to/skill/scripts/build_pptx_from_layout.py \
  --layout layouts/page_002.layout.json \
  --assets-root . \
  --out output/page_002_editable.pptx
```

Combine per-page layouts:

```bash
python /path/to/skill/scripts/combine_layouts.py \
  --layouts layouts \
  --out layouts/combined.layout.json
```

Inspect final PPTX:

```bash
python /path/to/skill/scripts/inspect_pptx.py \
  --pptx output/deck_editable.pptx \
  --report scratch/quality_report.json
```

## Extraction Decisions

Extract separately:

- logos, emblems, seals, wordmarks
- icons and pictograms
- photos, screenshots, chart screenshots when not reconstructing as data
- background campus/architecture line art
- footer/header decorative bands
- complex ribbons, tabs, badge shapes, paired flourishes
- reusable blank variants such as blank circles or empty ribbon tabs when useful

Do not extract:

- normal body text
- titles, section labels, captions, bullets, numbers that can be rebuilt as text
- simple rectangles, card frames, circles, and straight rules that can be native PPT shapes

Merge only when separate extraction adds no value, such as a footer band with many tiny decorative fragments or a paired title flourish intended to move together.

## Reconstruction Decisions

Use source-image pixel coordinates in layout JSON. Set `source_width` and `source_height` to the image size. The builder scales positions to the requested slide size.

Element order matters. Place backgrounds first, then large shapes, then image assets, then text.

Keep text boxes generous. PowerPoint, WPS, and preview renderers can use slightly different font metrics. Prefer wider boxes, explicit line breaks, and modest font-size adjustments over tight text regions.

For repeated page templates, create a reusable layout pattern and only swap text/image paths per page. For highly varied pages, rebuild each page individually.

## Validation Standard

A job is done only when:

- every meaningful visual asset from the source slide is either extracted as a PNG or intentionally rebuilt as a native shape
- ordinary text is editable in the PPTX
- PNG assets are independent picture objects and can be moved/replaced
- final PPTX passes package inspection with no empty media or placeholder text
- the saved PPTX preview has been visually compared against the source image, or the final response states why preview parity could not be rendered

Final responses should include the final `.pptx` path, extracted asset root, preview path if generated, QA command/report, and any known differences from the source image.
