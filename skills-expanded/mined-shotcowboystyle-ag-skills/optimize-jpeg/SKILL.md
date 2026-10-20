---
name: optimize-jpeg
description: Use when the user wants to shrink JPEG files — losslessly with `jpegoptim` (~5–15% reduction, no re-encode) or with re-compression via `mozjpeg` (~10–15% better than libjpeg-turbo at the same visual quality). Web-prep workhorse for photo libraries. Triggers - "compress these JPEGs", "make these photos smaller", "optimise my JPEG folder for web".
allowed-tools: Bash(which *), Bash(command *), Bash(brew *), Bash(test *), Bash(getconf *), Bash(mktemp *), Bash(jpegoptim *), Bash(djpeg *), Bash(cjpeg *), Bash(jpegtran *), Bash(exiftool *), Bash(identify *), Bash(magick *), Bash(mv *), Bash(rm *), Bash(find *), Bash(xargs *), Bash(wc *), Bash(du *), Read, Write
---

# Optimize JPEG

Squeeze JPEG file size. Two modes:

- **lossless** (default) — `jpegoptim --strip-all`. Repacks Huffman tables and strips metadata. No re-encode, no quality change.
- **recompress** — `mozjpeg`. Re-encodes with better quantisation tables; 10–15% smaller than libjpeg-turbo for the same SSIM. Quality flag controls trade-off. Always strips metadata (see step 4).

## When to use

- Web-prep: photo galleries, blog images, anything destined for upload.
- Archive squeeze: lossless mode is the no-regret option for any JPEG-heavy folder.
- Pre-step inside `web-ready` orchestrator.

Do **not** use this skill when:
- Source is PNG → use `optimize-png`.
- Source is HEIC/RAW/TIFF — pipe through `web-ready` (or convert first).
- The JPEG is already heavily compressed (<70% quality estimate) — recompress will visibly degrade.

## Inputs

1. **Input** — file or directory. Required.
2. **Mode** — `lossless` (default) or `recompress`.
3. **Recursive** — `--recursive` for directory descent.
4. **In-place** — default. `--output-dir <path>` to write copies.
5. **Quality** (mode=recompress) — `cjpeg -quality N`. Default `82` (web-quality). `90` for archival; `75` for aggressive web compression.
6. **Strip metadata** — default `on` for both modes. EXIF/IPTC/XMP gone. `--keep-metadata` is honoured in **lossless mode only** (drop `--strip-all`). Recompress always loses metadata at the decode step; the skill re-injects it afterwards with `exiftool` when `--keep-metadata` is set — see step 4.
7. **Progressive** — default `on`. Smaller files + better perceived load. `--baseline` to disable for compatibility with very old decoders.

## Procedure

1. Verify the relevant binary.

   **Lossless:** `which jpegoptim`. If missing, point at `image-ops-install-deps` and stop.

   **Recompress:** mozjpeg ships its `cjpeg`/`djpeg`/`jpegtran` under the *standard* names, but the package is deliberately kept off the default PATH so it does not shadow libjpeg-turbo. Resolve the real prefix before use — do **not** assume a `-mozjpeg` suffixed binary exists:

   ```bash
   # Resolve MOZ_BIN: directory containing mozjpeg's cjpeg/djpeg/jpegtran
   MOZ_BIN=""
   for d in \
     "$(brew --prefix mozjpeg 2>/dev/null)/bin" \
     /opt/mozjpeg/bin \
     /usr/local/opt/mozjpeg/bin
   do
     [ -x "$d/cjpeg" ] && { MOZ_BIN="$d"; break; }
   done
   if [ -z "$MOZ_BIN" ]; then
     echo "mozjpeg not found — install it (see image-ops-install-deps), or use mode=lossless" >&2
     exit 1
   fi
   ```

   If `MOZ_BIN` cannot be resolved, do not silently fall through to the system `cjpeg` — that is plain libjpeg-turbo and gives none of the promised gain. Report it and offer lossless mode instead.

2. Enumerate inputs (JPEG/JPG only — skip with note).

3. **Lossless** (jpegoptim):

   ```bash
   jpegoptim --strip-all --all-progressive ${outdir:+--dest "$outdir"} "$input" \
     || echo "FAILED: $input" >> "$failed_log"
   ```

   `--all-progressive` forces progressive output (smaller). `--strip-all` removes EXIF/IPTC/XMP/comments. Drop these if `--keep-metadata` was set.

4. **Recompress** (mozjpeg):

   mozjpeg's CLI is decode-then-encode. **Never redirect into the input path** — the shell truncates the redirect target before `djpeg` reads it, destroying the source. Always encode to a temp file and move it into place only on success:

   ```bash
   tmp="$(mktemp "${input}.XXXXXX.jpg")"
   if "$MOZ_BIN/djpeg" "$input" \
        | "$MOZ_BIN/cjpeg" -quality "$q" -progressive -optimize > "$tmp"
   then
     # --keep-metadata: recompress decodes to raw PPM, so EXIF/IPTC/XMP/ICC are
     # gone by this point. Re-inject from the original before the swap.
     if [ "$keep_metadata" = "yes" ]; then
       exiftool -overwrite_original -tagsFromFile "$input" -all:all "$tmp" || {
         echo "FAILED (metadata re-inject): $input" >&2; rm -f "$tmp"; continue; }
     fi
     mv "$tmp" "$output"
   else
     echo "FAILED (recompress): $input" >&2
     rm -f "$tmp"
     continue
   fi
   ```

   When `$output` equals `$input` this is the in-place path and it is safe: the original is only replaced after a successful encode.

   Or use `"$MOZ_BIN/jpegtran"` for lossless transforms when only metadata stripping + Huffman repack is desired (essentially a faster jpegoptim). `jpegtran` reads and writes JPEG directly, so it preserves metadata and needs no re-injection — but it too must go via a temp file for in-place use.

   For batch, parallelise with `xargs -P <ncpu>` where `<ncpu>` is `$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)`.

5. Sanity-check: any output file >95% of input size in recompress mode — keep the original instead. mozjpeg occasionally inflates already-optimised inputs. Compare with `stat` before the `mv`:

   ```bash
   in_sz=$(wc -c < "$input"); out_sz=$(wc -c < "$tmp")
   if [ "$out_sz" -ge $(( in_sz * 95 / 100 )) ]; then
     rm -f "$tmp"; echo "KEPT ORIGINAL (no gain): $input"; continue
   fi
   ```

6. Collect failures. Every `FAILED:` line emitted above feeds the summary in the Output section — do not report success counts without also reporting the failure list.

## Output

- Optimised JPEGs at the resolved paths.
- Summary:
  - Files processed / skipped / failed / kept-original (where recompress would have inflated).
  - Total: `<orig-MB>` → `<new-MB>` (`<pct>%` saved).
  - Visible-quality flag: if recompress was used and the source had a quality estimate <75 (via `identify -format "%Q"`), surface a warning per file.

## Notes

- mozjpeg is a drop-in libjpeg-turbo replacement with smarter trellis quantisation. It's slower than libjpeg-turbo by ~3× — fine for web-prep, not for thumbnail generation.
- mozjpeg's binaries are named `cjpeg` / `djpeg` / `jpegtran`, identical to libjpeg-turbo's. That is why step 1 resolves an explicit prefix rather than calling them bare: a bare `cjpeg` on PATH is almost always libjpeg-turbo's.
- For "I just want it smaller, don't touch quality": always use `lossless` mode. Free win.
- The orchestrator (`web-ready`) defaults to: resize first, then encode WebP/AVIF, fall back to mozjpeg for JPEG output. This skill exists to do JPEG-only optimisation without that pipeline.
