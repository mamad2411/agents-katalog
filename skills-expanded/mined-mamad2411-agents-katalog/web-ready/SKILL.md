---
name: web-ready
description: Use when the user wants to take a folder of images (any mix of HEIC, RAW, PNG, JPEG, TIFF, WebP) and produce a web-ready set — EXIF stripped, resized to a sensible max dimension, encoded in modern formats (AVIF + WebP, with JPEG fallback), and optimized for size. End-to-end orchestrator over the single-purpose skills in this plugin. Triggers - "make this folder web-ready", "prep these photos for upload", "get these images ready for my blog".
allowed-tools: Bash(which *), Bash(command *), Bash(test *), Bash(brew *), Bash(magick *), Bash(convert *), Bash(identify *), Bash(exiftool *), Bash(vips *), Bash(vipsthumbnail *), Bash(vipsheader *), Bash(heif-convert *), Bash(darktable-cli *), Bash(avifenc *), Bash(cwebp *), Bash(cjpeg *), Bash(jpegoptim *), Bash(oxipng *), Bash(mkdir *), Bash(mv *), Bash(rm *), Bash(find *), Bash(wc *), Read, Write
---

# Web-Ready (orchestrator)

One-shot pipeline: ingest anything → strip EXIF → resize → encode to web formats → optimize. The "make this folder uploadable" skill.

## When to use

- Photos coming off a phone (HEIC) destined for a blog.
- Camera RAW exports being prepped for an online gallery.
- A mixed folder of screenshots/photos that needs to ship to the web.
- Pre-step before image upload to any CMS, S3 bucket, or Cloudflare R2.

Do **not** use this skill when:
- The user wants archival output → keep originals; use the targeted skills (`to-jxl`, `transcode-jpeg-to-jxl-lossless`, `optimize-png`).
- The user wants pixel-perfect originals on the web (rare, e.g. art prints) → use `optimize-png`/`optimize-jpeg` only, no resize.
- Single-file conversion → call the underlying skill directly.

## Inputs

1. **Input directory** — required.
2. **Profile** — preset bundle. One of:
   - `blog` (default): max-side 2000px, AVIF q60 + WebP q80 + JPEG q82 fallback, EXIF stripped.
   - `gallery`: max-side 3000px, AVIF q70 + WebP q85, EXIF stripped.
   - `thumbnail`: max-side 800px, AVIF q55 + WebP q75, EXIF stripped.
   - `archival-web`: max-side 4000px, AVIF q80 + WebP q90, **EXIF preserved**.
3. **Custom overrides** — any of `--max-side N`, `--avif-q N`, `--webp-q N`, `--jpeg-q N`, `--keep-exif`, `--no-jpeg-fallback`.
4. **Output dir** — default: `<input>/web/`. Inside: `web/avif/`, `web/webp/`, `web/jpg/` parallel trees so the user can pick which set to upload.
5. **Recursive** — `--recursive`. Mirrors subdirectory layout.

## Procedure

1. **Pre-flight:** check each tool the pipeline needs and record which are present:

   ```bash
   for t in magick exiftool vipsthumbnail avifenc cwebp cjpeg oxipng jpegoptim \
            heif-convert darktable-cli
   do
     command -v "$t" >/dev/null && echo "ok    $t" || echo "MISS  $t"
   done
   ```

   `magick` and `exiftool` are required — stop and point at `image-ops-install-deps` if either is missing. The rest are optional: a missing encoder drops its output format from the pipeline with a one-line note, and a missing `heif-convert` / `darktable-cli` narrows which sources can be ingested (stage 1).

   For the mozjpeg-quality JPEG fallback, resolve `$MOZ_BIN` as described in `optimize-jpeg` step 1 — a bare `cjpeg` on PATH is libjpeg-turbo, not mozjpeg.

