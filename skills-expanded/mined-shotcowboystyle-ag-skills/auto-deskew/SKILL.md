---
name: auto-deskew
description: Use when the user wants to automatically straighten a tilted image — scanned documents, phone-captured pages, photographed receipts, or slightly off-axis photos. Detects the dominant skew angle and rotates the image to vertical/horizontal, optionally cropping the resulting transparent triangles. Uses ImageMagick `-deskew` for documents and a Hough-line fallback (via Python + OpenCV) for photographs. Triggers - "straighten this scan", "this photo is tilted", "deskew before OCR".
allowed-tools: Bash(magick *), Bash(convert *), Bash(identify *), Bash(command *), Bash(test *), Bash(getconf *), Bash(mktemp *), Bash(cat *), Bash(awk *), Bash(rm *), Bash(mkdir *), Bash(find *), Bash(xargs *), Read, Write
---

# Auto Deskew

Straighten a tilted image. Two backends, picked by content type:

- **document** (default) — `magick -deskew 40%`. Detects skew via the Radon-style projection profile that ImageMagick's deskew operator implements. Fast, robust on text/scans up to ±15°.
- **photo** — Python + OpenCV Hough-line transform. Detects the dominant horizontal/vertical line angle (horizons, building edges, table corners) and rotates by its negative. Use for photographs without a clean text baseline.

## When to use

- Scanned documents that came in at an angle.
- Phone snapshots of pages, receipts, whiteboards.
- Slightly-tilted architectural / horizon photos (`--mode photo`).
- Pre-step before OCR — Tesseract accuracy degrades sharply past ±2° skew.

Do **not** use this skill when:
- The image is intentionally tilted (Dutch angle, artistic composition).
- Skew is severe (>15°) — usually means the document was captured upside down or sideways. Detect orientation first (`exiftool -Orientation`, or rotate by 90/180 multiples) before deskewing.
- The image has no straight reference lines (clouds, abstract textures) — Hough will return noise; rotation will be near-random.

## Inputs

