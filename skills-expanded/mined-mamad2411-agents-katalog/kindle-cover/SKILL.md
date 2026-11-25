---
name: kindle-cover
description: >
  Generate a full-wrap paperback cover PDF for Amazon KDP (front + spine + back in one file).
  Use this skill whenever the user wants to: create a book cover for KDP, make a paperback cover,
  generate a full wrap cover, design a book cover PDF, or needs a cover for Amazon self-publishing.
  Trigger for phrases like "book cover", "paperback cover", "KDP cover", "full wrap",
  "cover PDF", "spine + back cover", or when the user has a front cover image and needs
  the complete printable cover file.
---

# Kindle Cover — KDP Full Wrap Paperback Cover Generator

Generate a print-ready full-wrap cover PDF for Amazon KDP paperback books.
The output is a single PDF containing back cover, spine, and front cover — ready to upload to KDP.

## When to use this skill

- User has a front cover image and needs the full wrap (front + spine + back) PDF
- User is publishing a paperback on KDP and needs a cover file
- User wants to generate or regenerate a book cover with updated page count

## How it works

Run the bundled script:

```bash
python3 <skill-path>/scripts/generate_cover.py \
  --front-image <path-to-front-cover-image> \
  --title "Book Title" \
  --author "Author Name" \
  --pages <page-count> \
  --output <output-path.pdf> \
  --back-headline "Your hook headline" \
  --back-bullets "Bullet 1" "Bullet 2" "Bullet 3" \
  --back-tagline "Closing tagline" \
  --accent-color "#e040a0"
```

## Key parameters

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| `--front-image` | Yes | — | JPG/PNG of the front cover |
| `--title` | Yes | — | Book title for spine |
| `--author` | Yes | — | Author name for spine |
| `--pages` | Yes | — | Total page count (determines spine width) |
| `--output` | Yes | — | Output PDF path |
| `--trim` | No | `6x9` | Trim size: `5x8`, `5.5x8.5`, `6x9`, `8.5x11` |
| `--paper` | No | `white` | Paper type: `white` (0.002252"/page) or `cream` (0.0025"/page) |
| `--back-headline` | No | — | Main headline on back cover (max 3 lines) |
| `--back-subtitle` | No | — | Subtitle text below headline |
| `--back-bullets` | No | — | Feature bullet points (pass multiple strings) |
| `--back-cta` | No | — | Bold call-to-action line |
| `--back-tagline` | No | — | Italic tagline at bottom |
| `--accent-color` | No | `#e040a0` | Color for accent line and bullet dots |
| `--bg-color` | No | `#0a0a0a` | Back cover background color |
| `--spine-bg` | No | `#111111` | Spine background color |
| `--front-fit` | No | `cover` | How front image fills the area: `cover` (crop to fill) or `contain` (fit without cropping) |
| `--front-padding` | No | `0` | Padding in inches around front image (useful if title/author on image need breathing room) |

## KDP specs baked in

- **Bleed**: 0.125" on all sides (per KDP requirements)
- **Safe zone**: all text placed >= 0.375" from trim edges (KDP requirement for text)
- **Spine width**: calculated automatically from page count and paper type
- **No barcode placeholder**: Amazon places its own ISBN barcode at print time — the script does not add any barcode zone, rectangle, or placeholder

## Trim sizes supported

| Size | Paper width | Paper height |
|------|-------------|--------------|
| 5x8 | 5" | 8" |
| 5.5x8.5 | 5.5" | 8.5" |
| 6x9 | 6" | 9" |
| 8.5x11 | 8.5" | 11" |

## Tips for best results

- Front cover image should be high resolution (300 DPI ideal, minimum 1500px on short side)
- If front image has title/author text near edges, use `--front-padding 0.2` to prevent clipping
- Keep back cover headline to 2-3 short lines for readability
- 5-8 bullet points work well; more than 10 will crowd the back cover
- The accent color should contrast with the dark background — bright pinks, cyans, golds work well
- Spine text auto-sizes based on spine width; very thin spines (< 100 pages) may not fit text

## Dependencies

Requires `reportlab` and `Pillow`:
```bash
pip install reportlab Pillow --break-system-packages
```
