---
name: image-transform-pipeline
description: >-
  Inspect, resize, and convert local raster images with explicit dimensions and output formats. Use when an agent needs deterministic image preparation for a document, web page, or handoff. Use it for thumbnails, responsive image variants, format conversion, checking dimensions/transparency, or preparing a single-frame raster asset. It does not generate images, interpret their contents, or perform OCR.
---

# Image transform pipeline

The CLI uses `sharp` and reads local files only. Success is one JSON object on stdout; failures are one JSON object on stderr with exit code 1. Paths are resolved from the current working directory. It requires Node.js 20 or newer.

```sh
node scripts/index.js info photo.jpg
node scripts/index.js resize photo.jpg thumbnail.webp --width 320 --fit inside
node scripts/index.js convert logo.png logo.avif --format avif --quality 75
node scripts/index.js variants photo.jpg ./public/images --widths 320,640,1280 --format webp --quality 78
node scripts/index.js --help
```

## Commands

| Command | Arguments | Behavior |
| --- | --- | --- |
| `info` | `<input>` | Read metadata without writing a file. |
| `resize` | `<input> <output>` plus `--width N` and/or `--height N` | Resize while preserving aspect ratio unless `--fit fill` is selected. |
| `convert` | `<input> <output> --format jpeg\|png\|webp\|avif` | Convert to the requested format; the output extension must match. |
| `variants` | `<input> <output-dir> --widths N,N,... --format jpeg\|png\|webp\|avif` | Write one aspect-ratio-preserving, non-enlarged variant per requested width. |
| `--help` | none | Print usage as JSON and exit successfully. |
| `--version` | none | Print the package name and version as JSON. |

`resize` options:

- `--fit contain|cover|fill|inside|outside` defaults to `contain`.
- `--quality N` accepts integer values 1–100 for JPEG, WebP, or AVIF output; it is invalid for PNG. For resize, the output format comes from the filename.
- `--without-enlargement false` allows an image to grow beyond its source dimensions. By default, resizing never enlarges it.

`convert` accepts `--quality N` for JPEG, WebP, and AVIF. PNG ignores quality semantics, so the CLI rejects `--quality` with PNG rather than silently pretending to apply it. JPEG extensions may be `.jpg` or `.jpeg`.

`variants` accepts 1–12 unique widths from 1 through 20,000 pixels, sorts them numerically, and writes `<input-basename>-<width>.<format>` files into the requested directory. It creates the output directory if needed, preserves aspect ratio, and never enlarges the source. Requested widths larger than the source produce the source's existing width. Existing files with generated names are overwritten. Each completed variant is listed in the JSON result; if a later variant fails, earlier outputs may already exist.

## Result fields

`info` returns the input path, file size in bytes, decoded format, dimensions, color space, channel count, bit depth, density, alpha-channel presence, and page count when available:

```json
{"data":{"input":"photo.jpg","size":284010,"format":"jpeg","width":1600,
"height":1200,"space":"srgb","channels":3,"depth":"uchar","density":72,
"hasAlpha":false,"pages":1}}
```

`resize` and `convert` return `input`, `output`, actual `format`, output `width`, output `height`, and output file `size`. `variants` returns the resolved output directory, sorted requested widths, and a result object for each generated file. Sharp applies EXIF orientation before resizing, so reported dimensions reflect the oriented output.

## Bounds and workflow

- Input must be a regular local file no larger than 100 MiB.
- Decoded input is limited to 100 million pixels. This helps bound memory use for unexpectedly large or compressed images.
- Requested resize dimensions cannot exceed 20,000 pixels. Output is also limited to 100 million pixels.
- For `resize` and `convert`, output parent directories must already exist. `variants` creates its requested output directory. Generated output files can overwrite existing files, so choose paths carefully when preserving prior outputs matters.
- Animated and multi-page inputs are reported by `info` but rejected by transformation commands so frames/pages are not silently discarded.
- Supported formats are JPEG, PNG, WebP, and AVIF. SVG, PDF, HEIC, and other formats depend on the installed `sharp` build and are not promised here.