1. **Input** — file or directory. Required.
2. **Mode** — `document` (default) | `photo` | `auto` (heuristic: if `magick identify -format "%[colorspace]"` is `Gray` or the image has very low saturation → `document`; else `photo`).
3. **Recursive** — `--recursive` for directory descent.
4. **Output** — default in-place suffix `_deskew`. `--output-dir <path>` for sibling folder. `--overwrite` to replace.
5. **Threshold** (mode=document) — `-deskew` percentage. Default `40%` (ImageMagick's recommended value). Higher = more aggressive detection, more false positives.
6. **Max angle** — default `15°`. If detected skew exceeds this, refuse to rotate and flag the file (probably wrong orientation, not skew).
7. **Crop** — default `on`. After rotation, crop to the largest inscribed rectangle so there are no transparent / black triangle borders. `--no-crop` to keep the full rotated canvas.
8. **Background** — fill colour for the post-rotation triangles when `--no-crop`. Default `white`. Use `none` for transparent (PNG/WebP only).

## Procedure

1. Verify ImageMagick 7+. For `photo` mode, also resolve the plugin's uv venv and verify it has `opencv-python-headless` and `numpy` (managed by `image-ops-install-deps`; if missing, point at it):

   ```bash
   PLUGIN_DATA_DIR="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops"
   VENV_PY="$PLUGIN_DATA_DIR/venv/bin/python"
   test -x "$VENV_PY" || { echo "Plugin venv missing — run image-ops-install-deps."; exit 1; }
   "$VENV_PY" -c 'import cv2, numpy' 2>/dev/null \
     || { echo "photo mode needs opencv-python-headless + numpy in the plugin venv — run image-ops-install-deps."; exit 1; }
   ```

   Invoke Python as `"$VENV_PY"` directly, matching the convention `image-ops-install-deps` establishes. Do not shell out to `uv run`.

2. Enumerate inputs (JPEG/JPG/PNG/TIFF/TIF/WebP). Skip and note RAW.

3. **document** mode:

   Measure first, then write — the max-angle guard in step 5 has to decide *before* the file is rotated. `-deskew` records what it detected in the `deskew:angle` artifact, so a throwaway pass to `null:` yields the angle without producing output:

   ```bash
   ANGLE=$(magick "$IN" -deskew "${THRESHOLD}%" -print '%[deskew:angle]\n' null:)
   ```

   Apply the guard (step 5), then do the real conversion:

   ```bash
   magick "$IN" -background "$BG" -deskew "${THRESHOLD}%" \
     $( [ "$CROP" = on ] && echo "+repage -fuzz 1% -trim +repage" ) \
     "$OUT"
   ```

   `-deskew` applies the rotation. `-trim` with a small fuzz removes the resulting fill border when `CROP=on`. `$ANGLE` from the measuring pass feeds both the guard and the summary.

4. **photo** mode (Python via the plugin's uv venv):

   ```python
   import cv2, numpy as np, sys
   img = cv2.imread(sys.argv[1])
   if img is None:
       # Unreadable / corrupt / unsupported — exit non-zero so the caller skips
       # the file rather than reading a "0.0" as "no skew detected".
       print("unreadable", file=sys.stderr)
       sys.exit(1)
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   edges = cv2.Canny(gray, 50, 150, apertureSize=3)
   lines = cv2.HoughLines(edges, 1, np.pi/720, 200)
   if lines is None:
       print("0.0"); sys.exit(0)
   # Collect angles near horizontal (±30°) and near vertical (±30° of 90°)
   angles = []
   for rho, theta in lines[:200, 0]:
       deg = np.degrees(theta) - 90  # 0 = horizontal line
       if abs(deg) < 30:
           angles.append(deg)
       elif abs(deg - 90) < 30:
           angles.append(deg - 90)
       elif abs(deg + 90) < 30:
           angles.append(deg + 90)
   if not angles:
       print("0.0"); sys.exit(0)
   print(f"{np.median(angles):.3f}")
   ```

   That snippet is not shipped as a file — write it to a temp script at run time, then invoke it with the venv interpreter resolved in step 1:

   ```bash
   DESKEW_PY="$(mktemp -t deskew_photo.XXXXXX.py)"
   cat > "$DESKEW_PY" <<'PYEOF'
   # ... the Python above, verbatim ...
   PYEOF

   if ! ANGLE=$("$VENV_PY" "$DESKEW_PY" "$IN"); then
     echo "SKIPPED (unreadable): $IN" >> "$failed_log"
     rm -f "$DESKEW_PY"
     continue
   fi

   magick "$IN" -background "$BG" -rotate "$(awk -v a="$ANGLE" 'BEGIN{print -1*a}')" \
     $( [ "$CROP" = on ] && echo "+repage -fuzz 1% -trim +repage" ) \
     "$OUT"

   rm -f "$DESKEW_PY"
   ```

   For a batch, write the temp script once before the loop and delete it after, rather than per file.

5. **Max-angle guard**: applies to both modes, using `$ANGLE` from step 3 (document, measuring pass) or step 4 (photo). If `|angle| > MAX_ANGLE`, skip the file before writing anything and flag it:

   ```bash
   if awk -v a="$ANGLE" -v m="$MAX_ANGLE" 'BEGIN{ exit !(((a < 0) ? -a : a) > m) }'; then
     echo "$IN: detected ${ANGLE}° — exceeds max-angle ${MAX_ANGLE}°, skipping (likely wrong orientation, not skew)"
     continue
   fi
   ```

6. **Crop to inscribed rectangle** (when `--no-crop` is off and the simple `-trim` leaves uneven borders): use the analytic formula for the largest inscribed axis-aligned rectangle inside a rotated rectangle. For input `W×H` rotated by `θ`:

   ```
   new_w = (W·|cos θ| - H·|sin θ|) / (cos²θ - sin²θ)   if W ≥ H
   new_h = (H·|cos θ| - W·|sin θ|) / (cos²θ - sin²θ)
   ```

   Crop centred. For small angles (<5°) the difference vs. `-trim` is negligible — `-trim` is fine.

7. For batch, parallelise with `xargs -P "$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"` — `nproc` is GNU coreutils and is absent on macOS/BSD. Skip files ending `_deskew`.

8. Per-file failures append to `$failed_log` and the batch continues. Report that list in the summary; a processed count on its own hides the skips.

## Output

- Deskewed images at the resolved paths.
- Summary:
  - Files processed / skipped (RAW or non-image) / failed / unchanged (|angle| < 0.1°) / refused (|angle| > max).
  - Per-mode count when mixed.
  - Distribution of detected angles (min / median / max) — sanity check across the batch.

## Notes

- ImageMagick's `-deskew` is tuned for bilevel/grayscale text. On colour photos it often returns 0° or noise — that's why `photo` mode exists.
- For OCR pipelines: deskew before binarisation. After deskew, `magick "$IN" -threshold 50%` or hand off to `tesseract` directly.
- If you want both content types handled in one run: `--mode auto`. The heuristic isn't perfect — review the angle distribution in the summary and re-run misclassified files explicitly.
- This skill rotates only. For perspective correction (four-corner unwarping of a photographed document), use a dedicated tool like `dewarp` or OpenCV's `getPerspectiveTransform` — auto-deskew won't fix keystoning.
