---
name: slim-file-sizes
description: Shrink the files founders send — datarooms, decks, PDFs, video, images, zips — to the lightest format at the smallest size that is still legible on a retina laptop, one file at a time, verified and logged. Use whenever a dataroom or deck folder is downloaded or unzipped; whenever a repo, Cloudflare Artifacts repo or drive is near a size limit (e.g. getting a client's humain-fs under Artifacts' 1 GB per repo); whenever the user says "compress", "shrink", "slim down", "this folder is huge", "convert the decks to PDF", "get rid of the pptx", "why is this 100MB"; or before committing binary files anywhere. Encodes the legibility settings per file type (PDF images to 200 dpi with text kept vector, decks exported by Keynote/PowerPoint, 720p video, WebP images), the one-script-per-kind rule with an agent judging each file, the verify-then-delete order, and the per-folder transform log.
---

# Slim File Sizes

> **The one thing to remember: convert every file, one at a time, and check
> each one before the original goes.** Founders send whatever they have: 100MB
> decks with an 80MB video inside, 170MB PDFs of photos, zips already
> unpacked beside themselves. We only need the content to read the dataroom
> and analyze the deck. If something goes wrong, we ask the company for the
> file again.

## The standard: legible, not a byte budget

There are no size caps here. The test is human:

- **Text stays text.** A PDF that had selectable text still has it, with the
  same characters. Fonts stay vector, so they are sharp at any zoom.
- **It reads cleanly on a retina laptop at 100%.** A reading column is about
  800 CSS px, which is 1600 real pixels. Full screen is about 2560.
- **The format is the lightest one that holds the content.** Nobody needs a
  `.pptx`, `.key` or `.docx` back. We are not photographers or designers.

Every file goes through, not just the ones that look large. A 2MB deck that
could be 600KB is the same problem, a few hundred times over.

## What becomes what

