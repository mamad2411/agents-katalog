---
name: convert-images-to-pdf
description: Turn a folder of slide images (macOS screenshots of a DocSend or Drive deck, exported PNGs, phone photos of pages) into one lean 16:9 PDF deck, legible on a retina laptop at about 50–80 KB a page. Use whenever the user hands over a folder of deck screenshots or slide images and wants a PDF; says "stitch these into a PDF", "make a deck PDF from these screenshots", "convert images to PDF", "the deck is just PNGs"; or before feeding a screenshot deck to the memopop orchestrator (deals/<deal>/inputs/) or a dididecks deal slide. Encodes the settled settings (long side 1600 px, JPEG q85 optimize, assembled with PyMuPDF, not img2pdf, Ghostscript or ImageMagick), capture-time page order for macOS screenshots (earliest = page 1, which filename sort gets wrong), the unanimous-box viewer-chrome crop, and the DocSend-watermark warning. Composes with slim-file-sizes (for a deck that is already a PDF) and setup-new-firm (where the PDF lands).
---

# Convert Images to PDF

> **The one thing to remember:** 1600 px on the long side, JPEG q85, PyMuPDF.
> That combination was measured, not guessed: a 28.0 MB retina-screenshot deck
> came out at 1.4 MB with every slide still readable at 100%. Don't re-litigate
> it per deck. If one chart-heavy deck smears, raise *that deck* to q92.

## Run it

```bash
S=~/code/lossless-monorepo/context-v/agent-skills/convert-images-to-pdf/scripts
uv run --script $S/images-to-pdf.py <folder> -o <deck>.pdf --dry-run   # check the page order first
uv run --script $S/images-to-pdf.py <folder> -o <deck>.pdf
# window captures with browser chrome: measure the slide box, then crop to it
uv run --script $S/images-to-pdf.py <folder> -o <deck>.pdf --measure
uv run --script $S/images-to-pdf.py <folder> -o <deck>.pdf --crop 3282x1846+199+306
```

The script declares its own dependencies (PEP 723), so `uv` installs them on
first run. Add `--crop-chrome` when the screenshots include the viewer's
toolbars. The script never overwrites its output and never deletes an input.

## The settings, and why

| Setting | Value | Why |
|---|---|---|
| Long side | **1600 px** (`--max-long`) | 16:9 → 1600×900. That's about 150 DPI across a 10.6" slide, the orchestrator's settled render density (`deck_analyst.py`). Retina screenshots come in 2–3× larger, and that excess is the waste. |
| Encoding | **JPEG q85, `optimize=True`** | PNG→JPEG is the big win. q85 keeps slide text clean; q70 is only for vision triage thumbnails. |
| Assembler | **PyMuPDF** (`new_page` + `insert_image`) | Each page is sized to its image, so there's no letterboxing and no re-encode. It's already in the orchestrator's lockfile. The plan that settled this says outright: don't reach for `img2pdf` or Ghostscript. |
| Alpha | Flattened onto white | JPEG has no alpha. A transparent PNG otherwise turns black. |
| Orientation | EXIF applied | Phone photos of pages otherwise come in sideways. |

Higher: `--max-long 1920` for decks with tiny chart labels or dense tables.
Lower: don't go under 1400. Below that, footnotes and axis labels stop reading.

Sanity check on the output: **about 40–100 KB a page.** A 20-slide deck should land
around 1–2 MB. Well over 150 KB a page means the cap didn't apply. Under 30 KB
a page means you should look at a dense slide before trusting it.

## Page order: the part that silently goes wrong

macOS screenshot names (`Screenshot 2026-11-22 at 9.05.03 AM.png`) carry the
capture time, and **capture order is page order, earliest = page 1.** A filename
sort gets this wrong: `10.01.00 AM` sorts before `9.05.03 AM`, and PM before AM
across noon. The orchestrator's `slim_deck.py` sorts by filename, which is
why this skill exists.

- `--order auto` (default): capture time if *every* file is a macOS screenshot
  name, else a natural sort (`slide-2` before `slide-10`).
- Duplicate-second captures (`… (2).png`) sort after their twin.
- Always run `--dry-run` first and look at the list. Missing pages show up
  here, not after the memo is written. (One deal deck was 13 of 15 pages
  captured.)

## Before you stitch

1. **One folder per document.** For a dataroom, use
   `inputs/dataroom__<Deal>/<DocName>__<Deal>/`, one PDF per folder.
2. **Watermarks.** DocSend stamps the viewer's email or name on each page. The
   memopop deck analyst has extracted a DocSend watermark *as the company name*.
   Crop it out, or tell the user before the run.
3. **Viewer chrome. Look at page 1 before stitching.** Two kinds:
   - *Slide area only, with toolbars above and below:* `--crop-chrome` crops
     only when every page agrees on the same slide box, and otherwise crops
     nothing. Crop nothing rather than crop content.
   - *Whole-window capture* (macOS window screenshot: a drop shadow, the browser
     frame, the "Dropbox DocSend" bar): `--crop-chrome` can't see the slide
     edges. Run `--measure` on the folder. It prints the slide box in the first
     image as `WxH+X+Y` with its ratio. If the ratio is 1.778 (16:9), pass that
     box with `--crop`. Check that every screenshot has the same pixel size
     first, because a fixed box assumes one window size. Measured on a 13-slide
     DocSend deck (2026-11-22): 3680×2392 window captures, box
     `3282x1846+199+306`, 25.7 MB → 1.6 MB.
4. **Confidentiality.** A founder's deck stays in a private repo (`io/<firm>/`,
   a client-site). Loose `Screenshot *.png` files at a deal root are
   gitignored by `setup-new-firm`. The stitched PDF in `inputs/` is the
   canonical copy.

## Verify, then report

- Open page 1 and the densest chart or table page at 100% on a retina screen.
- Report: page count, page px, source MB → PDF MB, KB per page.
- The PDF is raster: no selectable text, no links. That's fine for a memo input
  (the analyst reads it with vision). If the founder's deck had live links that
  matter, ask for their real PDF and run it through `slim-file-sizes` instead.

## Don't

- Don't use `img2pdf`, Ghostscript or ImageMagick `magick *.png deck.pdf` for
  this. ImageMagick's glob sorts by name (wrong order) and keeps full retina
  pixels unless you remember every flag.
- Don't write WebP into the PDF. Not every PDF reader handles it.
- Don't delete the source screenshots until the user has looked at the PDF.

## Lineage

- `ai-labs/memopop-ai/apps/memopop-orchestrator/scripts/slim_deck.py`, which is
  the source of these settings and the chrome crop. It also emits per-page JPEGs
  for DidiDecks Play-UI slides, so use it when you need those.
- `ai-labs/context-v/plans/Quick-Slides-Assembly-to-Demo-Deal-Coverage.md`, where
  the library choice and the 28.0 → 1.4 MB measurement are recorded.
- `memopop-orchestrator/src/agents/deck_analyst.py`: 150 DPI, q85.
