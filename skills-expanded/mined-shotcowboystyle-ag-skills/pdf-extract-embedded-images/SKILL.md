---
name: pdf-extract-embedded-images
description: Use when the user wants to recover the images embedded in a PDF at their native resolution, without rasterizing the pages — a PDF that is essentially a wrapper around photos. For rendering whole pages to images instead, use `pdf-to-images`. Triggers - "get the photos out of this PDF", "extract the original images from this brochure", "recover the embedded pictures at full quality".
allowed-tools: Bash(pdfimages *), Bash(command *), Bash(file *), Bash(ls *), Bash(mkdir *), Bash(wc *), Read, Write
---

# Extract Embedded Images from PDF

Pull out JPEG and PNG objects embedded in a PDF using `pdfimages`. Extracts at native resolution without rasterizing the page. Different from `pdf-to-images` — this recovers the original embedded image files, not a rasterized page render.

## When to use

- A PDF is a container for photos (e.g., a photo book or brochure) — you want the original images, not a rasterized version.
- Bulk-extracting image assets from a multi-page document without re-encoding.
- Recovering embedded images at their full embedded resolution and quality.

## Inputs to gather

- **Input PDF file** — path to the PDF. Required.
- **Output directory** — optional. Default: current directory.

## Procedure

### 1. Check tooling

```bash
command -v pdfimages >/dev/null || {
  echo "pdfimages not installed — see the image-ops-install-deps skill (poppler-utils)" >&2
  exit 1
}
```

### 2. Validate PDF and inspect contents

```bash
file "$input"
pdfimages -list "$input" || { echo "not a readable PDF: $input" >&2; exit 1; }
```

The `-list` flag shows a summary of embedded images: page number, index, width, height, bits per component, color space, encoding. This helps set expectations (e.g., "3 JPEG images at 2400×3000px").

### 3. Extract

```bash
mkdir -p "$outdir"
pdfimages -all "$input" "$outdir/$prefix" \
  || { echo "extraction failed for $input" >&2; exit 1; }
```

`-all` is shorthand for `-j -jp2 -jbig2 -ccitt`: it writes each image in its *native* encoding rather than dumping raw pixels. A JPEG stream comes out as `.jpg`, a JBIG2 stream as `.jb2`, and so on. It does not extract extra "alternate-format versions" — there is one output per embedded image.

**Alternatives:**

- `-j` — preserve native JPEG encoding for JPEG streams. It is an *encoding* switch, not a filter: non-JPEG images are still extracted, as raw `.ppm`/`.pbm` dumps.
- `-png` — write everything as PNG. Re-encodes non-PNG content; lossless output, but larger files and no longer byte-identical to what was embedded.

Recommend `-all` unless the user specifies otherwise — it is the only mode that never re-encodes.

### 4. Report

After extraction:

- Count of images extracted, by type (JPEG, PNG, etc.).
- Output filenames and their dimensions.
- File sizes and whether any extraction failed.
- Remind the user that embedded images may have compression applied by the PDF creator — they are not necessarily at absolute maximum quality, but they are at their native resolution.

## Output / side effects

- Image files created with names like `prefix-000.jpg`, `prefix-001.png`, etc. (depends on PDF content).
- Original PDF unchanged.

## Notes

- **Native resolution, not PDF rendering resolution:** `pdfimages` extracts the raw embedded objects at the resolution they were embedded, not the page rendering resolution. For a photo book PDF with 2400×3000px JPEGs embedded, you get those 2400×3000px files directly — much faster and lossless compared to rasterizing the 8.5"×11" page at 300 DPI.
- **Lossy source warning:** Even though `pdfimages` does not re-encode, the original embedded images may already be JPEG-compressed by the PDF creator. You cannot recover quality that was lost before embedding. Check output sizes and quality to verify.
- **Format preservation:** `-all` keeps each stream in its embedded encoding, so nothing is re-encoded on the way out. `-png` is useful when you want a uniform output format, at the cost of re-encoding and a file-size change.
- **Naming collision:** If multiple images have the same name, `pdfimages` appends sequential suffixes (e.g., `prefix-000.jpg`, `prefix-001.jpg`). No files are overwritten.
- Depends on poppler (`apt install poppler-utils` on Debian/Ubuntu, `brew install poppler` on macOS). Use `image-ops-install-deps` rather than installing by hand.
