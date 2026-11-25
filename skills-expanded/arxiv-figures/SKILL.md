---
name: arxiv-figures
description: 'Optimize and prepare figures for arXiv submission: format conversion (EPS/PDF/PNG/JPG), size reduction, metadata stripping, processor compatibility (DVI vs PDFLaTeX). Triggers on: "optimize figures for arXiv", "reduce figure size", "convert figures for arXiv", "fix arXiv figures", "figure too large", "arxiv image compression". Companion to arxiv-preflight and arxiv-package.'
metadata:
  version: 1.0.0
  complements: [arxiv-preflight, arxiv-package, manuscript-review]
  category: review
  tags: [arxiv, figures, optimization, latex, submission]
  difficulty: intermediate
  phase: ship
---

# arXiv Figure Optimizer

## Purpose

Analyze, optimize, and convert figures in a TeX/LaTeX project to meet arXiv
requirements and size constraints. Produces correctly formatted, efficiently
compressed figures that compile without errors.

Companion skills:
- `arxiv-preflight` — full submission validation
- `arxiv-package` — tarball packaging

## Format Rules

### By Processor

| Processor | Accepted | Rejected |
|-----------|----------|----------|
| LaTeX (DVI mode) | `.ps`, `.eps` | `.pdf`, `.png`, `.jpg` |
| PDFLaTeX | `.pdf`, `.png`, `.jpg` | `.ps`, `.eps` |

### By Content Type

| Content | Optimal Format | Rationale |
|---------|---------------|-----------|
| Photographs | JPEG | Lossy compression suits continuous tone |
| Line drawings / diagrams | PDF (vector) | Scalable, sharp at any resolution |
| Plots with text labels | PDF (vector) | Text remains crisp and searchable |
| Screenshots / raster art | PNG | Lossless compression for sharp edges |
| Mixed photo + text | PNG or PDF | Depends on dominant content |

## Workflow

### 1. Inventory

Scan the project for all figures:
- Parse `\includegraphics` calls from all `.tex` files
- Identify the TeX processor (DVI vs PDFLaTeX) from document preamble or build config
- For each figure: record path, format, file size, dimensions (pixels or vector bounds)
- Flag missing figures, wrong-format figures, oversized figures

### 2. Analyze

For each figure, determine:

1. **Format compliance** — does the format match the processor?
2. **File size** — flag individual figures >2MB, total >15MB
3. **Resolution** — PNG/JPEG: flag >34 Megapixels (arXiv warning threshold since Feb 2026)
4. **Content type** — photograph vs diagram vs plot (determines optimal format)
5. **Redundant metadata** — PNG: ICC profiles, alpha channels, EXIF, interlacing
6. **EPS efficiency** — verbose PostScript from plotting programs (common with matplotlib, R, MATLAB)

### 3. Optimize

Apply transformations in order of impact:

**Format Conversion** (when format violates processor requirements)
```bash
# EPS → PDF (for PDFLaTeX)
epstopdf figure.eps
# or
ps2pdf -dEPSCrop figure.eps figure.pdf

# PDF/PNG/JPG → EPS (for DVI mode)
convert figure.png figure.eps
```

**Size Reduction — Vector Figures**
```bash
# Distill verbose EPS
eps2eps input.eps output.eps
# or convert to PDF
ps2pdf -dEPSCrop input.eps output.pdf
```

**Size Reduction — Raster Figures**
```bash
# Strip PNG metadata, remove alpha, optimize compression
convert input.png -strip -alpha remove -define png:compression-level=9 output.png

# Reduce oversized PNG resolution (keep ≤300 DPI at print size)
convert input.png -resize 3000x3000\> -strip output.png

# JPEG quality optimization (80-90 is visually lossless for most content)
convert input.jpg -quality 85 -strip output.jpg

# Downsample oversized JPEG
convert input.jpg -resize 3000x3000\> -quality 85 -strip output.jpg
```

**PNG Optimization** (avoid arXiv warnings)
- Remove palette indexing if unnecessary
- Remove alpha channel if background is solid
- Strip ICC color profiles
- Remove metadata chunks
- Disable interlacing

**EPS BoundingBox Fix** (prevents `Missing number, treated as zero`)
- Verify `%%BoundingBox` appears near top of file, not only at end
- If only `%%BoundingBox: (atend)`, extract actual values and place at top

### 4. Update TeX Source

If figures were renamed or reformatted:
1. Update `\includegraphics` paths
2. Remove explicit extensions where possible (allows processor flexibility)
3. Verify `\graphicspath` settings if used

### 5. Verify

After optimization:
1. Attempt local compilation to verify all figures render
2. Compare visual output of optimized vs original figures
3. Report size reduction per figure and total

### 6. Report

```markdown
# Figure Optimization Report

**Processor:** [detected]
**Total figures:** [count]
**Size before:** [total MB]
**Size after:** [total MB]
**Reduction:** [percentage]

## Changes Made

| Figure | Original | Optimized | Size Before | Size After | Action |
|--------|----------|-----------|-------------|------------|--------|
| fig1 | fig1.eps | fig1.pdf | 12.3 MB | 0.4 MB | EPS→PDF conversion |
| fig2 | fig2.png | fig2.png | 8.1 MB | 1.2 MB | Strip metadata, downsample |

## Warnings

[Any remaining issues — e.g., figures still above thresholds]
```

## Tools Reference

| Tool | Install | Use Case |
|------|---------|----------|
| ImageMagick (`convert`) | System package | Format conversion, resizing, stripping |
| Ghostscript (`ps2pdf`, `eps2eps`) | System package | EPS/PS optimization and conversion |
| `epstopdf` | TeX Live | EPS → PDF conversion |
| `pdfcrop` | TeX Live | Trim PDF whitespace |
| `optipng` | System package | PNG lossless optimization |
| `pngquant` | System package | PNG lossy size reduction |
| `jpegoptim` | System package | JPEG lossless optimization |

## Core Principles

- **Never degrade visual quality below print-readable.** Optimization means
  removing waste (metadata, unnecessary resolution, verbose encoding), not
  destroying information.
- **Match format to processor.** A figure in the wrong format blocks compilation.
  This is the highest priority fix.
- **Preserve vector where possible.** Converting vector to raster is a one-way
  quality loss. Only do this when the vector version is pathologically large
  (>10MB) and cannot be distilled.
- **Report everything.** The user decides which optimizations to accept. Show
  before/after sizes and explain each transformation.
