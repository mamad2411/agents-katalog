---
name: linkedin-carousel
description: "Convert slides into LinkedIn-ready carousel PDFs. Triggers: 'create LinkedIn carousel', 'convert slides to carousel', 'carousel PDF from images', 'PPTX to carousel', 'slides to PDF for LinkedIn'. Supports square (1080x1080) and vertical (1080x1350) formats from HTML slides, image folders, or PowerPoint files."
license: MIT
---

# LinkedIn Carousel Skill

Convert slides into LinkedIn-ready carousel PDFs.

## Workflow Overview

1. **Choose input method**: HTML slides (recommended), image folder, or PPTX
2. **Select format**: Square (1080×1080) or Vertical (1080×1350)
3. **Generate PDF**: Run script or use code pattern below
4. **Upload to LinkedIn**: As document post

## Quick Start

### Option 1: HTML Slides to Carousel (Recommended)

```javascript
const { chromium } = require('playwright');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

const WIDTH = 1080, HEIGHT = 1080;
const slides = [`<html>...</html>`, `<html>...</html>`]; // Your HTML slides

async function createCarousel(outputPath) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: WIDTH, height: HEIGHT });
  
  const pdfDoc = await PDFDocument.create();
  for (const html of slides) {
    await page.setContent(html, { waitUntil: 'networkidle' });
    const img = await pdfDoc.embedPng(await page.screenshot({ type: 'png' }));
    const p = pdfDoc.addPage([WIDTH * 0.75, HEIGHT * 0.75]);
    p.drawImage(img, { x: 0, y: 0, width: p.getWidth(), height: p.getHeight() });
  }
  await browser.close();
  fs.writeFileSync(outputPath, await pdfDoc.save());
}

createCarousel('carousel.pdf');
```

### Option 2: Image Folder or PPTX

```bash
# From images
node scripts/pptx-to-carousel.js ./my-slides/ output.pdf --format square

# From PowerPoint (requires LibreOffice)
node scripts/pptx-to-carousel.js presentation.pptx carousel.pdf
```

## Scripts Reference

| Script | Usage |
|--------|-------|
| `pptx-to-carousel.js` | `node scripts/pptx-to-carousel.js <input> [output.pdf] [--format square\|vertical]` |
| `render-slides.js` | `renderSlidesToImages(htmlSlides, outputDir, width, height)` |

## LinkedIn Requirements

| Spec | Value |
|------|-------|
| **Square** | 1080×1080 px (recommended) |
| **Vertical** | 1080×1350 px |
| **Safe zone** | 960×960 px centered |
| **Slides** | 2-20 per carousel |
| **Format** | Multi-page PDF |

## Best Practices

1. **Hook slide first** - Compelling title to drive swipes
2. **One idea per slide** - Don't overcrowd
3. **CTA on final slide** - Clear call to action
4. **Min 24pt font** - Readable on mobile
5. **Consistent branding** - Colors/style across slides

## Dependencies

```bash
npm install playwright sharp pdf-lib adm-zip
npx playwright install chromium
```

## References

- **Detailed specs**: `references/linkedin-specs.md`
- **Full examples**: `references/examples.md`
