---
name: screenshot-html
description: Capture pixel-exact PNG screenshots of design artifact components inside HTML files produced by design-* skills (LinkedIn, Instagram, YouTube, Twitch, OBS overlays, blog hero, business card, etc.). Targets the `.canvas` / `.canvas-*` / `.scene` containers — not full pages. Use after generating design artifacts and visual exports are needed.
---

# Skill: screenshot-html

Targeted artifact-node screenshots via headless Chromium. Skips browser chrome and page background — captures just the design canvas.

## When to use

- After running any `design-*` skill that produces artifact HTML (LinkedIn post, Instagram card, YouTube thumbnail, Twitter card, blog hero, podcast cover, quote card, carousel, business card, speaker bio, Twitch panels, OBS scene pack, stream overlay, newsletter header, OG/hero pair, talk slides, etc.) and you want PNG exports of each artifact.
- When you need a clean image asset to attach to a post, deck, or PR — without the surrounding page padding the artifact HTML uses for preview backdrop.

Skip if:

- The HTML is a deliverable page (e.g. `design-landing-page`, `design-link-in-bio`) — the page IS the artifact, not a `.canvas` inside it. Use `--full-page` for those.
- The user wants browser-rendered review (open in a browser instead).

## What it targets

The script queries for these conventions used by `design-*` skills:

- `.canvas` — the primary fixed-size artifact wrapper (most skills).
- `[class*="canvas-"]` — modifier variants: `canvas-front` / `canvas-back` (business card), `canvas-main` / `canvas-compact` (speaker bio), `canvas-full` / `canvas-safe` (YouTube channel art), `canvas-og` / `canvas-hero` (blog hero), `canvas-square` / `canvas-story` (quote card), `canvas-offline` (Twitch offline banner), `canvas-panel` (Twitch info panels).
- `.scene` — hash-routed scenes inside stream-overlay and OBS scene-pack files (`<section id="scene-starting" class="scene">` etc.). The script navigates each scene's hash before capture so the `.is-active` toggle applies.

Nested matches are deduped — only top-level artifact containers are screenshotted.

If a file has no matches, the script falls back to a full-page screenshot. `--full-page` forces fallback for every file.

## How to run

From the project root where the design HTML lives (Playwright must resolve there):

```bash
node skills/screenshot-html/scripts/screenshot-html.mjs <dir> [--output <dir>] [--width <px>] [--height <px>] [--full-page]
```

Flags:

- `<dir>` (positional, default `.`): directory to scan recursively for `*.html`. The `screenshots/` subdirectory and hidden dirs are skipped.
- `--output <dir>` (default `<dir>/screenshots`): where PNGs are written. Output is flat (one file per artifact target), not mirrored from the input tree — filenames disambiguate via slug + index.
- `--width <px>` / `--height <px>` (default `1920 × 1080`): browser viewport. Artifact canvases set their own pixel size, so the viewport just needs to be big enough to contain them. Bump up for very tall canvases (Instagram story 1080×1920, YouTube channel art 2560×1440).
- `--full-page`: force full-page screenshots for every file, skipping artifact targeting.

The browser runs at `deviceScaleFactor: 1` so PNG pixel dimensions match the canvas's declared size exactly (matches what `design-*` skills assume for export).

## Prerequisites

**None — the script self-bootstraps on first run.**

If Playwright isn't resolvable, the script installs it (and the Chromium binary) into its own `node_modules` next to `screenshot-html.mjs`. First run takes ~10–60s for the install; subsequent runs hit the fast path (~1s overhead).

```text
$ node screenshot-html.mjs ./design/<brand>/artifacts
Playwright not found. Installing into <skill-dir>/scripts/node_modules (one-time)…
added 2 packages in 986ms
…
```

The bootstrap also catches the "Chromium binary missing" failure mode (post-upgrade, fresh CI runner) and self-heals with `playwright install chromium` before retrying the launch.

### How the bootstrap stays scoped

The script anchors npm to its own directory by writing a stub `package.json` and passing `--prefix=<scripts-dir>`. Without those, npm walks up looking for the closest ancestor `package.json` and the install bleeds into a parent project. The bootstrap deliberately avoids that.

A local `.gitignore` covers `node_modules/`, `package.json`, and `package-lock.json` — none of the install artifacts are checked in.

### What does NOT work (intentional non-fallbacks)

These were considered and rejected; documented so future maintainers don't waste time re-discovering them:

