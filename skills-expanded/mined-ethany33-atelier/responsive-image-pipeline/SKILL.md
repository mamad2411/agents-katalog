---
name: responsive-image-pipeline
description: Resize PNG/JPG/WebP images into AVIF and WebP srcset variants (EXIF-rotated, never upscaled), a fallback <img> file and a base64 LQIP placeholder, then print a copy-paste <picture> snippet with truthful srcset widths. Cached per source. Use for site images, hero art, gallery screenshots, srcset, page-weight or LCP work, or reprocessing after swapping an asset.
---

## Run

CLI (one or more files, `file://` URLs, or folders; folders are not recursive):

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" images src/hero.jpg --out public/img --alt "Harbor at dusk" --base-url /img/ --loading eager
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" images src/gallery --out public/img/gallery --widths 480,960 --json
```

On Windows in Git Bash, put `MSYS_NO_PATHCONV=1` in front of `node` when you pass `--base-url /img/`. Otherwise Git Bash rewrites `/img/` to `C:/Program Files/Git/img/` and the CLI stops with a usage error. With it set, give file paths as relative or `C:/...` paths, not `/c/...`. Do not use `//img/`: that is a protocol-relative URL.

JS API (the module path is passed as an argument, so the import works on Windows, macOS and Linux):

```bash
node --input-type=module -e "const { pathToFileURL } = await import('node:url'); const m = await import(pathToFileURL(process.argv[1]).href); const result = await m.processImage({ input: 'src/hero.jpg', outDir: 'public/img' }); console.log(m.buildPictureSnippet({ ...result, alt: 'Harbor at dusk', baseUrl: '/img/' }));" "${CLAUDE_SKILL_DIR}/index.mjs"
```

Always build the snippet from the `processImage` result so its widths, formats and fallback match the files on disk.

## Options

CLI flag / API option, default:

- `--out <dir>` / `outDir`: output folder (required).
- `--widths` / `widths`: `480,768,1280,1920`. Widths above the source are skipped and the source width becomes the top size.
- `--formats` / `formats`: `avif,webp`. `<source>` formats, best first; also `jpg`, `png`.
- `--fallback` / `fallback`: `auto` (png for transparent, PNG or GIF sources, jpg otherwise). Also `jpg`, `png`, `webp`, `avif`, `none` (API: `false`).
- `--lqip-width` / `lqipWidth`: `24`.
- `--name` / `name`: output file stem, default the input name without extension. CLI: one input only.
- API only: `quality` `{ avif: 60, webp: 78, jpg: 80 }`; `background` `#ffffff` (transparent pixels are flattened onto it for JPEG output).
- Snippet (`buildPictureSnippet`): `--alt` / `alt` (default empty, meaning decorative), `--sizes` / `sizes` (`100vw`), `--base-url` / `baseUrl` (URL prefix, default bare file names), `--loading` / `loading` (`lazy`; use `eager` for the hero/LCP image), `fallbackFormat` and `formats` (taken from the result).
- `--json`: print one JSON object per input (the result plus `snippet`) instead of text.

## Output

For each source `<name>` in the output folder:

- `<name>-<w>.avif` (quality 60, effort 4) and `<name>-<w>.webp` (quality 78) for each produced width.
- `<name>-<top>.jpg` or `.png`: fallback at the largest produced width (skipped when the fallback format is already a variant).
- `<name>-lqip.txt`: data URL of a tiny placeholder: JPEG, or WebP with alpha for transparent sources.
- `<name>.cache`: JSON manifest (source, settings hash, files). Delete it to force regeneration.

`processImage` resolves to `{ cached, variants, lqip, basename, widths, skippedWidths, formats, fallback, fallbackFormat, lqipPath, source: { path, format, width, height, transparent }, images: [{ path, format, width, height }] }`. `variants` lists the `<source>` files only.

Snippet (a 1000 px wide `Hero Image.jpg`, default widths):

```html
<picture>
  <source type="image/avif" srcset="Hero%20Image-480.avif 480w, Hero%20Image-768.avif 768w, Hero%20Image-1000.avif 1000w" sizes="100vw">
  <source type="image/webp" srcset="Hero%20Image-480.webp 480w, Hero%20Image-768.webp 768w, Hero%20Image-1000.webp 1000w" sizes="100vw">
  <img src="Hero%20Image-1000.jpg" alt="" loading="lazy" decoding="async">
</picture>
```

## Exit codes

- `0`: every input was processed or was already cached, or `-h` / `--help` printed the usage.
- `2`: usage error (usage printed to stderr), or at least one input failed (`atelier: <reason>` on stderr; the other inputs still run).

## Notes

- EXIF orientation is applied before resizing. Output files carry no EXIF or GPS metadata.
- A rerun is a cache hit only when the input bytes, every option, the pipeline version and the sharp version match and every output file still exists; otherwise it regenerates.
- One output name per source: in a single CLI run, inputs sharing a stem get distinct names (`hero-png`, `hero-jpg`, plus a short hash when the extension matches too). Across runs, `processImage` refuses to overwrite files that belong to another existing source; pass `--name` or another `--out`.
- File names keep the source stem, spaces included; the snippet URL-encodes them (a literal `%` becomes `%25`) and HTML-escapes every attribute. `--base-url` keeps any `%XX` escapes it already has.
- AVIF allows at most 16384 px per side and WebP 16383 px. When a variant would be larger (a long full-page screenshot at 1280 px, say), the input fails before any file is written, and the error names the largest width that fits; pass it with `--widths`. When an input fails partway, the files it wrote are removed.
- Progressive loading: put the LQIP on the `<img>` as `style="background-size:cover;background-image:url(<lqip>)"`. For transparent images, clear it once the image loads, or it shows through.
- Only the first frame of an animated GIF or WebP is used. SVG is rasterized at its intrinsic size, so prefer brand-asset-pipeline for logos.
- Remote URLs are not fetched: download the image first.