Inspect first when you need to know the source dimensions or transparency. Then pick the output dimensions and fit behavior based on the destination: `inside` keeps the image within a box, `cover` fills and may crop, and `contain` fits the full image inside the box. Verify the output metadata before using it in a layout where exact dimensions or transparency matter.

## Choosing a transformation

- Use `info` before changing a source when dimensions, alpha, page count, or format are unknown.
- Use `resize` when the goal is a target box. Prefer `inside`/`contain` when all content must remain visible; use `cover` only when cropping is acceptable; use `fill` only when distortion is intended.
- Use `convert` when pixel dimensions should stay the same but the encoded format should change. Choose a lossy quality setting only when the output format supports it and the visual tradeoff is acceptable.

Keep the original when transformations are lossy or when orientation or transparency matters. `variants` creates multiple widths for one source image; it does not process a directory of source files. For multiple inputs, run a separate operation for each file with explicit output names and verify representative outputs.

## Detailed asset-preparation procedure

### 1. Confirm the source and intended destination

Identify the exact source image and the use case: a fixed-size avatar, a responsive content image, a printable document asset, a transparent logo, or a smaller web delivery format. Find the target dimensions and whether cropping, transparency, metadata, or sharp detail must be retained. If the user has not specified a target, inspect first and ask or choose a conservative output only when the destination provides a clear constraint.

### 2. Inspect before transforming

Run `info` when source format, dimensions, orientation, alpha channel, color space, or page count may affect the choice. A portrait image with EXIF orientation can report an output orientation different from its raw stored pixel order; the tool applies orientation during resize. Check whether a logo needs transparency before selecting JPEG, which has no alpha channel.

### 3. Pick fit behavior intentionally

- `contain` fits the entire image inside the requested box and may leave unused space around it. This is useful for product tiles and icons where no content may be cropped.
- `cover` fills the requested box while preserving aspect ratio, so edges may be cropped. Use it only when the crop is acceptable for the subject.
- `inside` keeps both dimensions within the bounds and does not enlarge by default; it is useful for safe thumbnails.
- `outside` ensures both dimensions reach at least the target bounds and can produce a larger output than the box.
- `fill` forces exact dimensions and can distort proportions.

If both width and height are passed, consider how the selected fit affects the subject and final dimensions. Do not promise exact output dimensions unless the chosen fit guarantees them; use the result fields to verify actual width and height.

### 4. Choose format and quality

Use PNG when lossless edges or transparency matter, JPEG for opaque photographic content where lossy compression is acceptable, and WebP/AVIF when the target supports them and smaller delivery is useful. These are practical defaults, not universal compatibility guarantees. `--quality` is meaningful for JPEG, WebP, and AVIF only; the CLI rejects it for PNG. Keep an original or use a new output filename whenever compression could discard detail.

### 5. Verify and hand off

Inspect the returned output format, dimensions, and byte size. For a variant set, confirm the requested widths are represented and that no larger source was accidentally enlarged. For an asset used in a UI or document, visually inspect the result when possible, especially for cropped faces, text in images, transparent edges, and fine detail. Report the source and output paths plus any crop or quality tradeoff. Do not claim that metadata verification proves visual quality.

## Common failure decisions

- If a `resize` or `convert` output path's parent directory does not exist, create the intended directory explicitly or choose an existing one; `variants` creates its output directory.
- If the input exceeds the byte or decoded-pixel cap, resize it with a trusted image application or split the workflow. Do not repeatedly retry the same oversized input.
- If the format is unsupported, convert it with a suitable image tool first. Renaming the extension does not convert image data.
- If animation or multiple pages matter, use an animation-aware workflow; this CLI is designed for a single-frame output and may not preserve all frames.
