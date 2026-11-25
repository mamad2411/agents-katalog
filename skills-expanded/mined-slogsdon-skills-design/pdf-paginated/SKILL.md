---
name: pdf-paginated
description: >
  Exports document-flow HTML to a PAGINATED PDF at a real paper size (Letter/A4),
  with a running folio footer (title · page X / Y). The long-form sibling to
  pdf-html: where pdf-html renders each .canvas to one tall auto-height page (right
  for social artifacts and audit reports), this paginates a whole document across
  pages — right for essays, field guides, specs, and anything meant to be read or
  printed as pages.

  Trigger on: "paginated PDF", "print PDF", "PDF with pages", "Letter/A4 PDF",
  "multi-page PDF", "PDF of this essay/guide/doc". For single-canvas design
  artifacts (LinkedIn, Instagram, business card, audit report), use pdf-html or
  screenshot-html instead.
---

# Skill: pdf-paginated

Paginated document PDF via headless Chromium `page.pdf({format, margin})`. No
`.canvas` targeting — the whole document flows across paper pages. A folio footer
(title left, `page X / Y` right, JetBrains Mono) is rendered in the bottom margin.

## When to use

- Long-form documents where the reader expects pages: an essay, a field guide, a
  spec, a report body, a letter.
- When the output should be Letter or A4 with real margins and page numbers, not a
  single tall canvas.

Skip if:

- The artifact is a fixed-size design canvas (social post, business card, blog
  hero, audit-report canvas). Use `pdf-html` — it sizes the PDF to the canvas.
- You want a PNG. Use `screenshot-html`.

## The HTML it expects

Plain document-flow HTML, NOT the `.canvas` convention:

- Content flows normally (`body` → `article`). No fixed-width `.canvas` wrapper.
- Give the reading column a measure with `max-width` (e.g. `64ch`) centered, and
  put the page surface color on `body` (it prints because `printBackground` is on).
- **Do not set `@page` size/margins in CSS** — the script owns paper size and
  margins via `--format` / `--margin`. A CSS `@page` margin would double up.
- Optional `@media print` rules to keep things tidy across page breaks:
  `h2, li { break-inside: avoid; }` and `h2 { break-after: avoid; }`.
- Set a clean `<title>` — it becomes the footer's running head.
- Self-contained styles (inline `<style>` or a resolvable `@import`); web fonts
  load fine (the script waits for `document.fonts.ready`).

## How to run

```bash
node skills/pdf-paginated/scripts/pdf-paginated.mjs <dir> [--output <dir>] [--format Letter|A4] [--margin <css>] [--bleed <color>] [--no-footer]
```

Flags:

- `<dir>` (positional, default `.`): directory scanned recursively for `*.html`.
  `screenshots/`, `pdfs/`, and hidden dirs are skipped.
- `--output <dir>` (default `<dir>/pdfs`): where PDFs are written, one per HTML file.
- `--format` (default `Letter`): `Letter` or `A4`.
- `--margin` (default `0.9in`): CSS length applied to all four sides. Ignored in bleed mode.
- `--bleed <color>`: full-bleed page surface. See below.
- `--no-footer`: drop the folio footer (in bleed mode the footer strip still paints).

## Full-bleed backgrounds (`--bleed <color>`)

Default mode gives white paper margins. If the document has a **committed
background color** (e.g. a cream editorial page), that background floats as a card
on white — the margins show through. `--bleed <color>` fixes this: it zeroes the
left/right margins so the HTML background reaches the side edges, and paints the
top and bottom margin strips `<color>` so every page is that color edge-to-edge,
with a per-page inset and no white bands. The folio still renders in the bottom
strip.

In bleed mode the HTML owns **only its side text insets** (via `body` padding);
the top/bottom insets are the painted strips. So the HTML should:

- set the surface color on `html` and `body` with `print-color-adjust: exact`,
- pad only the sides (e.g. `padding: 0.1in 0.95in 0.3in`), and
- keep the reading column measured (`max-width`) and centered.

```bash
# cream editorial essay, full-bleed
node skills/pdf-paginated/scripts/pdf-paginated.mjs . --output ./pdfs --bleed '#fbfaf9'
```

## Prerequisites

**None — self-bootstraps on first run**, installing Playwright + Chromium into its
own `node_modules` next to the script (shared pattern with `pdf-html` /
`screenshot-html`). First run ~10–60s; subsequent runs are fast.

## Relationship to pdf-html

| | pdf-html | pdf-paginated |
|---|---|---|
| Output | one auto-height page per `.canvas` | document paginated across paper pages |
| Sizes to | canvas pixel dimensions | Letter / A4 + margins |
| Footer | none | folio (title · page X / Y) |
| Use for | social artifacts, audit-report canvases | essays, field guides, specs, reports |
