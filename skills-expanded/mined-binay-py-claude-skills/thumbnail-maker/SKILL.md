---
name: thumbnail-maker
description: Make YouTube and social thumbnails (1280x720, plus 1080x1920 Shorts/Reels and 1200x630 link previews) with Pillow - a large auto-fitted title with one highlighted keyword on a clean flat or blurred-photo background, plus either a real screenshot with a hand-drawn red circle and arrow (tech and tutorial style), or a person photo/cut-out that can stand in front of the text. Checks readability at YouTube search size, the squint test, and YouTube's timestamp corner, and writes a preview sheet. Use when the user asks for a thumbnail, cover image, video title card or gig image.
---

# thumbnail-maker

`scripts/thumbnail.py` (with `scripts/fonts.py` next to it). Python 3.9+ and `pip install pillow`.

```
# tech / tutorial: a real screenshot, the important line circled, an arrow from the title
python thumbnail.py --title "Claude almost deleted *everything*" --style dark --shot terminal.png --circle 0.19,0.17,0.18 --arrow --out t.jpg

# talking-head: a cut-out person in front of the title
python thumbnail.py --title "I tested *every* AI coding tool" --style dark --photo me-cutout.png --out t.jpg

# photo background, Shorts size
python thumbnail.py --title "A day as a *dev*" --bg desk.jpg --style dark --size 1080x1920 --out short.jpg
```

| Option | What it does |
|---|---|
| `--title` | 3-5 words reads best. `*word*` marks the keyword (one box or color). Uppercased unless `--keep-case`. |
| `--style` | `dark` (near-black + yellow), `light` (off-white + red), or the louder `pop`, `red`, `green`, `tech`. |
| `--look` | `clean` (default): flat color with a soft vignette, or `--bg` photo blurred and darkened for contrast. `burst`: the older gradient + sunburst look. |
| `--shot img` | A real screenshot as the main visual. Wide crops (one or two lines of a terminal or UI) go full-width under the title; taller ones sit beside it. Scaled up to fill the space. |
| `--circle x,y,r` | Hand-drawn red oval on the screenshot. `x,y` = center and `r` = half-width of the thing, all as fractions of the screenshot. |
| `--arrow` | Hand-drawn arrow from the title to the circle (routes around the title when there's no room above). `--mark-color` changes the red. |
| `--photo img` | Person photo. A PNG with transparency (a cut-out) is outlined and drawn in front of the title edge for depth; a normal photo becomes a bordered card (`--photo-shape circle`, `--tilt`). |
| `--subtitle`, `--emoji`, `--accent`, `--highlight color`, `--size`, `--align`, `--font` | As before: a small second line, an emoji sticker, keyword color, colored keyword without a box, output size, alignment, title font. |

## Design rules (from what top thumbnails do in 2026)
- **One idea, 3-5 words.** The title complements the image; don't describe it.
- **Show the real thing.** A cropped screenshot of the actual error, result or UI beats generic art. Crop tight to the line that matters and circle it.
- **Faces:** a cut-out with a clear expression, large (40-60 % of the height). Don't put text over the eyes.
- **Two colors.** Flat background plus one accent. No sunbursts, emoji walls or gradient text; they read as template or AI-made.
- Keep the **bottom-right corner clear**: YouTube draws the video length there.

## Checks (printed, and on `<name>.preview.png`)
- Title letter height at 168 px wide (YouTube search) under 8 px → warning.
- Effective contrast of the title (fill vs background, and its outline) under 3:1 → warning.
- **Squint test:** the title area blurred to 48 px wide must still stand out from its surroundings.
- **Timestamp corner:** title reaching the bottom-right 20 % x 16 % → warning.
- Keyword box blending into the background, keyword vs box/outline contrast, more than 6 words.
Exit code 1 on any warning. LOOK at the preview sheet before using the image.

## Limits
- No background removal: pass a PNG that is already cut out (remove.bg, Photoshop, macOS "Copy Subject").
- Circles and arrows are placed from your `--circle` numbers: check the preview and adjust x/y/r if the oval misses.
- Fonts: Impact for titles (Windows/macOS; on Linux install `ttf-mscorefonts` or set `FONT_TITLE=/path/Anton-Regular.ttf`). Override with `FONT_TITLE`, `FONT_BOLD`, `FONT_EMOJI`.
- Devanagari (Hindi/Nepali) titles and subtitles switch to Mangal Bold / Nirmala UI automatically (`FONT_DEVANAGARI` overrides). Pillow without raqm (stock Windows) can't join conjuncts or place the short-i matra, so that text is shaped by ffmpeg's drawtext (HarfBuzz) word by word and composited in; mixed English + Nepali titles work. With no ffmpeg built with libharfbuzz on PATH the check warns instead, so read the preview.
- Characters the font can't draw (an emoji typed into `--title`, for example) are reported as a warning instead of silently becoming boxes.
- Emoji: single-codepoint only (Pillow without libraqm can't join ZWJ sequences).
- No face detection: crop photos so the face isn't near an edge.
