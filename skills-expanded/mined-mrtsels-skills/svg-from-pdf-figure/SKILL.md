---
name: svg-from-pdf-figure
description: Extract figures from PDF slides, analyze them with vision, and recreate as self-contained SVG for embedding in Markdown notes.
---

# SVG from PDF Figure

Extract a figure from a PDF slide, understand its content via vision, and produce a clean standalone SVG for Markdown embedding.

## When to Use

- A lecture/paper PDF has a figure (dendrogram, chart, diagram, flowchart) that you want to include in accompanying Markdown notes
- The PDF's text extraction only yields a caption like "Figure 1: ..." but no structured content
- You want a self-contained vector graphic that renders natively in markdown viewers

## Workflow

### 1. Locate the Figure in the PDF

Use PyMuPDF (`fitz`) to find which page and which images correspond to the figure:

```bash
python3 -c "
import fitz
doc = fitz.open('Lecture N.pdf')
page = doc[PAGE_INDEX]
images = page.get_images(full=True)
print(f'{len(images)} images on page')
for i, img in enumerate(images):
    xref = img[0]
    pix = fitz.Pixmap(doc, xref)
    path = f'/tmp/fig_{i}.png'
    pix.save(path)
    print(f'  [{i}] {pix.width}x{pix.height} → {path}')
"
```

If unsure which page, iterate all pages and check `page.get_text()` for the figure caption (e.g. "Figure 1:" or "Visualization of ...").

### 2. Analyze with Vision

Pass each extracted PNG to `vision_analyze()` with a specific question asking about structure, axis labels, colors, data values:

```
vision_analyze(image_url='/tmp/fig_1.png', question='Describe all visual elements: axes, labels, colors, data points, merge structure, annotations.')
```

From the vision result, extract:
- Chart type and data structure
- Exact axis labels, ranges, tick values
- Merge/group hierarchy and distances
- Color scheme and layout
- Any threshold lines or annotations

### 3. Construct the SVG Manually

Write a self-contained SVG using `write_file`. Rules:

- **Filenames:** use only lowercase letters, digits, and hyphens (no spaces, em dashes, or special chars — they break Markdown image references). Example: `lecture15-dendrogram.svg`
- **Dimensions:** set `viewBox`, `width`, `height` explicitly on `<svg>`.
- **Font:** always set `font-family="Arial, Helvetica, sans-serif"` for portability.
- **Layout:** compute coordinates mathematically in comments (e.g. `<!-- 6 points, from x=110 to x=470, spacing=72 -->`).
- **Colors:** use hex codes, contrast between groups, semantic red for threshold lines.
- **Annotations:** label merge distances, group names, threshold values directly on the SVG.
- **Title:** include a centered title at the top.

### 4. Reference in Markdown

Use standard Markdown image syntax with a **relative path**:

```markdown
![Descriptive Alt Text](lecture15-dendrogram.svg)
```

- Path is relative to the `.md` file location.
- Do NOT URL-encode the path — keep it plain (no `%20`, no `—`, etc.).
- Alt text should describe what the figure shows (accessibility + fallback).

### 5. Commit

Add both the `.md` file and the `.svg` file in the same commit.

## Pitfalls

- **Spaces/special chars in SVG filename** → Markdown image broken. Use only `[a-z0-9-]`.
- **SVG syntax error** → silent failure (no render, no error). Check well-formedness.
- **ViewBox mismatch** → cropped or stretched rendering. Match `viewBox` to desired `width`/`height`.
- **Text too large** → overlaps elements. Use `font-size="10-14"` for annotations, `12-14` for labels.
- **Right-edge text clipped** — the most common layout bug. Elements near the right margin (axis labels, group names like "Cluster W") may exceed the viewBox width and get silently cropped. Build your layout (data points, ellipses, labels) first, then compute the viewBox with **10–15% padding** on all sides. A good check: place the rightmost label's x-coordinate + estimated text width compared to viewBox width.
- **Forgot to save both images from same page** → first `pix.save()` overwrites the second. Always use unique paths per image.
- **Text overplotting on background elements** — draw all lines/shapes first, then redraw points on top so data markers aren't hidden by connector lines.
