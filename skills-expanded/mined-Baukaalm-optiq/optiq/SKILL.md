---
name: optiq
description: Optimise images in a project (JPEG, PNG, WebP, AVIF, GIF) with verified quality using the optiq-image CLI. Use when the user asks to compress, shrink or optimise images, reduce image weight or page size, strip EXIF/GPS from photos, or convert images to WebP/AVIF.
---

# Optimising images with Optiq

`optiq-image` encodes each image with several codecs (jpegli, libwebp, libavif, oxipng), measures every result
against the input, and keeps the smallest one that passes: pixel-exact in `lossless` mode, SSIM ≥ 0.99 in
`visually-lossless`, SSIM ≥ 0.975 in `balanced`. Everything runs locally; nothing is uploaded. Needs Node ≥ 20.

If the `optiq` MCP server is connected (tools `analyze_images` / `optimize_images`), prefer it over the CLI.

## Workflow

1. **Dry run first** (writes nothing) and show the user the expected savings:
   ```sh
   npx -y optiq-image <files or folders> --json
   ```
2. **Write** once the user agrees, or when the request is unambiguous:
   - Images referenced from code or markup: overwrite in place. The format and file name are kept, so references
     stay valid. Files are replaced atomically and only when smaller.
     ```sh
     npx -y optiq-image public/images --in-place --json
     ```
   - New assets or an explicit format change: write to a folder (extensions may change, e.g. `hero.png` →
     `hero.webp`; then update the references yourself).
     ```sh
     npx -y optiq-image src/assets --out src/assets-optimized --json
     ```
3. **Report** from the JSON: `totals.saved` (share), per-file `from`/`to`, `before`/`after` bytes, `quality`
   (SSIM or `"exact"`), `usedOriginal`, `warnings`, `error`.

## Choosing options

| Situation | Flags |
|---|---|
| Default for site images | `--mode balanced` (default) |
| Hero images, product photos, artwork, anything the user calls important | `--mode visually-lossless` |
| Logos, icons, screenshots that must stay exact | `--mode lossless` |
| Many images, speed matters | `--mode fast` |
| Photos going public (location privacy) | `--strip-metadata` (removes EXIF incl. GPS, and XMP) |
| Oversized camera photos | `--max-size 2560` |
| Old browsers must be supported | `--formats jpeg,png,webp` (no AVIF) |

## Rules

- Do not use `--reoptimize` unless the user asks. Files Optiq already compressed lossily carry a small marker and
  are skipped on purpose: every lossy pass loses a little more and the losses add up.
- Exit code `2` means some files failed; the others were still processed. Report the failures, do not retry blindly.
- SVG is optimised safely (ids kept, every result verified by rendering); it is not sanitised, so scripts stay.
  HEIC/HEIF is not supported (convert it elsewhere first).
- SSIM is a proxy for perception, not a guarantee. If the user reports visible artefacts, re-run the affected files
  from the originals (for example from git) with `--mode visually-lossless` or `--mode lossless`.
- Do not commit results without the user's approval.

Docs: https://baukaalm.github.io/optiq/guide/agents · CLI reference: https://baukaalm.github.io/optiq/guide/static
