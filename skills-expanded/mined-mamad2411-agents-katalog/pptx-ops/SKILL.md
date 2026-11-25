---
name: pptx-ops
description: "Use this skill any time a .pptx file is involved. Key triggers: 'slides', 'presentation', 'deck', '.pptx', 'PowerPoint', 'class presentation', 'project slides', 'pitch deck'. Target users are busy college and working women — class presentations, group project slides, job fair pitch decks, club proposals, internship reports. Also use for reading or editing existing presentations. Trigger whenever the user mentions 'deck', 'slides', or 'presentation' and wants a file output."
---

# PPTX — Class Presentations, Pitch Decks, and Slide Decks

## Primary Use Cases (Creane Users)

| Request | Presentation Type | Notes |
|---------|------------------|-------|
| "make slides for my bio class on [topic]" | Academic presentation | 8-12 slides, structured |
| "I need a pitch deck for my startup idea" | Pitch deck | Problem/solution/market/ask |
| "presentation for my group project" | Group project deck | Clean, professional, teammates can edit |
| "slides for my job fair presentation" | Career pitch | Who I am, skills, what I want |
| "club proposal slides" | Proposal deck | Hook, plan, ask for support |
| "internship report presentation" | Report deck | Summary, findings, recommendations |

## Quality Standards

Every presentation must:
- Have a **consistent visual theme** — one color palette, one font pairing, carried through every slide
- Have **at least one visual element per slide** — image placeholder, icon, chart, or shape (no pure bullet dumps)
- Have **strong size contrast** — titles 32-40pt, body 16-18pt, captions 11-12pt
- Use **left-aligned body text** — centered titles only
- **Never use accent lines under titles** (hallmark of AI slides — use whitespace instead)
- Be **immediately presentable** — no lorem ipsum, no placeholder text

---

## Color Palettes for Creane Users

Pick one palette and commit. Don't mix.

| Theme | Primary | Secondary | Accent | Best For |
|-------|---------|-----------|--------|----------|
| Berry & Cream | `6D2E46` | `A26769` (dusty rose) | `ECE2D0` (cream) | Nursing, health, fashion |
| Sage Calm | `84B59F` | `69A297` (eucalyptus) | `50808E` (slate) | Biology, environment, wellness |
| Teal Trust | `028090` | `00A896` (seafoam) | `02C39A` (mint) | Business, data, tech |
| Coral Energy | `F96167` | `F9E795` (gold) | `2F3C7E` (navy) | Marketing, creative, energetic |
| Charcoal Minimal | `36454F` | `F2F2F2` (off-white) | `212121` (black) | Minimalist, professional |
| Midnight Executive | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` | Finance, formal proposals |
| Warm Terracotta | `B85042` | `E7E8D1` (sand) | `A7BEAE` (sage) | Social sciences, humanities |

One color dominates (60-70% visual weight), one supports, one accents. Never give all three equal weight.

---

## Typography

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Trebuchet MS | Calibri |
| Cambria | Calibri |
| Arial Black | Arial |

| Element | Size |
|---------|------|
| Slide title | 32-40pt bold |
| Section header | 22-26pt bold |
| Body text | 16-18pt |
| Captions / footnotes | 11-12pt muted |

---

## Creating Presentations — python-pptx (Primary)

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
```

### Standard Slide Deck Pattern

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Color palette (Teal Trust example)
PRIMARY   = RGBColor(0x02, 0x80, 0x90)
SECONDARY = RGBColor(0x00, 0xA8, 0x96)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
DARK      = RGBColor(0x1A, 0x1A, 0x2E)
BODY_GREY = RGBColor(0x33, 0x33, 0x33)

prs = Presentation()
prs.slide_width  = Inches(13.33)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # blank — full control

