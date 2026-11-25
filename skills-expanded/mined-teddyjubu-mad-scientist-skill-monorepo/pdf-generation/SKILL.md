---

name: pdf-generation
description: pdf-generation lets the user create PDF documents from text, HTML, or structured data when weasyprint fails due to font subsetting bugs, using fpdf2 as a reliable fallback so they can still produce clean, usable PDFs for reports, invoices, or printed materials.
category: productivity

---
## What This Skill Does

This skill pdf-generation lets the user create PDF documents from text, HTML, or structured data when weasyprint fails due to font subsetting bugs, using fpdf2 as a reliable fallback so they can still produce clean, usable PDFs for reports, invoices, or printed materials.

## Known Issue: Weasyprint Font Subsetting Bug

Weasyprint crashes on this system with:
```
ValueError: expected 0 <= int <= 122, found: 123
```

**Root cause:** Liberation fonts have Unicode range bits > 122 in the `OS/2` table. fontTools `subset._prune_post_subset()` calls `recalcUnicodeRanges()` which throws on bits >= 127. This happens across fontTools 4.59.2 - 4.62.1.

**Do NOT waste time on:**
- Downgrading fontTools (breaks weasyprint dependencies)
- `--pdf-identifier` flags (doesn't affect subsetting)
- Upgrading/downgrading weasyprint (same fontTools dependency chain)

## Working Approach: fpdf2

### 1. Install in the Hermes venv
```bash
cd /root/.hermes/hermes-agent
./venv/bin/python3 -m pip install --force-reinstall --no-cache-dir "fonttools[woff]==4.59.2"
./venv/bin/python3 -m pip install fpdf2 --no-input
```

**Important:** If fontTools was previously installed but can't import (`No module named 'fontTools'`), force reinstall with `--force-reinstall --no-cache-dir`. The package may show as installed in `pip list` but be corrupted.

### 2. Font Paths
Check actual font files before assuming paths:
```bash
find /usr/share/fonts -name "DejaVuSans*" 2>/dev/null
```

**Available on this system:**
- `DejaVuSans.ttf` (Regular)
- `DejaVuSans-Bold.ttf` (Bold)
- `DejaVuSansMono.ttf` (Mono Regular)
- `DejaVuSansMono-Bold.ttf` (Mono Bold)
- `DejaVuSansMono-Oblique.ttf` (Mono Italic)
- `DejaVuSansMono-BoldOblique.ttf` (Mono Bold Italic)

**Note:** `DejaVuSans-Oblique.ttf` (Sans Italic) does NOT exist. Use the regular `DejaVuSans.ttf` as fallback.

### 3. Basic PDF Pattern
```python
from fpdf import FPDF

pdf = FPDF('P', 'mm', 'Letter')
pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')

pdf.add_page()
pdf.set_font('DejaVu', 'B', 16)
pdf.cell(0, 10, 'Title', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('DejaVu', '', 10)
pdf.multi_cell(0, 6, 'Body text...')
pdf.output('/tmp/output.pdf')
```

### 4. Key API Notes
- `rect(x, y, w, h, 'DF')` — use `'DF'` (draw+fill), NOT `fill=True` keyword
- `new_x='LMARGIN'` — return to left margin after cell
- `new_y='NEXT'` — move to next line after cell
- `pdf.set_auto_page_break(auto=True, margin=18)` — enable auto pagination
- Dark backgrounds: call `pdf.rect(0, 0, 210, 297, 'F')` before adding content
- Cards/boxes: use `rect()` for backgrounds + `line()` for accent borders
- **`uni=True` in `add_font()` is deprecated** since v2.5.1 — remove it. Still works with deprecation warning.
- **Italic fonts must be registered explicitly** — fpdf2 won't auto-synthesize italics. If you use `set_font('DejaVu', 'I', ...)`, you MUST first call `pdf.add_font('DejaVu', 'I', '/path/to/font.ttf', uni=True)` or it will crash with "Undefined font". If DejaVuSans-Oblique.ttf doesn't exist (it doesn't on this system), use regular DejaVuSans.ttf as the italic fallback.
- **`pdf.no_of_pages`** (property) — NOT `pdf.pages_count()`. Access page count with `pdf.no_of_pages` (it's an int property, not a method).
- **`set_xy(x, y)`** — use before `rect()` to position drawing cursor correctly. Without it, overlapping elements may render in wrong positions.
- **Letter size**: `FPDF('P', 'mm', 'Letter')` — default Letter is 216×279mm. Use `pdf.rect(0, 0, 216, 279, 'F')` for full-page background fills on Letter, or `210×297` for A4.

### 5. execute_code vs terminal
- `execute_code` runs in an isolated sandbox — **cannot import system-wide packages**
- Either install in sandbox (ephemeral) or write script to `/tmp/` and run with `./venv/bin/python3 /tmp/script.py`
- fpdf2 must be installed in `/root/.hermes/hermes-agent/venv/` for venv python to access it

### 6. Dark Theme PDFs (all-page backgrounds)

**CRITICAL: `pdf.page` is a reserved FPDF property — do NOT name a method `page(self)`.** It causes `TypeError: 'int' object is not callable`.

When using `set_auto_page_break(auto=True, margin=X)`, fpdf2 creates **blank white pages** on auto-breaks. For dark-themed PDFs, every page (even auto-generated ones) needs a background fill:

```python
def mkpage(pdf):
    """Helper: add page + fill dark background + red top accent."""
    pdf.add_page()
    fill_dark_page(pdf)

def fill_dark_page(pdf):
    """Must call after EVERY add_page() — even auto page breaks."""
    pdf.set_fill_color(12, 12, 16)
    pdf.set_xy(0, 0)          # CRITICAL: reset x before rect at abs coords
    pdf.rect(0, 0, 216, 279, 'F')   # Letter size fill
    pdf.set_fill_color(220, 40, 40)
    pdf.set_xy(0, 0)
    pdf.rect(0, 0, 216, 3, 'F')     # Top red accent line

# Usage:
mkpage(pdf)           # explicit page
# ... content ...
# When auto page break fires, the new page is WHITE.
# To fix: check Y before overflow, call mkpage() explicitly:
if pdf.get_y() > 160:  # threshold — tune for your content
    mkpage(pdf)        # dark background applied
# ... more content ...

# Bottom red accent (on last page):
pdf.set_xy(0, 276)   # reset x before absolute rect
pdf.set_fill_color(220, 40, 40)
pdf.rect(0, 276, 216, 3, 'F')
```

**Pro tip:** Use `pdf.get_y()` to debug page breaks. Log Y positions as you build:
```python
print(f"  {label}: page={pdf.page_no()}, y={pdf.get_y():.0f}mm")
```
Letter page height = 279mm. With 16mm bottom margin, content must end before ~263mm.

### 7. Deliver via Telegram
Include the path in your response: `MEDIA:/tmp/output.pdf`
