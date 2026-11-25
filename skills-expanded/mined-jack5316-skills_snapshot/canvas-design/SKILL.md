---
name: canvas-design
description: Create sophisticated visual art and designs through a two-phase process: design philosophy then visual expression in PDF or PNG format. Use when the user wants to create visual art, design posters, create visual compositions, generate design files, or produce museum-quality visual output.
---

# Canvas Design Skill

Create sophisticated visual art through a two-phase process: establishing a design philosophy, then expressing it visually.

## Phase 1: Design Philosophy

Before creating anything visual, establish a clear aesthetic direction:

1. **Understand the purpose**: What is this design communicating?
2. **Choose a tone**: From brutalist to maximalist, minimal to ornate
3. **Identify constraints**: Format, colors, audience, context
4. **Write the philosophy**: 4-6 substantial paragraphs describing the visual aesthetic movement

The philosophy should emphasize:
- Spatial communication and artistic interpretation
- "Minimal text as visual accent" — text is a design element, not primary content
- Subtle, niche references embedded within the art
- The craftsmanship principle: work must appear "meticulously crafted"

## Phase 2: Visual Expression

Express the philosophy as a single-page PDF or PNG with:
- Sophisticated, minimal typography
- Systematic visual language
- Museum-quality execution
- "Pristine" composition — nothing falls off the page, nothing overlaps

### Quality Standards

- **Expert-level execution**: Each element reflects painstaking care
- **Conceptual depth**: Identify subtle references that add layers of meaning
- **Visual hierarchy**: Clear spatial organization guiding the eye
- **Restraint**: Less is more — remove anything that doesn't serve the philosophy

## Output Formats

- **Philosophy**: Markdown file (4-6 substantial paragraphs)
- **Visual**: Single-page PDF or PNG

## Tools

Use Python with `reportlab` for PDF generation:

```python
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

c = canvas.Canvas("design.pdf", pagesize=A4)
width, height = A4

# Design elements
c.setFillColor(colors.HexColor('#141413'))
c.rect(0, 0, width, height, fill=1)

# Typography
c.setFont("Helvetica", 48)
c.setFillColor(colors.HexColor('#faf9f5'))
c.drawCentredString(width/2, height/2, "Title")

c.save()
```

## Design Principles

1. **Visual philosophy first** — never jump to implementation
2. **One dominant idea** — not a collection of effects
3. **Intentionality** — every element has a reason to exist
4. **Niche reference** — embed sophisticated meaning for informed viewers
5. **Spatial precision** — exact positioning, no accidents