def add_rect(slide, left, top, width, height, hex_color):
    """Add a colored rectangle shape."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hex_color)
    shape.line.fill.background()  # no border
    return shape

def add_text_box(slide, text, left, top, width, height, size, bold=False, color=None, align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    return txBox

# ---- Title Slide ----
title_slide = prs.slides.add_slide(BLANK)
add_rect(title_slide, 0, 0, 13.33, 7.5, "028090")          # full background
add_rect(title_slide, 0, 4.8, 13.33, 2.7, "1A1A2E")        # dark bottom strip
add_text_box(title_slide, "Presentation Title", 1, 1.5, 11, 2, 40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text_box(title_slide, "Subtitle or Course Name", 1, 3.5, 11, 1, 20, color=RGBColor(0xCA, 0xDC, 0xFC), align=PP_ALIGN.CENTER)
add_text_box(title_slide, "Your Name  |  Date", 1, 5.5, 11, 1, 14, color=RGBColor(0xAA, 0xBB, 0xCC), align=PP_ALIGN.CENTER)

# ---- Content Slide (Two-column: text left, visual placeholder right) ----
def content_slide(prs, title, bullets):
    slide = prs.slides.add_slide(BLANK)
    # Top color bar
    add_rect(slide, 0, 0, 13.33, 0.7, "028090")
    # Title
    add_text_box(slide, title, 0.3, 0.05, 12, 0.65, 26, bold=True, color=WHITE)
    # Bullet content
    txBox = slide.shapes.add_textbox(Inches(0.4), Inches(1.0), Inches(7.5), Inches(5.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {bullet}"
        p.font.size = Pt(18)
        p.font.color.rgb = BODY_GREY
        p.space_after = Pt(10)
    # Right side placeholder (image or chart goes here)
    placeholder = slide.shapes.add_shape(1, Inches(8.2), Inches(1.0), Inches(4.7), Inches(5.5))
    placeholder.fill.solid()
    placeholder.fill.fore_color.rgb = RGBColor(0xF0, 0xF5, 0xF5)
    placeholder.line.color.rgb = SECONDARY
    add_text_box(slide, "[Image / Chart]", 8.2, 3.0, 4.7, 1, 14, color=SECONDARY, align=PP_ALIGN.CENTER)
    return slide

content_slide(prs, "Key Point 1", [
    "Supporting fact or explanation",
    "Another point — keep it to one idea per bullet",
    "Use numbers when possible: 73% of students...",
])

# ---- Closing Slide ----
closing = prs.slides.add_slide(BLANK)
add_rect(closing, 0, 0, 13.33, 7.5, "1A1A2E")
add_text_box(closing, "Thank You", 0, 2.5, 13.33, 2, 48, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_text_box(closing, "Questions?", 0, 4.5, 13.33, 1, 22, color=SECONDARY, align=PP_ALIGN.CENTER)

prs.save("presentation.pptx")
```

### Academic Presentation Structure (8-10 slides)

```
1. Title slide      — Topic, your name, course, date
2. Agenda           — What we'll cover (3-5 items)
3. Background       — Why this topic matters
4. Main point 1     — Claim + evidence + visual
5. Main point 2     — Claim + evidence + visual
6. Main point 3     — Claim + evidence + visual
7. Analysis         — What does it mean / implications
8. Conclusion       — 3-sentence summary of what you proved
9. References       — APA or MLA, consistent
10. Q&A             — Thank you + contact (optional)
```

### Pitch Deck Structure (8-10 slides)

```
1. Title / Hook     — Bold claim or problem statement
2. Problem          — Who has this problem, how painful
3. Solution         — What Creane / your idea does
4. How It Works     — 3-step flow, simple
5. Market           — Who are the users, how many
6. Traction         — What's working so far
7. Business Model   — How it makes money
8. Ask              — What you need / want from the audience
9. Team             — Who's behind it
10. Thank You / Q&A
```

## Reading Existing Presentations

```python
from pptx import Presentation

prs = Presentation("existing.pptx")
for i, slide in enumerate(prs.slides):
    print(f"\n--- Slide {i+1} ---")
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                if para.text.strip():
                    print(para.text)
```

## QA Checklist

- [ ] No leftover placeholder text ("[Image]", "Lorem ipsum", "Click to add")
- [ ] Consistent font sizes across same-type elements across slides
- [ ] All slides have at least one visual element (not pure text)
- [ ] Title slide has presenter name and date
- [ ] Closing slide is clean (no orphaned content)
- [ ] File opens correctly in PowerPoint and Google Slides

## Converting to Images (for Visual QA)

```bash
# Requires LibreOffice and poppler
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 150 presentation.pdf slide
# Creates slide-01.jpg, slide-02.jpg, etc.
```

## Dependencies

```bash
pip install python-pptx
pip install "markitdown[pptx]"   # text extraction from existing files
```
