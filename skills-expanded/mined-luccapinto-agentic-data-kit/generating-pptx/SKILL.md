---
name: generating-pptx
description: Use when the user needs an EDITABLE PowerPoint (.pptx) deliverable — "make a PowerPoint", "export to PPTX", "editable slides", "send me a .pptx". Generates native, fully editable PowerPoint (real text boxes, shapes, native charts with embedded data, tables) via python-pptx — not images. Brand colors map from DESIGN.md. For HTML decks/sites/PDF use building-html-presentations instead.
---

# Skill: generating-pptx

Produce a **native, editable** PowerPoint with `python-pptx`. Every element is a real PowerPoint
object — editable text, shapes, **native charts** (backed by embedded data you can edit in
PowerPoint), and tables. This is the right path when the deliverable must be `.pptx` and editable;
for HTML decks, interactive sites, or designed PDFs use `building-html-presentations`.

> Why not HTML→PPTX? Exporting an HTML deck to PPTX (e.g. Marp `--pptx`) embeds each slide as a
> flat **image** — not editable. `python-pptx` builds the real OOXML, so charts and text stay live.

## Setup
```bash
pip install python-pptx
```

## Build it
`scripts/build_pptx.py` is a working generator — a brand-themed sales deck with a title slide,
agenda, KPI slide, **native charts** (clustered column, line, pie), a table slide, and a closing.
Run it, then adapt:
```bash
python .claude/skills/generating-pptx/scripts/build_pptx.py --out deck.pptx
```

Adapt by editing the `DATA`, `BRAND`, and the `build()` slide calls — not the helpers.

## What python-pptx gives you (the palette)
- **Native charts** (editable, with embedded Excel data): `COLUMN_CLUSTERED`, `COLUMN_STACKED`,
  `BAR_CLUSTERED`, `LINE`, `LINE_MARKERS`, `PIE`, `DOUGHNUT`, `XY_SCATTER`, `AREA`, `RADAR`. Use
  `CategoryChartData` for category charts and `XyChartData` for scatter.
- **Tables** via `slide.shapes.add_table(rows, cols, ...)` — style cells, headers, number formats.
- **Text** via placeholders or `add_textbox` → `text_frame` → paragraphs/runs (font, size, color, bold).
- **Shapes / KPI cards** via `add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ...)` with fill + text.
- **Brand**: set `RGBColor` from your `DESIGN.md` tokens; reuse one accent + semantic colors.

## Rules
- **Map brand from DESIGN.md** — colors, and font name if defined. Keep one accent.
- **Native charts over images** — let the user edit data in PowerPoint.
- **Never invent data** — use provided numbers; mark placeholders. Add a source line per data slide.
- **16:9** by default (`Inches(13.333) × Inches(7.5)`).
- Action-title style: the slide title states the insight, not just the topic.
