---
name: optimize-images
description: Scans the project for heavy images and outdated formats, then proposes sizes, conversions and markup changes before touching any file.
disable-model-invocation: true
---

Audit images in: $ARGUMENTS (default: the whole repository, skipping node_modules and build output).

1. List image files with size on disk and pixel dimensions (`find` with `-size +200k`, and `identify`, `sharp` or `file` for dimensions). Report the 20 largest.
2. For each, find where it is used (search for the file name in code, templates and CSS) and the largest size it is displayed at.
3. Flag: dimensions more than 2x the displayed size, PNG or BMP photographs, JPEG graphics with flat colors, SVGs with embedded bitmaps, and files nothing references.
4. Propose per file: target format (AVIF or WebP with a fallback, or SVG), target width, and estimated saving. Suggest `srcset`, `sizes`, `loading="lazy"` below the fold, and explicit `width` and `height` to prevent layout shift.
5. Do not convert or delete anything yet.

Show a table of file, current size, proposed result and saving, with a total. Ask which files to convert, keep originals in a clearly named folder, and name the exact command you will run.
