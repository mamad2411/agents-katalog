---
name: fast-resize
description: Use when the user wants to resize a large batch of images (>500 files) where ImageMagick throughput is the bottleneck. Wraps libvips for 5–10× faster batch resize at lower memory. Falls back to ImageMagick if `vips` isn't installed. Same outputs as the `/batch-resize` command — different engine. Triggers - "resize this whole folder fast", "these thousands of images are too slow in ImageMagick".
allowed-tools: Bash(which *), Bash(command *), Bash(getconf *), Bash(mktemp *), Bash(awk *), Bash(vips *), Bash(vipsthumbnail *), Bash(vipsheader *), Bash(magick *), Bash(convert *), Bash(identify *), Bash(mv *), Bash(rm *), Bash(mkdir *), Bash(find *), Bash(xargs *), Bash(wc *), Read, Write
---

# Fast Resize (libvips)

Batch image resize using libvips. Material throughput improvement over ImageMagick on large libraries — typical 5–10× speed-up and lower peak memory.

## When to use

- Batch is >500 images.
- The user is feeling ImageMagick's slowness (or is about to).
- The job is "resize this directory" — pure resize without compositing or filters.

Do **not** use this skill for:
- Small batches (<100 images) — the `/batch-resize` command is fine, no point swapping engines.
- Resize-with-filter / resize-with-text / multi-op pipelines — ImageMagick is the better tool for compound work.

## Inputs

1. **Input directory** — required.
2. **Target size** — one of:
   - `--width N` — resize so width = N, height auto.
   - `--height N` — resize so height = N, width auto.
   - `--max NxM` — fit within NxM box (preserves aspect).
   - `--exact NxM` — force exact dimensions (may distort or crop).
3. **Output mode** — `--output-dir <path>` (default: `<input>/resized/`), or `in-place`. **In-place is destructive and downscaling is not reversible** — never select it on the user's behalf. Require an explicit request plus a confirmation after the dry-run count in step 2, and write via a temp file so a failed resize cannot leave a truncated original (step 3).
4. **Filter** — interpolation kernel: `lanczos3` (default — best quality), `cubic`, `linear`, `nearest`.
5. **Recursive** — `--recursive` to descend into subdirectories. Default: top-level only.
6. **Format preserve** — by default keeps source format. `--to <ext>` to change format on the way out.

## Procedure

1. Verify `vips` is on PATH. If missing, fall back to ImageMagick `convert` with the same parameters and warn that this will be slower (point at `image-ops-install-deps`).

2. Enumerate input files (filter to image extensions: jpg, jpeg, png, webp, tiff, gif, heic, avif, jxl). Report the count and the resolved output mode. **If in-place was requested, stop here and get explicit confirmation** — state the file count and that originals will be replaced.

3. For each file, build the vips command. Two main forms:

   **Fit within box (preserves aspect):**
   ```bash
   vipsthumbnail "$input" --size "${W}x${H}" --output "$output[Q=85]"
   ```

   `vipsthumbnail` is the right tool for "resize down" — it's optimised for thumbnail-style ops and handles JPEG shrink-on-load (free 8× speedup for 1/8-size targets).

   **Exact resize via `vips`:**
   ```bash
   # scale = target / source; vips resize takes a scale factor, not pixel dims
   src_w=$(vipsheader -f width "$input")
   scale=$(awk -v t="$target_w" -v s="$src_w" 'BEGIN{ printf "%.6f", t/s }')
   vips resize "$input" "$output" "$scale" --kernel "$kernel"
   ```

   For `--width`/`--height`, compute scale = target / source as above. `vipsthumbnail` is preferred when shrinking; use `vips resize` when upscaling or when source dimensions vary widely.

   **In-place writes go through a temp file.** A vips process killed mid-write (OOM, corrupt source) otherwise leaves a truncated file where the original was:

   ```bash
   tmp="$(mktemp "${input}.XXXXXX.${ext}")"
   if vipsthumbnail "$input" --size "${W}x${H}" --output "$tmp[Q=85]"; then
     mv "$tmp" "$input"
   else
     rm -f "$tmp"
     echo "FAILED: $input" >> "$failed_log"
   fi
   ```

4. Run in parallel where safe. vips is internally threaded; running multiple processes via xargs/parallel adds little. One process per CPU core is the sweet spot for large batches — `$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)`, which works on both macOS and Linux (`nproc` is GNU-only).

5. Report progress every N files (every 10% or every 100, whichever is more frequent).

6. Capture per-file failures as shown above. Every non-zero exit appends to `$failed_log`; the summary in the Output section reads from it. Do not report a processed count without the failure list.

## Output

- Resized images at the resolved output paths.
- Summary: `<n> files processed, <total-input-MB>MB → <total-output-MB>MB, <elapsed-s>s, avg <ms>ms/image`.
- List of any files that failed (corrupt, unsupported format, permission errors).
- If output-dir was used and any source files had identical names from different subdirectories without `--recursive` flattening logic, flag the collision.

## Notes

- `vipsthumbnail` accepts `[Q=N]` syntax for JPEG quality on output (default 75; 85 is a good balance).
- Wide colour gamut: vips preserves ICC profiles by default. If the user is processing display-P3 / Adobe RGB images, that's a feature.
- HEIC / AVIF / JXL: vips supports these if compiled with the right libs (apt's `libvips-tools` includes libheif and libjxl on recent Ubuntu).
- ImageMagick fallback path: if `vips` is missing, run `magick "$input" -resize "${W}x${H}" "$output"` per file. Same output, slower. (`magick` is the ImageMagick 7 entry point; `convert` is the v6 name and is deprecated in v7.) The same temp-file-then-`mv` rule applies for in-place runs.
