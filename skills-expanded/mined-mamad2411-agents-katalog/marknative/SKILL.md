---
name: marknative
description: Render Markdown files to paginated PNG/SVG images using the marknative CLI. Use this skill whenever asked to convert, render, or export Markdown to image formats.
metadata:
  author: liyown
  homepage: https://github.com/liyown/marknative
  source: https://github.com/liyown/marknative/tree/main/packages/marknative-skill
user-invocable: false
---

# marknative — Markdown to PNG/SVG renderer

`marknative` renders Markdown (CommonMark + GFM + LaTeX math) to paginated PNG or SVG pages without a browser. Runs entirely server-side via skia-canvas.

## Installation

```bash
npm install -g marknative
# or run without installing:
npx marknative <file.md>
```

## Basic usage

```bash
# Render file → page-01.png, page-02.png … next to the source
marknative README.md

# Write to a directory
marknative README.md -o out/

# Single output file
marknative README.md -o README.png

# SVG output
marknative README.md -f svg -o diagram.svg

# Pipe from stdin
cat notes.md | marknative -o preview.png
echo "# Hello" | marknative -f svg
```

## All flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--format <fmt>` | `-f` | `png` | Output format: `png` or `svg` |
| `--output <path>` | `-o` | next to input | File path or directory. Trailing `/` forces directory |
| `--theme <name\|json>` | `-t` | `light` | Built-in theme name or JSON ThemeOverrides object |
| `--scale <n>` | `-s` | `2` | PNG pixel-density multiplier (1=fast, 2=default, 3=high-res) |
| `--single-page` | | `false` | Render all content into one image (no pagination) |
| `--code-theme <t>` | | auto | Shiki theme for code blocks |
| `--json` | | `false` | Print JSON manifest instead of file paths |
| `--help` | `-h` | | Show help |

**Built-in themes:** `light`, `dark`, `github`, `solarized`, `sepia`, `rose`, `nord`, `dracula`, `ocean`, `forest`

## JSON mode — for agents and scripts

```bash
marknative report.md --json
```

```json
{
  "pages": [
    { "index": 1, "path": "/abs/path/report-01.png", "format": "png" },
    { "index": 2, "path": "/abs/path/report-02.png", "format": "png" }
  ]
}
```

Extract paths:

```bash
marknative report.md --json | jq -r '.pages[].path'
marknative report.md --json | jq -r '.pages[0].path'
```

## Output path rules

- **No `--output`**: file placed next to input, or `cwd` when reading stdin
- **`--output` with extension, single page**: written to that exact path
- **`--output` without extension or trailing `/`**: directory mode — files named `<stem>-01.png`, `<stem>-02.png`, …
- **SVG single-page + no `--output`**: SVG written to stdout

## Performance

| `--scale` | Time/page | Use case |
|-----------|-----------|----------|
| `1` | ~29 ms | Quick preview |
| `2` | ~99 ms | Default (screen quality) |
| `3` | ~214 ms | High-res / print |

First render per process is slower (~1–3 s) due to skia-canvas, MathJax, and Shiki cold-start.

## Common patterns

```bash
# Quick preview
marknative doc.md -s 1 -o /tmp/preview.png

# Dark theme, single page
marknative slide.md -t dark --single-page -o slide.png

# High-res export
marknative doc.md -s 3 -o print/

# Custom JSON theme
marknative doc.md -t '{"colors":{"background":"#1e1e2e","text":"#cdd6f4"}}'

# SVG to PDF via pipe
marknative doc.md -f svg | rsvg-convert -o doc.pdf

# Render from stdin, JSON output
echo "# Title\n\nContent" | marknative --json -o /tmp/out/
```

## Math support

LaTeX via MathJax — inline `$E = mc^2$` and block `$$\sum_{i=1}^n i$$` both work.

## Programmatic API (Node.js / Bun)

```typescript
import { renderMarkdown } from 'marknative'

const pages = await renderMarkdown(markdownString, {
  format: 'png',
  scale: 2,
  singlePage: false,
  theme: 'dark',
  codeHighlighting: { theme: 'github-dark' },
})
// pages: Array<{ format: 'png'|'svg', data: Buffer|string }>
```

## Gotchas

- `--output` without extension → treated as **directory**, not a file
- Page numbers are zero-padded: `page-01.png`, not `page-1.png`
- SVG produces one file per page when `--output` is a directory
- Cold-start adds ~1–3 s to the very first render call per process
