---
name: screenshot-cli
description: Use when the user's host screen must be captured — the full desktop, one monitor, or a pixel region — or when a screen capture needs cropping, resizing, rotation, flipping, format conversion (png/jpeg/webp), quality control, or filters/enhancement; also when you need to enumerate connected monitors and their geometry. Not for browser-page screenshots (use claude-in-chrome).
---

# Screenshot CLI

One-command screen capture plus post-processing via `screenshot.py` in this
directory (PEP 723 script, mss + Pillow; `uv run` handles dependencies, no
setup). Prefer it over `screencapture` + `sips`: `screencapture -R` takes
Retina *points* (2x pixel surprise) and `sips --cropOffset` silently
center-crops. This CLI uses one consistent unit — whatever `--list-monitors`
reports — verified: `-r 100,100,800,600` yields an 800x600 image.

## Quick start

`screenshot.py` ships alongside this SKILL.md — set `S` to its path inside
this skill's directory (the base directory reported when the skill loads):

```bash
S=<this-skill-dir>/screenshot.py
uv run $S --list-monitors      # JSON: index, left, top, width, height (0 = all combined)
uv run $S -m 1 -o shot.png     # monitor 1 only
uv run $S -m 1 -r 100,100,800,600 -f jpeg -q 70 --resize 50% -o region.jpg
```

## Flags

| Group | Flags |
|-------|-------|
| capture | `-m N` monitor (0 = all, 1..N single) · `-r X,Y,W,H` region, relative to the selected monitor's origin · `--list-monitors` |
| output | `-o PATH` (default `screenshot-<timestamp>.<ext>` in cwd) · `-f {png,jpeg,webp,bmp,tiff}` (default: inferred from `-o` extension, else png) · `-q 1-100` (jpeg/webp only) · `--lossless` (webp) |
| geometry | `--crop X,Y,W,H` · `--roll DX,DY` (wraparound shift) · `--rotate DEG` · `--flip-h` · `--flip-v` · `--resize 1200x800 \| 1200x \| x800 \| 50%` |
| enhance | `--filter NAME` (repeatable: blur, sharpen, smooth, smooth-more, detail, contour, edge-enhance, edge-enhance-more, emboss, find-edges) · `--blur RADIUS` · `--brightness/--contrast/--saturation/--sharpness F` (1.0 = unchanged; the full [PIL ImageEnhance](https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html) module — Brightness, Contrast, Color, Sharpness) · `--grayscale` · `--invert` · `--autocontrast` |

## Behavior contract

- Processing order: crop → roll → rotate → flip → resize → filters → enhance.
- Success prints `path (WxH, FORMAT, KB)` to stdout, exit 0. Bad input prints a
  one-line `error: ...` to stderr, exits nonzero — safe to branch on exit code.
- A region extending past the monitor is clipped with a stderr warning.
- `--rotate` expands the canvas (black fill), so output dims can exceed input.

## Gotchas

- `-q` is silently ignored for png/bmp/tiff.
- `--list-monitors` reports geometry only. To identify which index is the
  built-in display, cross-reference `system_profiler SPDisplaysDataType -json`
  (match resolutions); indices can change when displays are replugged.
- `--help` is complete and authoritative for anything not listed here.
