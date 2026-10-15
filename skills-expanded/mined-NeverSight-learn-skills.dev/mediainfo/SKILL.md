---
name: mediainfo
description: Use ffprobe to inspect image/video assets and understand their visual properties. Useful when doing frontend work involving media files.
---

# Media Info

When you encounter or are asked about an image or video asset (dimensions, format, aspect ratio, color space, etc.), use `ffprobe` to inspect it before making assumptions.

## Usage

```bash
ffprobe -hide_banner <file_path>
```

This gives a concise summary including:
- **Dimensions** (width x height) — critical for sizing, aspect ratios, responsive layouts
- **Pixel format** — whether the image has alpha (e.g., `rgba` vs `rgb`)
- **Codec/format** — PNG, JPEG, WebP, AVIF, etc.
- **Duration/frame rate** — for video or animated assets (GIF, APNG, WebM)

## When to Use

- Before writing CSS/HTML that references an image asset (know the actual dimensions)
- When a user asks about an asset's properties
- When choosing `width`/`height`, `aspect-ratio`, or `object-fit` values
- When deciding if an image needs a transparency-capable format
- When debugging layout shifts caused by incorrect intrinsic sizes

## Example

```
$ ffprobe -hide_banner hero.png
Input #0, png_pipe, from 'hero.png':
  Duration: N/A, bitrate: N/A
  Stream #0:0: Video: png, rgba(pc), 1920x1080, 25 fps, 25 tbr, 25 tbn
```

From this you know: 1920x1080, has alpha channel (`rgba`), PNG format — so you can confidently set `aspect-ratio: 16/9` and know transparency is available.
