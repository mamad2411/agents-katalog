---
name: deck-file-size-optimizer
description: Cuts a bloated .pptx down by finding what is actually heavy — cropped pixels, uncompressed images, embedded media, orphan masters — and removing it without visible quality loss. Not for speeding up a slow-running animation.
---

# Deck File Size Optimizer

## When to use

Use this skill when a deck will not send, opens slowly, saves slowly, or is simply absurd for what is on the slides — the classic case being a 40-slide deck that weighs 180 MB and contains eight photographs. Also use it before a template ships firm-wide, because whatever bloat is in the template is inherited by every deck built on it. Do not use it for playback lag caused by animations or transitions; that is a rendering problem, not a size problem.

## What it does

It measures where the bytes actually are, then applies the fixes in descending order of payoff, and states the expected saving for each. The output is a before/after size with an itemised list of what was removed.

## Method

**1. Measure before you cut.** A `.pptx` is a ZIP container. Copy the file, rename the copy to `.zip`, and open it. What you are looking for:

- `ppt/media/` — every image, video and audio file, at its original size. Sort by size. This is nearly always where the weight is.
- `ppt/embeddings/` — embedded workbooks and OLE objects.
- `ppt/slideMasters/` and `ppt/slideLayouts/` — count them.
- `ppt/fonts/` — embedded fonts, a few hundred KB per weight.

Do this first. Guessing wastes an hour on a 200 KB problem while a single 90 MB video sits untouched.

**2. Delete cropped pixels.** This is usually the single biggest win and the least known. When you crop an image in PowerPoint, the cropped-away pixels are still in the file; the crop is a display instruction. A 24-megapixel photo cropped to a thumbnail still costs you 24 megapixels. Select a picture, then `Picture Format > Compress Pictures`, and tick **Delete cropped areas of pictures**. Untick *Apply only to this picture* to sweep the whole deck. This is destructive and cannot be undone after saving, so work on a copy.

**3. Compress images to the resolution the deck actually needs.** Same dialog, *Resolution*:

| Option | ppi | Use for |
|:--|:--|:--|
| HD | 330 | Large-format print, high-DPI display |
| Print | 220 | Normal printing |
| Web | 150 | On-screen presentation, sharing |
| E-mail | 96 | Email attachment, quick review |

For a deck that will only ever be projected or read on a laptop, 150 ppi is generous. Going from *Use document resolution* on a deck full of phone photos to 150 ppi routinely removes 80–90% of the file. Keep the uncompressed original elsewhere; this is one-way.

**4. Fix the sources, not just the compression.** Compression is a patch over the real cause:

- **Screenshots saved as PNG at 4K.** PNG is lossless and enormous for photographic content. Photographs belong as JPEG; flat graphics, screenshots of UI and anything with text stay PNG.
- **Vector logos pasted as 5000 px bitmaps.** Use the vector (EMF/SVG) or a correctly sized PNG.
- **The same image placed 30 times.** PowerPoint does deduplicate identical image parts, but only if they are genuinely identical bytes — a re-cropped or re-inserted copy becomes a new part. Insert once, then copy the shape.
- **Images inserted at native size and shrunk on the slide.** The full pixel count is still stored.

**5. Handle embedded media.** Video and audio dwarf everything else. On Windows, `File > Info > Compress Media` offers Full HD (1080p), HD (720p) and Standard (480p) and re-encodes in place; 720p is enough for a deck. Better still, link to a hosted video and keep it out of the file entirely — accepting that a linked video breaks when the deck travels without a connection. Decide which risk you prefer, and say so.

**6. Strip orphan masters and layouts.** A deck that has been merged from three sources carries three slide masters and thirty-odd layouts, most unused, each with its own background graphics. In `View > Slide Master`, PowerPoint shows how many slides use each layout on hover. Delete the masters and layouts nothing uses. Note that PowerPoint normally removes an unused master by itself — unless someone has right-clicked it and chosen **Preserve Master**, which pins it (a pin icon appears beside the thumbnail) and is exactly why the orphans survived. In the file this is the `preserve` attribute on the master. Unpin, then delete.

**7. Remove editing data and stop future bloat.** `File > Options > Advanced > Image Size and Quality`. Tick **Discard editing data** (drops the undo history retained for picture edits), leave **Do not compress images in file** unticked, and set **Default resolution** to the value the deck needs so newly inserted images arrive already sized. Setting these in the corporate template is the one fix that prevents the problem recurring.

**8. Clear the incidental leftovers.** Unused custom slide shows, leftover embedded workbooks behind charts that no longer need live data, hidden slides nobody will ever un-hide, and old comment threads. Individually small; collectively a few megabytes.

**9. Re-save and re-measure.** Save As a new file rather than saving over the original — a long-lived `.pptx` accumulates cruft that a fresh save discards. Then re-open the ZIP and confirm `ppt/media/` shrank. Check the heaviest images on screen at full-screen size before signing it off.

## Inputs

- The deck and its current size.
- Where it is going: email attachment (state the size limit), print, or on-screen only.
- Whether images will ever need to be printed at high resolution.
- Whether embedded video may be replaced by a link.

## Output format

- Before size, and the ZIP breakdown showing where the bytes were.
- An ordered list of actions taken, each with the bytes saved.
- After size, and the reduction as a percentage.
- Anything deliberately left alone, and why.
- Template-level changes recommended to stop it recurring.

## Example

Input: a 62-slide sales deck at 212 MB that bounces off a 25 MB mail gateway.

Output:

- Before: 212 MB. ZIP shows `ppt/media/` at 208 MB — one 96 MB MP4, 41 PNGs averaging 2.4 MB, three slide masters.
- Delete cropped areas across all pictures: −34 MB.
- Compress all pictures to 150 ppi (Web): −61 MB.
- Re-save six photographic PNGs as JPEG at source: −9 MB.
- Compress Media to 720p: −79 MB.
- Delete two orphan masters (both pinned with Preserve Master) and 19 unused layouts: −4 MB.
- Discard editing data, default resolution set to 150 ppi: −1 MB, and stops recurrence.
- After: 24 MB, a 89% reduction. Full-screen check on slides 4, 17 and 40 shows no visible loss.
- Left alone: the vector logo on the master, already 40 KB.
