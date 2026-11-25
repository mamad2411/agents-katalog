---
name: og-card-generator
description: Render 1200x630 Open Graph and Twitter card PNGs, one per page, from .atelier/brand.json colors, fonts, logo and studio name; single card from flags or a batch from a pages.json manifest. Use when adding og:image or twitter:image meta tags, setting up social link previews for a site or blog, or regenerating cards after a brand color or font change.
---

## Run

Run from the project root that holds `.atelier/brand.json` (or pass `--project <dir>`):

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" og pages.json public/og
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" og --title "TideWane" --subtitle "A deep-sea idle dungeon crawler" --slug home --out public/og
```

`pages.json` is `{ "pages": [ { "slug": "home", "title": "...", "subtitle": "..." } ] }` or a bare array of pages.

JS API (the module path goes in as an argument and is loaded through `pathToFileURL`, so the import also works with Windows paths; importing it does not start the CLI):

```bash
node --input-type=module -e "const { pathToFileURL } = await import('node:url'); const m = await import(pathToFileURL(process.argv[1]).href);
const { loadBrand } = await import(new URL('../brand-memory/index.mjs', pathToFileURL(process.argv[1])).href);
const paths = await m.generateCards({
  brand: loadBrand(process.cwd()),
  pages: [{ slug: 'home', title: 'TideWane', subtitle: 'A deep-sea idle dungeon crawler' }],
  outDir: 'public/og',
});
for (const p of paths) console.log(p);" "${CLAUDE_SKILL_DIR}/index.mjs"
```

Also exported: `generateCard({ brand, page, outPath })` for one card, and `buildCardHtml(brand, page, { fonts?, mark? })` for the HTML without rendering.

## Options

CLI:
- `<pages.json> [outDir]`: batch; `outDir` defaults to `og-cards` (or use `--out <dir>`).
- `--title <text>`, `--subtitle <text>`, `--slug <slug>`, `--out <dir>`: one card without a manifest.
- `--project <dir>`: where `.atelier/brand.json` lives (default: current directory).
- `--font-display <file>`, `--font-body <file>`: font files (.woff2, .woff, .ttf, .otf) for the brand fonts.
- `--mark <file>`: logo on the card (.svg, .png, .jpg, .webp, at most 2 MB). Default: `logos.mark` from brand.json when set, resolved inside the project root.
- `--no-mark`: leave the logo off.
- `-h`, `--help`: print usage and exit 0.

API (both functions): `fonts: { display?, body? }` (font file paths), `mark` (logo file path; the API does not read `logos.mark` itself, so pass it), `browser` (reuse an open Playwright browser; it is left open), `onWarning(message)` (default: printed to stderr).

Page fields:
- `slug`: file name and footer path. Lowercase letters, digits, `-` and `_`, with `/` for nested folders (`blog/launch`). Default `index`.
- `title`: falls back to `brand.product`.
- `subtitle`: `description` is accepted as an alias.

Brand fields read (nothing else):
- `palette.bg`: default `#111111`.
- `palette.fg`: default `#111111` or `#ffffff`, whichever contrasts more with `bg`.
- `palette.accent`: shapes and glow only, never text; default `palette.fg`.
- `typography.display` (title; falls back to `body`) and `typography.body`.
- `brand.studio` (falls back to `brand.product`) and `brand.product`.
- `logos.mark`: the logo, CLI only (see `--mark`).

## Output

`<outDir>/<slug>.png` per page, 1200x630 PNG. The CLI prints the written paths.

Layout: a brand row at the top (logo, studio name, and the page path in a pill), the title and subtitle anchored to the bottom margin, and one piece of art: a disc of light rising from the top-right corner in `palette.accent`, toned for light and dark backgrounds. The title is set in the display font at weight 400 (never a faked bold), 88px, shrinking to 48px to fit 4 lines, then shortened with an ellipsis; the subtitle keeps 2 lines; the brand row always stays on the card.

Warnings (stderr, cards are still written): text contrast below 4.5:1, a brand font that is not installed and has no font file, a font file that fails to load, text shortened to fit.

## Exit codes

- `0`: cards written.
- `2`: usage error (usage printed to stderr) or runtime failure (`atelier: <message>`, plus a `Fix:` line when Chromium is missing).

## Notes

- Fonts: without a font file the card uses fonts installed on the rendering machine, so web fonts such as Inter usually fall back. Pass the file to get the real font; it is inlined, never fetched.
- Font stacks are quoted per family, so names like `Press Start 2P` work. Generic keywords (`sans-serif`, `system-ui`, ...) and the vendor keywords `-apple-system` and `BlinkMacSystemFont` stay unquoted and are skipped when picking the brand font: the installed-font check and a `--font-display`/`--font-body` file apply to the first named family in the stack.
- Every slug is checked before anything is written: a slug that could leave `outDir` (`..`, `:`, backslashes, dots) or two pages writing the same file is an error.
- Page text is HTML-escaped. The card page runs with JavaScript disabled and all network requests blocked, so a title or brand value cannot run script or fetch anything.
- Needs Playwright Chromium. Check with `node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" doctor`.
- One PNG serves both tags:

```html
<meta property="og:image" content="https://example.com/og/home.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:image" content="https://example.com/og/home.png" />
```
