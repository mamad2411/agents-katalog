---
name: svg-to-raster
description: Use when the user wants to rasterize SVG files — convert SVG to PNG, PDF, or PostScript at a chosen resolution. Wraps CairoSVG (Python, in the plugin venv). Single file or batch. Companion to `vectorize` (other direction). Triggers - "convert this SVG to PNG", "render my icons at 2x", "I need a raster version of this logo".
allowed-tools: Bash(command *), Bash(test *), Bash(find *), Bash(mkdir *), Bash(rm *), Bash(wc *), Read, Write
---

# SVG to Raster

Rasterize SVG files to PNG / PDF / PS via [CairoSVG](https://github.com/Kozea/CairoSVG). Runs from the plugin's uv venv — no system Python pollution.

## When to use

- Convert logo / icon / diagram SVGs to PNG for use in slides, social, or pipelines that don't accept SVG.
- Render an SVG at multiple resolutions (e.g. 1×, 2×, 3× for app assets).
- Bake an SVG into a PDF for print or archival.

Do **not** use this skill when:
- Source is already raster — wrong direction; use `vectorize` instead.
- You need to *edit* the SVG — CairoSVG is render-only.
- The SVG uses advanced filters / unsupported CSS — CairoSVG covers SVG 1.1 well but newer features may not render. Inspect output and warn the user.

## Inputs

1. **Input** — SVG file or directory. Required.
2. **Format** — `png` (default), `pdf`, `ps`.
3. **Output dir** — default: `<input-dir>/<format>/`. Never overwrites originals.
4. **Scale** — multiplier on the SVG's intrinsic size. Default `1.0`. Use `2.0`, `3.0` for hi-DPI.
5. **Width / Height** — explicit pixel dimensions (overrides scale). Pass one to preserve aspect; both to force.
6. **DPI** — for PDF/PS output. Default `96`.
7. **Background** — default transparent. Pass a CSS colour (`#ffffff`, `white`) for solid fill.
8. **Recursive** — `--recursive` for directory descent.

## Procedure

1. Resolve venv: `VENV_DIR="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops/venv"`.

2. Verify `cairosvg` is importable in the venv:

   ```bash
   "$VENV_DIR/bin/python" -c "import cairosvg" 2>&1
   ```

   If missing → point at `image-ops-install-deps`. If it imports but raises a libcairo error, surface the system-lib install command (`sudo apt install libcairo2` / `brew install cairo`).

3. Enumerate `*.svg` inputs (case-insensitive). Skip non-SVG with note.

4. Call CairoSVG via the venv Python (keeps the skill self-contained — no helper script needed). Pass the gathered options as arguments rather than string-substituting them into the source; the script below dispatches on format and builds the kwargs itself:

   ```bash
   "$VENV_DIR/bin/python" - "$input" "$output" "$fmt" \
       "$scale" "$width" "$height" "$dpi" "$background" <<'PYEOF'
   import sys, cairosvg

   src, dst, fmt, scale, width, height, dpi, bg = sys.argv[1:9]

   fn = {'png': cairosvg.svg2png,
         'pdf': cairosvg.svg2pdf,
         'ps':  cairosvg.svg2ps}[fmt]

   kwargs = {'url': src, 'write_to': dst}
   # Empty string means "not supplied" — omit rather than passing a default
   # that would override CairoSVG's own.
   if scale:  kwargs['scale'] = float(scale)
   if width:  kwargs['output_width'] = int(width)
   if height: kwargs['output_height'] = int(height)
   if dpi:    kwargs['dpi'] = int(dpi)
   if bg:     kwargs['background_color'] = bg

   fn(**kwargs)
   PYEOF
   ```

   Function map: `png → svg2png`, `pdf → svg2pdf`, `ps → svg2ps`.

   Note that `output_width` / `output_height` override `scale` in CairoSVG — do not pass both unless that is what the user asked for.

5. Track file sizes and any render warnings (CairoSVG prints to stderr for unsupported features). Wrap each conversion so one bad file does not kill the batch:

   ```bash
   if ! "$VENV_DIR/bin/python" - ... <<'PYEOF'
   ...
   PYEOF
   then
     echo "FAILED: $input" >> "$failed_log"
     rm -f "$output"
     continue
   fi
   ```

   Removing the partial `$output` matters — a truncated PNG left on disk reads as a successful conversion to the summary.

## Output

- Rasterized files at `<output-dir>/`.
- Summary:
  - Files processed / failed, with the failed paths from `$failed_log`.
  - Per-file: source dimensions → output dimensions, output size.
  - Any render warnings (unsupported SVG features).

## Notes

- CairoSVG is LGPL-3.0; using it as a CLI dependency is fine, no licence contagion.
- For multi-resolution batch (e.g. app icon set), call this skill multiple times with different `--scale` values, or wrap in a small loop.
- If you need true SVG editing or advanced filter support, look at Inkscape CLI (`inkscape --export-type=png`). CairoSVG is the lighter-weight pure-Python option.
- Animated SVG (SMIL) is not supported — CairoSVG renders the initial frame only.