- ❌ `npx -y playwright` / `npx -y --package=playwright -- node …` — `npx` only puts the playwright CLI on `PATH`; it does not make the package importable from an arbitrary `.mjs` file.
- ❌ `NODE_PATH=…` — ignored by Node's ESM resolver.
- ❌ Relying on a sibling project's `node_modules` — ESM resolves `import 'playwright'` from the script file's location, not cwd.

## Script location

`skills/screenshot-html/scripts/screenshot-html.mjs` (lives alongside this skill in the config repo). Always invoke with `node skills/screenshot-html/scripts/screenshot-html.mjs ...` from a directory where Playwright resolves — typically the project containing the design HTML, not this config repo. The script is self-contained — no relative imports — so calling it by absolute path from any cwd works too.

## Output naming

For each top-level artifact in a file, the script derives a hint from the element's id (preferred, e.g. `scene-starting`) or its most specific class token (`canvas-front`, `canvas-og`, etc.):

| Source file | Targets | Output filenames |
|---|---|---|
| `linkedin-2026-05-02-field-note.html` | one `.canvas` | `linkedin-2026-05-02-field-note.png` |
| `business-card.html` | `.canvas-front`, `.canvas-back` | `business-card--canvas-front.png`, `business-card--canvas-back.png` |
| `blog-hero.html` | `.canvas-og`, `.canvas-hero` | `blog-hero--canvas-og.png`, `blog-hero--canvas-hero.png` |
| `stream-overlay.html` | 5 `.scene` ids | `stream-overlay--scene-starting.png`, `…--scene-brb.png`, etc. |
| `carousel.html` | 5 sibling `.canvas` slides | `carousel--canvas-1.png` … `carousel--canvas-5.png` |
| `link-in-bio.html` | no `.canvas` (page IS the deliverable) | `link-in-bio.png` (full-page fallback) |

## Verification

- Each screenshot logs as `  <relative-input-path> → <output-name> (W×H)`.
- A summary line reports total shots and any full-page fallbacks.
- After running, `ls <output>` should show one PNG per artifact target.
- Spot-check by opening a few PNGs — pixel dimensions should match the canvas's declared `width`/`height` in the source CSS (e.g. LinkedIn share = 1200×627, Instagram portrait = 1080×1350, YouTube thumb = 1280×720).
- Failures (page errors, no-layout elements, broken `file://`) print per-file and don't abort the run.

### Token-load guard (@import sanity check)

`design-*` artifacts typically declare `@import url('../tokens.css')` inside an inline `<style>` block. If the script is run against an HTML file that's been moved out of its native `./design/<brand>/artifacts/` directory, `../tokens.css` resolves to a path that doesn't exist, the import silently fails, and every `var(--color-…)` falls back to its initial value — producing a screenshot with default browser styles (black text on white) that looks superficially correct in `ls` but is wrong in detail.

The guard catches this two ways per file:

1. **Network-level**: listens for `requestfailed` and `response.status() >= 400` on `.css` requests. A 404 / `ERR_FILE_NOT_FOUND` on any stylesheet trips the warning.
2. **Computed-style sniff**: if the artifact references `var(--*)` anywhere AND none of a handful of common token names (`--color-surface`, `--color-ink`, `--color-bg`, `--color-primary`, `--color-accent`, …) resolve to a value on the artifact element, the warning fires even if no CSS request technically failed (covers cases where the import path is empty or the file loaded but is empty).

The warning prints to stderr but does NOT abort — the screenshot still writes so you can inspect the broken render. Output looks like:

```text
  artifact.html ⚠ design tokens may not have loaded — screenshot likely shows fallback styles.
    failed CSS: file:///wrong/path/tokens.css (net::ERR_FILE_NOT_FOUND)
    Likely cause: a relative @import (e.g. '../tokens.css') doesn't resolve from this directory.
    Fix: run the script against the artifact's native folder so relative imports resolve.
```

Fix is always to point the script at the artifact's actual directory:

```bash
node screenshot-html.mjs ./design/<brand>/artifacts \
  --output ./design/<brand>/screenshots
```

## Common patterns

- **All artifacts in a brand folder:** `node skills/screenshot-html/scripts/screenshot-html.mjs ./design/<brand>/artifacts`
- **Custom output dir:** `node skills/screenshot-html/scripts/screenshot-html.mjs ./design --output ./previews`
- **Force full-page (deliverable pages):** `node skills/screenshot-html/scripts/screenshot-html.mjs ./design/landing-page --full-page`
- **Tall canvases (story / channel art):** add `--height 2200` so the viewport contains the canvas before targeting kicks in.
