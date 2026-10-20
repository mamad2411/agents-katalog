---
name: to-jxl
description: Use when the user wants to encode images of any raster format (PNG, GIF, WebP, TIFF, JPEG) to JPEG XL (.jxl) with a chosen quality preset — lossless, visually lossless, or web. General-purpose JXL encoder. For a JPEG-only archive where the goal is a byte-exact-recoverable lossless transcode with a savings report, use `transcode-jpeg-to-jxl-lossless` instead. Triggers - "convert these PNGs to JXL", "encode this folder as JPEG XL", "make JXL versions at web quality".
allowed-tools: Bash(cjxl *), Bash(command *), Bash(find *), Bash(sh *), Bash(wc *), Bash(du *), Read, Write
---

# Convert Images to JPEG XL

Encode images to JPEG XL (.jxl) format using `cjxl`. Supports lossless, visually lossless, and web quality presets, with optional effort (compression) tuning.

## When to use

- Converting photos to JXL for archival, where file size matters and quality must be preserved.
- Encoding non-JPEG sources (PNG, TIFF, WebP, GIF) to JXL at a chosen distance.
- Creating web-optimized JXL variants with controlled visual loss.

Do **not** use this skill when the source set is exclusively JPEG and the goal is archival: `transcode-jpeg-to-jxl-lossless` covers that case with a dry-run preview, a byte-savings report, and the recovery instructions. This skill is the general encoder; that one is the JPEG-archive workflow.

## Inputs to gather

- **Input file or directory** — single image, folder, or recursive tree. If omitted, ask for the path.
- **Quality preset** — ask which tier: `lossless` (full fidelity, `-d 0`), `visually-lossless` (imperceptible loss, `-d 1.0`, default), or `web` (visible compression acceptable, `-d 3.0`). Default: visually-lossless.
- **Effort level** — optional, range 1–9 (1 = fastest, 9 = slowest/best compression). Default: 7. Only ask if the user is concerned about speed vs file size.

## Procedure

### 1. Check tooling

```bash
command -v cjxl >/dev/null || {
  echo "cjxl not installed — see the image-ops-install-deps skill" >&2
  exit 1
}
```

### 2. Map quality presets to distance

- `lossless` → `-d 0`
- `visually-lossless` → `-d 1.0`
- `web` → `-d 3.0`

Set `effort=7` unless the user overrides.

### 3. Determine scope

- **Single file:** run one conversion.
- **Directory (non-recursive):** ask before processing, then loop over image files in the folder.
- **Recursive:** use `find` to locate all images in the tree.

Ask for confirmation before batch operations. Set the depth limit once, and reuse it:

```bash
maxdepth="-maxdepth 1"   # non-recursive
maxdepth=""              # recursive — omit the flag entirely
```

### 4. Convert

**Single file:**

```bash
cjxl -d "$distance" -e "$effort" "$input" "${input%.*}.jxl"
```

**Batch (folder or recursive):**

`find` substitutes only the literal token `{}`. It has **no** `{.}` "strip the extension" placeholder — that is GNU parallel syntax. Passing `{.}.jxl` writes every single file to one literal output named `{.}.jxl`, so each conversion overwrites the last. Derive the output name inside a shell instead:

```bash
find "$target" $maxdepth -type f \
  \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \
     -o -iname '*.gif' -o -iname '*.webp' -o -iname '*.tif' \) \
  -exec sh -c '
    for f do
      cjxl -d "$0" -e "$1" "$f" "${f%.*}.jxl" \
        || echo "FAILED: $f" >> "$2"
    done
  ' "$distance" "$effort" "$failed_log" {} +
```

Show progress (file count, time remaining estimate if batch is large).

### 5. Report

After conversion:

- Count of files converted, skipped, failed.
- Original vs. converted file sizes; report total bytes saved.
- Read the failure list from `$failed_log` written by step 4 and print it. Never report a converted count without also reporting failures — `find -exec` does not propagate per-file exit status, so an uncaptured failure is invisible.

## Output / side effects

- New `.jxl` files created in the same directory as originals (or in a user-specified output folder).
- Original files remain unchanged.

## Notes

- **Lossless JPEG→JXL transcoding:** at `-d 0` from a JPEG source, `cjxl` stores JPEG reconstruction data (JBRD) alongside the pixels. To recover the original JPEG bit-exact later, run `djxl input.jxl recovered.jpg` — reconstruction is driven by the `.jpg` output extension, not by a flag. If the `.jxl` carries no JBRD (it was encoded from PNG, or lossily), `djxl` fails rather than silently emitting a re-encode. This is the killer feature for photo archives; the `transcode-jpeg-to-jxl-lossless` skill wraps it with a savings report.
- **Effort vs. speed:** Effort 7 is a good default (reasonable compression in 1–2 seconds per MP). Effort 9 can take minutes on large files. Only use 9 for final archival encodes, not batch preview work.
- **Alpha channels:** JXL supports them natively. PNGs with transparency will retain it.
- Depends on `libjxl-tools` (`apt install libjxl-tools` on Debian/Ubuntu, `brew install jpeg-xl` on macOS). Use `image-ops-install-deps` rather than installing by hand.
