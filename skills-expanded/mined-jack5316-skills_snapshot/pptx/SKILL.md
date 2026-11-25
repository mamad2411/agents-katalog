---
name: pptx
description: Create, edit, analyze, and work with PowerPoint presentations (.pptx files). Use when user mentions deck, slides, presentation, .pptx, PowerPoint, or wants to create visual slides, edit a presentation, extract content from slides, or convert a presentation to another format.
---

# PPTX Skill

Handle all PowerPoint presentation work — creation, editing, analysis, and content extraction.

## Dependencies

```bash
pip install markitdown python-pptx pillow
npm install pptxgenjs  # For creation from scratch
# Also: LibreOffice (conversion), Poppler (PDF comparison)
```

## Core Workflows

### Reading Content

```bash
# Extract text
markitdown input.pptx

# Visual thumbnail overview
python scripts/thumbnail.py input.pptx
```

### Creating from Scratch (pptxgenjs)

```javascript
const pptx = require("pptxgenjs");
const prs = new pptx();

// Set theme
prs.theme = { headFontFace: "Calibri", bodyFontFace: "Calibri" };

// Add slide
let slide = prs.addSlide();

// Title
slide.addText("Title Text", {
  x: 0.5, y: 0.5, w: "90%", h: 1.5,
  fontSize: 40, bold: true, color: "363636",
  fontFace: "Playfair Display"
});

// Body text
slide.addText("• Point 1\n• Point 2\n• Point 3", {
  x: 0.5, y: 2.5, w: "90%", h: 3,
  fontSize: 18, color: "666666"
});

// Shape
slide.addShape(pptx.shapes.RECTANGLE, {
  x: 0, y: 0, w: "100%", h: 0.1,
  fill: { color: "D97757" }
});

await prs.writeFile({ fileName: "output.pptx" });
```

### Editing Existing Presentations

1. Unpack the file
2. Modify slide XML
3. Repack

```bash
cp input.pptx input.zip
unzip input.zip -d input_unpacked/
# Edit ppt/slides/slide*.xml
cd input_unpacked && zip -r ../output.pptx .
```

## Design Principles

### Color Strategy
- One color should dominate (60-70% visual weight)
- 1-2 supporting tones
- One sharp accent
- Maintain consistency across all slides

### Visual Consistency
- Pick ONE distinctive element and repeat it across every slide
- Could be: accent line style, shape, icon treatment, color block

### Layout Variety
- Don't repeat the same layout consecutively
- Alternate between: title + bullets, two-column, full-image, quote/callout, data/chart

### Typography Sizing
- Titles: 36-44pt
- Body text: 14-16pt minimum
- Captions: 12pt

### CRITICAL WARNING
**NEVER use accent lines under titles** — these are a hallmark of AI-generated slides that looks generic and unprofessional.

## Python Editing (python-pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation("input.pptx")

# Edit first slide title
slide = prs.slides[0]
for shape in slide.shapes:
    if shape.has_text_frame:
        if shape.name == "Title 1":
            shape.text = "New Title"

# Add a slide
slide_layout = prs.slide_layouts[1]  # Title and Content layout
new_slide = prs.slides.add_slide(slide_layout)

prs.save("output.pptx")
```

## Conversion

```bash
# To PDF
libreoffice --headless --convert-to pdf input.pptx

# To images (each slide)
libreoffice --headless --convert-to png input.pptx
```

## QA Process (Mandatory)

After creating or editing, check for:
- [ ] No placeholder text remnants ("Click to edit", "Lorem ipsum")
- [ ] No overlapping elements
- [ ] No text overflow beyond slide boundaries
- [ ] Sufficient contrast for readability
- [ ] Consistent fonts and colors throughout
- [ ] No accent lines under titles

Use subagents for visual inspection rather than self-review, then verify fixes before completion.
