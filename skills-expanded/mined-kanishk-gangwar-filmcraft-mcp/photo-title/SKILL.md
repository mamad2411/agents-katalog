---
name: photo-title
description: Build an animated title whose letters are made of photos — like the "2026" in year-recap reels, where each stroke of each digit is a different photo snapping in one after another — matching a reference's exact letter shapes (traced pixel for pixel) or a font, with clean anti-aliased edges, rendered as frames and baked for FilmCraft. Use it whenever an intro or title should be "made of photos", "stacked from pictures", a photo collage in the shape of text or a year, or when the user says the title's font or build-up doesn't match the reference.
---

# Photo-filled title

What users notice: the letter **shape** (it must look like the reference's font, not a similar one),
the **build-up** (pieces snapping in stroke by stroke in the reference's order and timing — a static
title "with stacking sound" is a failure), **clean edges** ("rough edges" read as unfinished), and
photos staying **inside their stroke** (no overflow across seams). Scripts need Pillow.

## 1. Study the reference title

With analyze-reference, extract the intro at full scale and look at:
- the finished title frame (shape, size as a fraction of the frame height, spacing)
- frames every 2–3 frames through the build-up: which piece appears when (pen order), how many frames
  between pieces, whether the first frame flashes the finished title, when each glyph starts
- whether photos inside are upright or sideways

## 2. Get the exact letter shape

Best: trace it from the reference's finished frame (lettering must sit on a dark background):
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/trace_mask.py ref_title_frame.png work/title_mask.png --box x0,y0,x1,y1
```
`--box` must contain only the lettering (no caption). Dark areas of the reference's own photos become
specks; small ones are filled automatically (raise `--speck` if holes remain, but not above the size of
real counters).
Otherwise use a font (`--font /path/Font.ttf --text 2026`); pick a heavy condensed face close to the
reference.

## 3. Render the animated title

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/photo_title.py --photos <photos dir> --out work/title \
  --mask work/title_mask.png --sideways --glyph-starts 6,22,40,54 --step 3 --frames 105 \
  --first-frame-full --reuse 2=0
```
- outline cleaned at 2x and anti-aliased; glyphs split into strokes along their own edges (bars across,
  strokes down), one photo per stroke, revealed top to bottom every `--step` frames from each glyph's
  start
- `--reuse 2=0`: a repeated character (the second "2") takes the cleaner trace of the first
- `--sideways`: photos rotated 90° as many reels do; omit for upright
- `--height-frac` letter height vs frame (match the reference); `--width/--height` your sequence size
Look at the finished frame and a few build-up frames side by side with the reference before going on.
If a glyph's strokes split oddly, check the trace (specks) first.

## 4. Use it

Import with `import_media(paths=[work/title/title_0000.png], imageSequence: true, bake: true)` and put
it at the start of V1 (plan `intro`). Never re-write frames of an already-imported sequence in place —
the app can keep showing stale frames; write a new folder and bake again. Confirm in the final render
with `check-render --intro-frames N` that the intro actually animates.
