---
name: pptx
description: Create, edit, and read PowerPoint presentations (.pptx) with python-pptx. Use whenever the user wants slides as output — a deck, pitch, briefing, training, or report presentation — or uploads a .pptx to summarize, restyle, update, or extend, even if they only say “slides” or “deck”.
license: Apache-2.0
compatibility: Tines 3B
---

# PowerPoint presentations

Work with `.pptx` files in Python through `execute`, adding `python-pptx==1.0.2` to a `requirements.txt` in `files`. In a workflow step, add it to the step’s `requirements.txt` instead.

User uploads arrive under `/3b/uploads/<id>/<file>`, which every execution can read. Write output to a persistent volume, such as `volumes: ["documents"]` and `/storage/documents/briefing.pptx`, then call `showStorageFile` so the user can preview and download it. Never overwrite the user’s upload: save edits as a new file, and call `showStorageFile` again after each change.

## Reading

```python
from pptx import Presentation

prs = Presentation("/3b/uploads/abc/deck.pptx")
for number, slide in enumerate(prs.slides, start=1):
    print(f"--- Slide {number} ({slide.slide_layout.name})")
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text.strip():
            print(shape.text_frame.text)
        if shape.has_table:
            for row in shape.table.rows:
                print(" | ".join(cell.text for cell in row.cells))
    if slide.has_notes_slide:
        print("Notes:", slide.notes_slide.notes_text_frame.text)
```

Group shapes hold their own `shapes`, so recurse into them when text seems missing.

## Plan the deck before writing code

Draft the outline as text first: one line per slide with its title and the point it makes. Confirm it with the user when the request is open-ended. The outline is cheap to change, and the code is not.

- **One idea per slide, with the title stating it.** “Phishing reports doubled after the training” beats “Phishing reports”.
- **Keep text short.** At most five or six bullets, each a single line. Move detail into speaker notes.
- **Show numbers as charts or big figures**, not as sentences full of digits.
- **Be consistent.** Use one title position, one margin, two fonts at most, and a palette of a neutral, a dark text color, and one or two accents.

## Creating

When the user supplies a template or an existing deck in their branding, open it and add slides from its layouts. Its masters carry fonts, colors, and logos you shouldn’t recreate by hand. Otherwise, start from the default and switch it to 16:9, because python-pptx’s default is 4:3.

```python
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
TITLE_ONLY = prs.slide_layouts[5]
ACCENT = RGBColor(0x1F, 0x4E, 0x79)

slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Security operations, Q3"
slide.placeholders[1].text = "Board briefing"

slide = prs.slides.add_slide(TITLE_ONLY)
slide.shapes.title.text = "Phishing reports doubled after the training"
data = CategoryChartData()
data.categories = ["Jul", "Aug", "Sep"]
data.add_series("Reports", (120, 180, 260))
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.75), Inches(1.6), Inches(11.8), Inches(5.4), data
).chart
chart.has_legend = False
chart.plots[0].series[0].format.fill.solid()
chart.plots[0].series[0].format.fill.fore_color.rgb = ACCENT
slide.notes_slide.notes_text_frame.text = "Training launched July 14."

slide = prs.slides.add_slide(TITLE_ONLY)
slide.shapes.title.text = "Next steps"
body = slide.shapes.add_textbox(Inches(0.75), Inches(1.6), Inches(11.8), Inches(5)).text_frame
body.word_wrap = True
for index, line in enumerate(["Roll out to contractors", "Automate triage of reports"]):
    paragraph = body.paragraphs[0] if index == 0 else body.add_paragraph()
    paragraph.text = line
    paragraph.font.size = Pt(24)

prs.save("/storage/documents/briefing.pptx")
```

- The default template’s layouts are 0 title, 1 title and content, 5 title only, and 6 blank. A user template has its own, so list `layout.name` for each layout and each placeholder’s `placeholder_format.idx` before you pick one.
- After widening the default template to 16:9, its placeholders keep their 4:3 positions. Use title-only or blank layouts and place your own text boxes, or reposition each placeholder.
- Use native charts (`add_chart`) and tables (`add_table`) so the user can edit them in PowerPoint. Reserve matplotlib images for chart types PowerPoint lacks.
- Add images with `slide.shapes.add_picture(path, left, top, width=...)`. Set only width or only height so the aspect ratio holds.
- Use 36–44 pt for titles, 20–28 pt for body text, and nothing below 14 pt.

## Text doesn’t shrink to fit

python-pptx writes text without measuring it, and auto-fit happens only when PowerPoint edits the shape, so long text silently overflows its box. Size boxes generously and keep text within these rough limits for a 16:9 slide: a title of about 60 characters on one line, and about 45 characters per line of 24 pt body text in a full-width box. Split a slide in two before shrinking the font.

## Editing an existing deck

- Replace text run by run, keeping each run’s formatting, rather than setting `text_frame.text`, which resets it.
- python-pptx has no public API to delete, duplicate, or reorder slides. Reorder by moving entries in `prs.slides._sldIdLst`. Delete by removing the entry and dropping the relationship: `prs.part.drop_rel(entry.rId)`.
- Fill a slide from the template’s layouts instead of copying shapes between decks, because shapes copied between files lose their images and charts.

## Check the result

Reopen the saved file and print each slide’s title, its shape count, and any shape that extends past the slide edge (`shape.left + shape.width > prs.slide_width`, and the same for height). Then call `showStorageFile` so the user can page through the rendered deck, and summarize the slide list for them.