2. **Stage 1: Decode/normalise inputs.** Walk the input tree; classify each file:
   - JPEG/PNG/WebP/TIFF → pass through.
   - HEIC → decode to PNG via `heif-convert` (or via `vipsthumbnail` if libvips has libheif). Fail loud if neither is available.
   - RAW (CR2, ARW, NEF, DNG, ORF, RAF) → decode via `darktable-cli "$input" "$staged.tiff"`. There is no libvips fallback here: libvips ships no camera-RAW decoder for these formats (a DNG that happens to be TIFF-wrapped may partially load via tiffload, but CR2/ARW/NEF/ORF/RAF will not). If `darktable-cli` is missing, skip the file with a flagged warning naming the format, and tell the user in the summary that RAW ingestion needs `darktable-cli` installed.
   - Anything else (BMP, GIF, etc.) → pass through.

3. **Stage 2: Strip EXIF.** Unless `--keep-exif` set:

   ```bash
   exiftool -all= -tagsfromfile @ -Orientation -ColorSpace -overwrite_original "$staged"
   ```

   Preserve `Orientation` and `ColorSpace` (rotation handling and colour fidelity) even in strip mode.

4. **Stage 3: Resize.** Per file, fit within `<max-side>` box preserving aspect:

   ```bash
   vipsthumbnail "$staged" --size "${max_side}x${max_side}" --output "$resized.png[Q=100]"
   ```

   Use lossless intermediate to avoid double-compression. Skip if the source's longest side is already ≤ max-side.

5. **Stage 4: Encode.** For each survivor, produce up to three outputs:

   - **AVIF:** `avifenc -q "$avif_q" -s 6 "$resized.png" "$out/avif/$basename.avif"`
   - **WebP:** `cwebp -q "$webp_q" "$resized.png" -o "$out/webp/$basename.webp"`
   - **JPEG fallback** (unless `--no-jpeg-fallback`): `cjpeg` cannot read PNG — it decodes PPM/PGM/BMP/Targa only — so the stage-3 PNG must be decoded first:

     ```bash
     magick "$resized.png" ppm:- \
       | "$MOZ_BIN/cjpeg" -quality "$jpeg_q" -progressive -optimize \
       > "$out/jpg/$basename.jpg"
     ```

     If `$MOZ_BIN` did not resolve in pre-flight, use ImageMagick end to end instead — slightly larger output, but it reads PNG natively:

     ```bash
     magick "$resized.png" -quality "$jpeg_q" -interlace Plane "$out/jpg/$basename.jpg"
     ```

   Run encodes in parallel — they're independent. Check each encoder's exit status and record failures per file and per format; a format that fails for one file must not abort the other two or the rest of the batch.

6. **Stage 5: Optimize (final squeeze).**
   - JPEGs: `jpegoptim --strip-all --all-progressive` in-place on `web/jpg/`.
   - PNGs (only if any survived as PNG, e.g. with `--no-jpeg-fallback`): `oxipng -o 4 --strip safe`.
   - AVIF / WebP: avifenc and cwebp already produce near-optimal output; no second pass.

7. **Cleanup:** delete `<staged>` intermediates. Write a manifest at `<output>/manifest.json` mapping `<original-path> → {avif, webp, jpg}` plus per-file size deltas.

## Output

- Three parallel trees under `<output-dir>`: `avif/`, `webp/`, `jpg/`.
- `manifest.json` with the mapping and size table.
- Summary report:
  - Files processed / skipped / failed (with reasons).
  - Total bytes per format. Typical: `<orig> → AVIF <X>%, WebP <Y>%, JPEG <Z>%`.
  - Recommendation line: which format to upload (AVIF if all targets support it; WebP otherwise; JPEG as universal fallback).

## Notes

- Defaults are tuned for the `blog` profile. `gallery` and `archival-web` raise quality for slower-but-better output.
- The orchestrator never modifies originals. The output tree is fully separate.
- For very large input trees (>10k files), the stage-by-stage design is intentional — early failure of one stage doesn't waste the others' work; intermediates persist until cleanup.
- Companion skills: `convert-to-avif` (single-format), `optimize-png`, `optimize-jpeg`, `fast-resize`; plus the `/convert-to-webp` command for single-format WebP. This orchestrator composes the same tools; the user is welcome to use the components directly when they want finer control.
