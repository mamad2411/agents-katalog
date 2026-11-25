---
name: readable-pdf
description: Extracts text (with original line breaks), metadata, per-page character / image density, and optional rendered PNGs from a PDF using pdfvision. Falls back to --render on pages whose density Overview shows low text coverage so multimodal models can read raster slides. Use when the URL ends in .pdf, the user supplies a local PDF path, or another readable-* skill produced a PDF that still needs structured extraction.
---

# PDF Reader

Uses [pdfvision](https://github.com/yamadashy/pdfvision) for cross-agent PDF extraction. pdfvision returns text with line breaks preserved, document metadata, per-page density, and optional rendered PNGs for multimodal models.

## Prerequisite

```bash
npx pdfvision --version
```

Or install globally: `npm install -g pdfvision`. Requires Node.js >= 22.13.

Run `npx pdfvision --help` once before invoking — the flag set evolves (page selection, render output dir, layout / geometry / image-boxes opt-ins, etc.) and the help text is the source of truth for what the installed version supports.

## Steps

### 1. Get a local PDF path

If the input is a URL, download first:

```bash
curl -L -o /tmp/doc.pdf "{URL}"
```

If the input is already a local path, skip this step.

### 2. Extract text + metadata

```bash
npx pdfvision /tmp/doc.pdf
```

Default output is `markdown` with one `## Page N` section per page and a density Overview at the top.

### 3. Switch format when needed

```bash
# Structured JSON for downstream programmatic use
npx pdfvision /tmp/doc.pdf -f json

# Tag-shaped XML, easier for some LLMs to parse than JSON
npx pdfvision /tmp/doc.pdf -f xml
```

### 4. Render pages for multimodal review

If the Overview shows low character coverage on a page (i.e. the page is largely an image / scan), render PNGs and read them:

```bash
npx pdfvision /tmp/doc.pdf --render -p {pages}
```

The output reports the PNG paths. Read each image with the agent's image-reading capability.

### 5. Page subsets

```bash
npx pdfvision /tmp/doc.pdf -p 1-5
npx pdfvision /tmp/doc.pdf -p 1,3,5
```

## Why pdfvision over a built-in PDF reader

- Works in any agent runtime that can spawn a CLI, not only Claude Code.
- Reports per-page density so the agent can detect rasterised pages and re-extract with `--render`.
- Caches by content hash, so repeated reads of the same PDF are instant.
