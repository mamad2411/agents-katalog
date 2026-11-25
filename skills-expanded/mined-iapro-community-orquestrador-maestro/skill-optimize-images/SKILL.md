---
name: skill-optimize-images
description: Optimizes images for blogs and websites, including format conversion, resizing, compression, responsive delivery, accessibility, and visual validation. Use when asked to optimize, reduce, prepare, convert, or improve images for the web.
category: media
risk: low
source: local-media-patterns
---

# Otimizar imagens para web

## Core Workflow

1. Inspect the source image and identify its format, dimensions, color profile, transparency, orientation, and current file size. Preserve the original and work on a derivative.
2. Confirm the intended placement when it is not obvious: blog hero, article thumbnail, social card, logo, inline content, or responsive site asset. If no dimensions are provided, infer them from the target layout and state the assumption.
3. Choose the smallest suitable output set:
   - AVIF for modern browsers and strongest compression.
   - WebP for broad browser compatibility.
   - JPEG for photographic fallback images.
   - PNG only when lossless detail or transparency is required.
4. Resize to the largest useful display size, avoid upscaling, preserve aspect ratio, correct orientation, and strip unnecessary metadata. Keep transparency when it is part of the design.
5. Compress while checking visual quality at 100% and at the rendered size. Prefer responsive variants (`srcset`/`sizes`) when the asset will be used on a site.
6. Produce predictable filenames, report dimensions, formats, quality, and before/after file sizes, and identify the recommended HTML/CSS delivery pattern when relevant.
7. Validate that the output opens correctly, has no visible artifacts, retains required transparency, and meets the target size/performance goal.

## Guardrails

- Never overwrite the source unless the user explicitly requests destructive replacement.
- Do not remove credits, copyright, or licensing metadata when it is required by the project; remove only metadata that is unnecessary or privacy-sensitive.
- Do not claim visual improvement without inspecting the result. For decorative or editorial images, do not alter the subject or meaning unless requested.
- Keep output names and paths portable; do not expose private local paths in generated documentation.

## Verification

- Compare source and derivative dimensions, format, byte size, and visual quality.
- Open or render each final derivative when possible.
- For a website change, check responsive rendering and confirm the asset is referenced by the intended path.

## Related Skills

- None yet.
