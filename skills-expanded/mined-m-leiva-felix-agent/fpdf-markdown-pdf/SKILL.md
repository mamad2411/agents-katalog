---
name: fpdf-markdown-pdf
description: Convert Markdown, text reports, or formatted letters into PDF using Python fpdf2 when CLI converters are absent, ensuring fonts, margins, and styling.
---

# FPDF2 Markdown to PDF Converter

Use this procedure to convert Markdown, structured text, or styled letters into formatted PDF documents on headless Linux environments where Pandoc, Typst, or WeasyPrint are unavailable.

## 1. Prerequisites and Environment Setup

Install `fpdf2` and `pypdf` if not already installed:
```bash
pip3 install --user --break-system-packages fpdf2 pypdf
```

Check available TrueType Unicode fonts (fpdf2 core fonts do not support accented Spanish characters or UTF-8):
```bash
ls /usr/share/fonts/truetype/dejavu/DejaVu*.ttf
```

Avoid `chromium --headless` on headless arm64/Raspberry Pi (unsupported flags cause hangs). WhatsApp gateway also rejects raw local `.html` files under `hostReadCapability`; always render styled documents directly to `.pdf` via `fpdf2`.

## 2. Document Construction Pattern

### Background Fills and Decorative Borders
For formal documents, letters, or certificates, apply background colors and borders before adding text:
```python
# Full-page background fill (A4: 210 x 297 mm)
pdf.set_fill_color(254, 250, 246)
pdf.rect(0, 0, 210, 297, style="F")

# Decorative outer border
pdf.set_draw_color(200, 140, 145)
pdf.set_line_width(0.8)
pdf.rect(15, 15, 180, 267)
```

Create a conversion script with the following strict constraints:

### Unicode and Glyph Sanitization
TrueType fonts such as DejaVuSans lack glyphs for emojis and exotic symbols, causing `fpdf2` to raise missing glyph exceptions. Strip emojis and unrenderable unicode before generating the document:
```python
import re

emoji_pattern = re.compile(
    '[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\u2300-\u23ff\u2b50-\u2b55\u200d\ufe0f]+',
    flags=re.UNICODE
)
clean_text = emoji_pattern.sub('', raw_text)
```

### Cursor and Position Management
In `fpdf2`, calling `multi_cell()` without explicit coordinates defaults to moving `x` rightwards, causing text to drift off the right margin. Always pass:
```python
from fpdf.enums import XPos, YPos

pdf.multi_cell(0, line_height, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
```
For headers and footers, ensure `cell(0, ...)` sets `new_x=XPos.LMARGIN, new_y=YPos.NEXT` or explicitly resets `set_x(l_margin)` to avoid cursor drift.

### Font Configuration
Register Unicode TTF fonts for normal, bold, and italic styles before adding pages (map italic to regular if oblique TTF is missing):
```python
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("Serif", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
pdf.add_font("Serif", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
```

### Tables
Use `pdf.table()` with explicit column widths and a valid `TableBordersLayout` enum (`HORIZONTAL_LINES`, `ALL`, or `NONE`):
```python
with pdf.table(col_widths=col_widths, borders_layout="HORIZONTAL_LINES", line_height=4) as table:
    for row in rows:
        row_cells = table.row()
        for cell_text in row:
            row_cells.cell(cell_text)
```

### Headings and Page Breaks
Check `pdf.get_y()` before rendering major headers to prevent orphaned titles at the bottom of pages:
```python
if pdf.get_y() > 245:
    pdf.add_page()
```

## 3. Verification

After writing the PDF, run an automated position audit using `pypdf` to guarantee no text renders outside page boundaries:

```python
import pypdf

reader = pypdf.PdfReader(output_pdf_path)
out_of_bounds = []

for idx, page in enumerate(reader.pages):
    def check_coords(text, cm, tm, font_dict, font_size):
        x, y = tm[4], tm[5]
        # A4 bounds: 595.28 x 841.89 pt; typical margins: 50 pt < x < 550 pt, 25 pt < y < 825 pt
        if text.strip() and (x < 40 or x > 560 or y < 25 or y > 825):
            out_of_bounds.append((idx + 1, x, y, text[:25]))
    page.extract_text(visitor_text=check_coords)

if out_of_bounds:
    raise ValueError(f"Found {len(out_of_bounds)} text elements outside page margins: {out_of_bounds[:5]}")
```
