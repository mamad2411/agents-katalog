---
name: pdf-html
description: >
  Exports design-* HTML artifacts to single-page PDFs using headless Chromium. Targets the
  same .canvas / [class*="canvas-"] conventions as screenshot-html, but outputs vector PDFs
  sized to each canvas's exact pixel dimensions rather than PNG rasters.

  Use when the desired output is a shareable PDF — audit reports, client deliverables,
  long-form documents. Do NOT use for social-media graphics (LinkedIn, Instagram, YouTube)
  or interactive overlay assets; screenshot-html produces better results for those.

  Trigger on: "export as PDF", "save as PDF", "generate a PDF", "capture as PDF", "PDF
  version of this", or whenever the user wants a PDF from an HTML artifact previously
  produced by a design-* skill.
---

# Skill: pdf-html

Targeted per-canvas PDF export via headless Chromium. Strips preview-backdrop styles (dark
page background, padding, gap) before rendering so the PDF contains only the canvas itself.

## When to use

- After any `design-*` skill that produces a document-style HTML artifact — audit reports,
  deliverables, spec sheets, long-form cards — and a PDF is the desired leave-behind format.
- When the user says "export as PDF", "capture as PDF", "PDF version of this", etc.

Skip if:

- The artifact is a social-media graphic (LinkedIn, Instagram, YouTube thumbnail, Twitter
  card). Use `screenshot-html` for those — PDFs don't add value and print media mode may
  alter the styling.
- The artifact is a stream overlay or OBS scene pack. Use `screenshot-html`.

## What it targets

Same canvas conventions as `screenshot-html`:

- `.canvas` — primary fixed-size artifact wrapper.
- `[class*="canvas-"]` — modifier variants: `canvas-front` / `canvas-back`, `canvas-audit`,
  `canvas-og` / `canvas-hero`, etc.
- `.scene` — hash-routed scenes (captured at their hash-navigated state).

Nested matches are deduped — only top-level containers generate PDFs.

If a file has no matches, falls back to a full-page PDF. `--full-page` forces this for
every file.

## How to run

```bash
node skills/pdf-html/scripts/pdf-html.mjs <dir> [--output <dir>] [--width <px>] [--full-page]
```

Flags:

- `<dir>` (positional, default `.`): directory to scan recursively for `*.html`. The
  `screenshots/` and `pdfs/` subdirectories and hidden dirs are skipped.
- `--output <dir>` (default `<dir>/pdfs`): where PDFs are written. Flat output — one file
  per canvas target.
- `--width <px>` (default `1920`): browser viewport width. Only needs to be ≥ the widest
  canvas; PDF height is measured from the rendered DOM, not the viewport.
- `--full-page`: force full-page PDFs for every file, skipping canvas targeting.

Height is always auto-measured from the canvas's rendered bounding box — no `--height`
flag needed.

## Prerequisites

**None — the script self-bootstraps on first run**, installing Playwright and the Chromium
binary into its own `node_modules` alongside the script. First run takes ~10–60s; subsequent
runs are fast (~1s overhead).

```text
$ node pdf-html.mjs ./design/<brand>/artifacts
Playwright not found. Installing into <skill-dir>/scripts/node_modules (one-time)…
…
```

### Token-load guard

Same `@import` sanity check as `screenshot-html`: if a relative `@import url('../tokens.css')`
can't resolve from the artifact's directory, the guard warns you before writing the PDF:

```text
  artifact.html ⚠ design tokens may not have loaded — PDF may show fallback styles.
    failed CSS: file:///wrong/path/tokens.css (net::ERR_FILE_NOT_FOUND)
    Fix: run the script against the artifact's native folder so relative imports resolve.
```

## PDF rendering details

Playwright's `page.pdf()` renders in `@media print` mode. For `design-*` artifacts the
canvas CSS contains no `@media print` overrides, so the rendered PDF matches the browser
preview. The preview-backdrop styles (`body { background: #2a2a2a; padding: 32px; }` and
`.canvas-label`) are stripped via injected CSS before each PDF is generated, so the output
contains only the canvas.

PDF dimensions are set to the canvas's exact rendered pixel size (e.g. `1200 × 5077 px`
for a tall audit report). This produces a single-page vector PDF — shareable, searchable,
and printable — at the canvas's native resolution.

## Output naming

Same convention as `screenshot-html` but with `.pdf` extension:

| Source file | Targets | Output filenames |
|---|---|---|
| `audit-report-2026-05-14-mercer-advisors.html` | one `.canvas-audit` | `audit-report-2026-05-14-mercer-advisors.pdf` |
| `business-card.html` | `.canvas-front`, `.canvas-back` | `business-card--canvas-front.pdf`, `business-card--canvas-back.pdf` |
| `blog-hero.html` | `.canvas-og`, `.canvas-hero` | `blog-hero--canvas-og.pdf`, `blog-hero--canvas-hero.pdf` |

## Common patterns

- **Single artifact PDF:** `node skills/pdf-html/scripts/pdf-html.mjs ./design/<brand>/artifacts --output ./design/<brand>/pdfs`
- **Full-page (deliverable pages without a .canvas):** add `--full-page`
- **Only want the audit report, not the whole artifacts dir:** point at a temp dir or use `--full-page` to get the page at its natural height