| Input | Output | Script | Setting that still looks right | Watch for |
|---|---|---|---|---|
| PDF with text | PDF | `pdf-compress.sh` | Images to 200 dpi, JPEG q80; text and fonts untouched | The script refuses if text is lost, a page looks different, or the file grows. Fallback: `ocrmypdf --skip-text -O2` (touches only images) |
| PDF of images only (screenshot decks, scans) | PDF | `pdf-compress.sh` | Same | Has no text to begin with; `ocrmypdf --optimize 2` adds a text layer, which helps analysis |
| `.key` | PDF, then compress | `deck-to-pdf.sh` | Keynote export, "Better" image quality | Only Keynote reads current `.key` files (LibreOffice's importer stops at Keynote 6) |
| `.pptx` / `.ppt` | PDF, then compress | `deck-to-pdf.sh` | PowerPoint export | LibreOffice and other converters swap fonts and break SmartArt; use them only on a server |
| Video inside a deck | Dropped | (the PDF export drops it) | | Log which slide had it. Ask the company if it turns out to matter |
| `.docx` | Markdown + images | `pandoc --extract-media=<dir> -t gfm` | | Use PDF instead when layout is the point (signed contracts) |
| `.xlsx` | Keep, or CSV per sheet | | | A financial model's formulas are its content. CSV keeps numbers and loses the logic |
| Video file | MP4 (H.264) | `video-720p.sh` | 720p, CRF 26 | Screen recordings with UI text: `--height 1080` |
| Audio, voice memos | M4A | `ffmpeg -ac 1 -c:a aac -b:a 64k` | Mono 48–64k | A transcript is lighter still |
| Photos (JPEG, PNG, HEIC) | WebP | `image-to-webp.sh` | Long edge 2000, q80 | |
| Screenshots, charts with text | WebP | `image-to-webp.sh --max 2400 --quality 85` | | Never JPEG for text: it smears the edges |
| Images for ImageKit or `og:image` | JPEG | see `prep-images-for-embed` | | ImageKit makes the WebP itself; give it a WebP and its fallback is a PNG up to 3× larger |
| Zip, already unpacked | Removed | `zip-check.sh` first | | Remove only on `SAFE` |
| Zip, never unpacked | Unpacked, then each file through this table | `unzip`, then `zip-check.sh` | | It may be the only copy (executed legal documents often are) |
| HTML export with base64 images | Markdown + images | `pandoc` | | memopop's HTML exports are mostly base64 |
| GIF | MP4 | `video-720p.sh` | | Often 10× smaller |
| Exact duplicates | One copy | `find-dupes.sh` reports | | Keep the copy in the dataroom folder, not the one in `_zip-originals/` |

Measured on the Humain dataroom, 2026-11-19 (Ghostscript, 200 dpi): a 162MB
photo-heavy PDF to 23MB, two image decks 64MB and 39MB to 8.3MB and 8.8MB, the
fund deck 31MB to 14MB, a research paper 23MB to 0.7MB. Every text check
passed within 0.3%. A scanned patent certificate went from 22.9MB to 10.4MB
once grayscale images were included. Rendered at retina size, slide text and
the scan's type both stayed sharp. A 1.2MB PNG of headshots became a 50KB WebP
that looks the same.

## The scripts: one per kind, one file per run

All in `scripts/`. Each takes **one file**, writes its output **beside** the
input, refuses to overwrite, and **never deletes anything**. Deleting the
original is the agent's decision, after checking.

| Script | Does | Exit codes |
|---|---|---|
| `pdf-compress.sh <pdf> [--dpi 200]` | Writes `<name>.slim.pdf` | 0 ok · 3 not smaller · 4 text lost · 5 a page looks different |
| `deck-to-pdf.sh <deck> [--app keynote\|powerpoint]` | Writes `<name>.pdf`; lists embedded video first | 0 ok · 4 export failed |
| `video-720p.sh <video> [--height 1080]` | Writes `<name>.720p.mp4` | 0 ok · 3 not smaller |
| `image-to-webp.sh <image> [--max 2400]` | Writes `<name>.webp` | 0 ok · 3 not smaller |
| `zip-check.sh <zip> [--root <dir>]` | Reports whether every file in the zip exists unpacked | 0 safe · 1 missing |
| `find-dupes.sh <dir>` | Reports identical files, biggest waste first | always 0 |

**Never write a script that walks a whole tree and converts everything.** A
script that rips through a dataroom is a fiasco to unpack when one file goes
wrong. The judgment about each file belongs to the agent.

## The procedure

Hand each dataroom to its own subagent. Datarooms don't overlap, so several
can run at once. Inside one dataroom:

1. **Inventory.** `du`, file counts by extension, `find-dupes.sh`, and
   `zip-check.sh` on every zip. Write the plan at the top of the log.
2. **Zips first.** `SAFE` zips go. Zips that were never unpacked get
   unpacked, and their contents join the queue.
3. **Duplicates.** Keep one copy, preferring the dataroom folder over
   `_zip-originals/` or `oversized/`. Log the removed paths.
4. **One file at a time:** pick the script, run it, then check.
   - The exit code is 0.
   - PDFs: the script's text and page checks passed (exit 0). Exit 5 means a page
     came out different: keep the original, don't retry with other settings.
     Open one page to look at it:
     `gs -q -sDEVICE=jpeg -r200 -dFirstPage=N -dLastPage=N -o /tmp/p.jpg <pdf>`, then view the image.
     Check a dense page (a table, a chart, small print) once per document type.
   - Decks: the slide count matches, and any dropped video is logged.
   - Images and video: open one to look at it.
5. **Replace.** Only after the check: remove the original and give the new
   file the original's base name (`deck.slim.pdf` becomes `deck.pdf`). Keep
   the folder structure the founder used.
6. **Log the line** (below), then the next file.
7. **Report back:** size before and after, files touched, anything skipped
   and why.

If a dataroom has leftovers from an earlier pass, such as an `oversized/`
folder of originals whose compressed copies sit in the dataroom, check the
pairs (same name, the dataroom copy smaller and opening fine). Then remove the
originals and log them like any other replacement.

### The log

One `_slim-log.md` per dataroom, beside its top folder. It's the record of
what changed, so a single file can be traced and re-requested:

```markdown
# Slim log: <Company> dataroom

Started <date> · <before> → <after>

| File | Was | Now | Action | Check | Note |
|---|---|---|---|---|---|
| Team/<Executive bio>.pdf | 162.1MB | 22.9MB | pdf-compress | text 1317→1303, p3 viewed | |
| Company Overview/<Company> Deck.pdf | 63.7MB | 8.3MB | pdf-compress | 24 pages, p5 viewed | image-only PDF |
| SPV Deck.pptx | 101.6MB | <size> | deck-to-pdf + pdf-compress | <n> slides | 80MB media1.mov dropped |
| _zip-originals/Team-…zip | 163.3MB | — | removed | zip-check SAFE 9/9 | |
```

## Gotchas

1. **Deleting from gitignored folders can't be undone.** Datarooms are
   usually gitignored, so git can't bring a file back. That's why the order
   is fixed: verify, then delete, then log.
2. **Zip file names decode differently.** Curly apostrophes and accents in
   zips often don't match the unpacked names byte for byte. `zip-check.sh`
   runs with `LC_ALL=C` and re-checks misses by size. A "missing" file is
   usually a renamed one: search by size before calling it lost.
3. **Text counts drift a little.** `pdftotext` before and after can differ by
   a fraction of a percent (ligatures, spacing). The script allows 2%.
   Anything more means look.
4. **Ghostscript rewrites the whole PDF.** Now and then it breaks links or an
   unusual font. When `pdf-compress.sh` exits 4, try
   `ocrmypdf --skip-text -O2 in.pdf out.pdf` (`brew install ocrmypdf`).
5. **Don't use `/screen` or `/ebook` presets.** `/screen` is 72 dpi and turns
   slides to mush. `/ebook` is 150 dpi, which is fine for documents but soft
   for full-screen slides. The script's explicit 200 dpi is the tested
   middle.
6. **`deck-to-pdf.sh` drives the real apps.** macOS asks once for permission
   to control Keynote or PowerPoint, and PowerPoint's sandbox may ask for
   folder access. On a server with no Mac, use Gotenberg (LibreOffice behind
   an HTTP API) for `.pptx`, or ask for a PDF; `.key` has no server option.
   The AppleScript was written 2026-11-19 and hasn't been run against a real
   deck yet: check the first export closely.
7. **Video only disappears from decks.** A standalone video file gets
   re-encoded, not dropped, unless the user says otherwise.
8. **The text check can't see pictures.** A deck that is almost all images has
   almost no text, so a blanked slide or a lost photo passes a text check. An
   earlier pass damaged two founder decks this way (blank slides, a missing
   image, a block over three slides). `pdf-compress.sh` now also renders every
   page of the original and the result small and in gray and compares them,
   refusing (exit 5) when any page differs by more than `--max-diff` (default
   0.06 RMSE; ordinary JPEG recompression stays well under it). It names the
   pages. Trust that refusal: the original stays.
9. **Not for brand or design assets.** Logos, fonts and design source files
   for our own sites aren't founder content. Leave them alone.

## When space is still short: move files to a CDN

Converting is the first move, and usually enough. Moving files out is only for
when you need the room, for example a Cloudflare Artifacts repo close to its
1 GB limit. Then the repo keeps the text plus a manifest (CDN URL, `sha256`,
dimensions, alt text) and the files live on ImageKit, Cloudflare R2 with Image
Transformations, or another CDN. It's set per client in a committed config,
with keys in `.env`:

```yaml
# cdn.config.yaml
provider: imagekit      # imagekit | cloudflare-r2 | cloudflare-images | s3
visibility: signed      # public | signed (gated content needs signed)
offload: ask            # off | ask | on
```

Not built yet. Gated content (LP-only memos) must use `signed`: a public CDN
URL sits outside the gate.

## Related

- `prep-images-for-embed`: images headed for a page or ImageKit (JPEG, alt text, CDN upload)
- `cloudflare-artifacts-interface`: the 1 GB per repo limit this skill most often serves
- `setup-new-firm` (memopop) § deck capture: screenshots stitched to PDF, `-resize 1920x -quality 85`
- `astro-knots/context-v/specs/Live-Content-on-Cloudflare-Artifacts-with-an-MCP.md`: humain deal repos on Artifacts
