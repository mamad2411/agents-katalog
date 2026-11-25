---
name: template-matching
description: "Use when a medical presentation must follow a supplied template or house style: a hospital, university or congress .pptx/.potx, a previous deck whose look should be copied, a brand guide, or a logo and colour set; also when converting a PowerPoint template's look into an HTML deck."
---

# Template matching

## Overview

The template is the user's institution speaking; reproduce it, don't reinterpret it.
Measure the template, write what you measured into `theme/theme.json`, and let both
builders read that file. Template elements (header bars, logos, footers, closing slides)
are never "slop" and never improved upon.

## Procedure

1. **Scan** the file:

   ```bash
   python scripts/scan_template.py template.pptx --out <talk>/theme --render
   ```

   This writes `scan.json`: slide size, theme colours, theme fonts, fonts actually used on
   slides, every layout and its placeholders, background images, and media with sizes. It
   also extracts the media files. `--render` exports a PNG of each slide when PowerPoint
   (Windows) or LibreOffice is installed.

2. **Look** at the renders. Background images often carry the real design (a coloured
   header band, a footer with the logo). Theme colours are often Office defaults that
   the template never uses. Sample colours from the renders or background images:

   ```bash
   python scripts/scan_template.py template.pptx --sample theme/media/image2.jpeg 500,40 500,700
   ```

3. **Write `theme/theme.json`** (shape below). Record geometry in the template's own
   proportions (fractions of slide width/height), so it maps onto 1920 × 1080 or 13.33 in.

4. **Note what not to copy**: watermarked stock photos, low-resolution logos (ask for the
   original file), 4:3 backgrounds stretched to 16:9. Put these in `theme/notes.md` and
   tell the user.

## `theme/theme.json`

```json
{
  "source": "template.pptx", "aspect": "16:9",
  "fonts": {"heading": "Arial", "body": "Arial", "serif_banner": "Times New Roman"},
  "colors": {"primary": "#09B1BE", "primary_dark": "#057E88", "rule": "#400D12",
             "title_text": "#FFFFFF", "accent": "#E8141B", "ink": "#1A1A1A",
             "muted": "#666666", "band": "#EBE8E3",
             "intervention": "#D7262E", "control": "#5B6B82"},
  "logo": {"file": "theme/logo.png", "position": "footer-right", "height_frac": 0.11},
  "layouts": {
    "title":   {"header_banner": true, "band_frac": [0.19, 0.71], "title_case": "upper", "title_color": "accent"},
    "content": {"header_frac": [0, 0.134], "header_rule_px": 6, "footer_frac": [0.852, 1],
                "title_case": "upper", "title_align": "center"},
    "closing": {"use": "title layout with thank-you text"}
  },
  "type_scale_px": {"title": 64, "subtitle": 34, "body": 24, "small": 20, "footer": 21}
}
```

Add `intervention` and `control` colours that fit the template and stay readable.
Check that they differ in lightness, so they survive colour-blindness and greyscale
printing.

## When there is no template

Propose a restrained palette from the brief (a hospital's brand colour if public, else a
neutral one). Ask the user to confirm it in one question with a rendered swatch, then write
`theme.json` the same way.
