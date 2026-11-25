---
name: convert-to-avif
description: Use when the user wants AVIF output — modern web format with ~30% better compression than WebP at the same visual quality, and ~50% better than JPEG. Wraps `avifenc`. Companion to the `/convert-to-webp` command. Best target for new web work; check browser support if delivering to ancient clients. Triggers - "convert these to AVIF", "encode this folder as AVIF for the web".
allowed-tools: Bash(avifenc *), Bash(command *), Bash(which *), Bash(exiftool *), Bash(find *), Bash(xargs *), Bash(sh *), Bash(getconf *), Bash(basename *), Bash(mkdir *), Bash(rm *), Bash(wc *), Read, Write
---

# Convert to AVIF

Encode JPEG/PNG/TIFF to AVIF. AVIF beats WebP on compression ratio and supports 10/12-bit, HDR, and lossless modes. Browser support is universal as of 2024 (Chrome 85+, Firefox 113+, Safari 16.4+).

## When to use

- Web-prep where modern browser support is fine.
- Archival of high-bit-depth photos (10/12-bit AVIF preserves more than JPEG).
- Pre-step inside `web-ready` orchestrator.

Do **not** use this skill when:
- Output must work in Safari <16.4 / IE / very old Android browsers — fall back to WebP or JPEG.
- Source is already AVIF — no point re-encoding.
- You need lossless re-encoding of a JPEG that should remain bit-exact-decodable — that's JPEG XL's unique trick, not AVIF's. Use `transcode-jpeg-to-jxl-lossless`.

## Inputs

1. **Input** — file or directory. Required.
2. **Quality** — `avifenc -q N` (0–100). Default `60` (visually equivalent to JPEG q82, much smaller). `80` for archival; `45` for aggressive.
3. **Speed/effort** — `avifenc -s <0..10>`. Default `6` (balanced). `0` is best compression but very slow; `10` is fast but bigger files.
4. **Lossless** — `--lossless`. Enables lossless mode (ignores quality). For exact archival of PNG.
5. **Bit depth** — `--depth 8|10|12`. Default `8`. Use `10` for HDR or 16-bit source.
6. **Output dir** — default: `<input-dir>/avif/`. Skill never overwrites originals.
7. **Recursive** — `--recursive` for directory descent.
8. **Preserve EXIF** — default off (web-prep assumption). `--keep-exif` to copy EXIF over via `exiftool`.

## Procedure

1. Verify `avifenc` is on PATH. If missing, point at `image-ops-install-deps`.

2. Enumerate inputs (jpg, jpeg, png, tiff — skip others with note).

3. For each file:

   ```bash
   avifenc -q "$quality" -s "$speed" ${lossless:+--lossless} ${depth:+--depth "$depth"} \
     "$input" "$output" \
     || { echo "FAILED: $input" >> "$failed_log"; rm -f "$output"; continue; }
   ```

   Per-file. avifenc is single-threaded per encode but accepts `--jobs N` for tile-parallel — useful on large images. Removing a partial `$output` on failure matters: a truncated AVIF left behind looks like a successful conversion to the summary and to anything that later globs the output directory.

   For batch parallelism:

   ```bash
   find "$indir" -type f \( -iname '*.jpg' -o -iname '*.jpeg' \
        -o -iname '*.png' -o -iname '*.tif' -o -iname '*.tiff' \) -print0 |
   xargs -0 -P "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)" -I{} \
     sh -c 'avifenc -q "$0" -s "$1" "$2" "$3/$(basename "${2%.*}").avif" \
            || echo "FAILED: $2" >> "$4"' \
     "$quality" "$speed" {} "$outdir" "$failed_log"
   ```

4. If `--keep-exif` was set, post-process:

   ```bash
   exiftool -tagsfromfile "$input" -all:all "$output" -overwrite_original
   ```

5. Track size deltas, and report the contents of `$failed_log` alongside them.

## Output

- AVIF files at `<output-dir>/`.
- Summary:
  - Files processed / failed, with the failed paths from `$failed_log`.
  - Total: `<orig-MB>` → `<new-MB>` (`<pct>%` saved).
  - Quality estimate per file (using `--qcolor` if requested).

## Notes

- AVIF encoding is *slow* compared to JPEG/WebP. Speed `6` is ~2–4× slower than `cwebp`. Speed `0` can be 30× slower. Pick `6` unless archiving.
- `--speed 6 --quality 60` is the de facto web-prep default — quality matches q82 JPEG at roughly half the bytes.
- Animation: avifenc supports animated AVIF from PNG sequences (`avifenc -i input1.png -i input2.png ...`) but this skill focuses on still images.
- Decode support outside browsers is uneven (older image viewers may not decode). Check before mass-converting an archive.
- For *guaranteed* lossless re-encode of a JPEG (bit-exact reversible), use `transcode-jpeg-to-jxl-lossless` instead — JXL has a unique lossless-JPEG mode that AVIF cannot match.
