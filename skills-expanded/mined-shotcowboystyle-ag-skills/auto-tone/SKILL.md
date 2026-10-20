---
name: auto-tone
description: Use when the user wants automatic tonal correction — fix flat/washed-out / underexposed / low-contrast images by stretching levels, normalising contrast, and gamma-correcting to a neutral midtone. Implements auto-level (per-channel histogram stretch), auto-gamma (midtone correction), and a combined "punch" mode via ImageMagick. Operates on JPEG/PNG/TIFF/WebP. Triggers - "this photo looks flat", "fix the exposure on these", "brighten up my scans".
allowed-tools: Bash(magick *), Bash(convert *), Bash(identify *), Bash(command *), Bash(test *), Bash(getconf *), Bash(mktemp *), Bash(awk *), Bash(mv *), Bash(rm *), Bash(mkdir *), Bash(find *), Bash(xargs *), Read, Write
---

# Auto Tone

Fix flat or under/over-exposed images without manual curves work. Three modes:

- **level** (default) — `-auto-level` on the luminance channel. Stretches the histogram to `[0,1]` without touching colour balance. Safe, reversible-feeling.
- **gamma** — `-auto-gamma`. Drives the image's mean brightness toward 50% grey. Lifts dark scans, tames blown-out daylight.
- **punch** — `-normalize` (1% black + 1% white clip) followed by `-auto-gamma`. Stronger; the "press the button" preset for batch gallery prep.

## When to use

- Underexposed indoor / night phone shots.
- Faded scans of old prints.
- Bulk normalisation of a gallery shot under varying light.
- Pre-step before sharpening or upscaling — auto-tone first so the next stage isn't operating on a flat histogram.

Do **not** use this skill when:
- Source is a RAW file — fix tone in `darktable-cli` where you have full bit depth.
- Image is intentionally low-key (silhouettes, night scenes with crushed shadows) or high-key (snow, fashion editorials). Auto-gamma flattens the look.
- The histogram is already well-distributed (a quick `magick identify -format "%[fx:standard_deviation]" "$IN"` ≥ 0.22 → likely already toned; auto-level becomes a no-op or worse).

## Inputs

1. **Input** — file or directory. Required.
2. **Mode** — `level` (default) | `gamma` | `punch`.
3. **Recursive** — `--recursive` for directory descent.
4. **Output** — default in-place suffix `_tone`. `--output-dir <path>` to write into a sibling folder. `--overwrite` to replace.
5. **Strength** — `0.0` to `1.0` (default `1.0`). Blends corrected image with original via `-compose blend`.
6. **Preserve hue** — default `on`. Operate on the luminance channel only (HSL `L`), so colour relationships aren't shifted. `--per-channel` to apply auto-level independently to R/G/B (acts as combined tone + white-balance — usually you want `auto-white-balance` for that instead).
7. **Clip** (mode=punch) — black/white clip percent. Default `1`. `--clip 0.5` for gentler, `--clip 2` for aggressive contrast.

## Procedure

1. Verify ImageMagick 7+. `magick -version | head -1`. Else `convert` (IM6) with the same syntax.

2. Enumerate inputs (JPEG/JPG/PNG/TIFF/TIF/WebP). Skip RAW with note.

3. **level** (luminance-only auto-level, hue-preserving):

   ```bash
   magick "$IN" -colorspace HSL -channel L -auto-level +channel -colorspace sRGB "$OUT"
   ```

   With `--per-channel`:

   ```bash
   magick "$IN" -channel RGB -auto-level +channel "$OUT"
   ```

4. **gamma**:

   ```bash
   magick "$IN" -auto-gamma "$OUT"
   ```

   `-auto-gamma` computes the gamma needed to drive `mean → 0.5` and applies it. No clipping, no hue shift.

5. **punch**:

   ```bash
   magick "$IN" -normalize -auto-gamma "$OUT"
   ```

   Or with explicit clip:

   ```bash
   magick "$IN" -colorspace HSL -channel L -contrast-stretch "${CLIP}%x${CLIP}%" \
     +channel -colorspace sRGB -auto-gamma "$OUT"
   ```

   The `-colorspace HSL` wrap is required, exactly as in the `level` mode above. In sRGB there is no channel named `L` for `-channel` to select, so without the wrap the clip does not do the hue-preserving stretch the mode advertises.

   `-contrast-stretch 1%x1%` clips the darkest 1% to black and brightest 1% to white before stretching — the "Photoshop auto-contrast" behaviour.

6. **Strength blend** (when `<1.0`):

   Steps 3–5 write the tone-corrected result to a temp file `$TONED`, not straight to `$OUT`; the blend then composites it back over the original:

   ```bash
   PCT=$(awk -v s="$STRENGTH" 'BEGIN{ printf "%.0f", s*100 }')
   magick "$IN" "$TONED" -compose blend -define compose:args="$PCT" -composite "$OUT"
   rm -f "$TONED"
   ```

   At `--strength 1.0` skip the blend entirely and let steps 3–5 write `$OUT` directly.

7. For batch, parallelise with `xargs -P "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"` — `nproc` is GNU coreutils and is absent on macOS/BSD. Skip files ending `_tone` to avoid recursive re-processing.

8. Check `magick`'s exit status per file. On non-zero, append the path to `$failed_log`, remove any partial output, and continue to the next file.

## Output

- Tone-corrected images at the resolved paths.
- Summary:
  - Files processed / skipped (RAW or non-image) / failed / no-op (where the histogram was already well-distributed). The failed count and the paths come from `$failed_log` — report both, never the processed count alone.
  - Per-mode count when mixed.
  - Average histogram-spread before/after (`fx:standard_deviation`) — sanity check that the run actually changed something.

## Notes

- For "make my photos look better" without thinking: `--mode punch --strength 0.7` is the sane default.
- Auto-tone amplifies noise. If the source is already noisy (high ISO phone shots), denoise first, then tone.
- Combined with `auto-white-balance`: run WB first (so tone correction operates on a neutral image), then tone. Reverse order is not order-equivalent.
- This skill is the tone-only primitive. The `/apply-filters` command may chain it with sharpen/saturate; use this skill standalone when you only want tonal work.
