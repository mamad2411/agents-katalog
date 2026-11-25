---
name: pdf-ops
description: "Use this skill whenever the user wants to do anything with PDF files. Key triggers: 'PDF', '.pdf', 'summarize this PDF', 'read this paper', 'extract text from', 'create a PDF report', 'research summary'. Target users are busy college and working women — reading research papers, creating polished report PDFs, extracting data from uploaded documents, merging assignment files. Do NOT use for Word documents, spreadsheets, or presentations unless the user explicitly wants a PDF output."
---

# PDF — Reports, Research, and Document Processing

## Primary Use Cases (Creane Users)

| Request | Operation | Notes |
|---------|-----------|-------|
| "summarize this research paper" | Extract + summarize | Use pdfplumber for layout-aware extraction |
| "create a report as PDF" | Generate PDF | Use reportlab — clean typography |
| "extract the data from this PDF" | Extract tables | pdfplumber handles complex layouts |
| "combine these assignment PDFs" | Merge | pypdf |
| "split this PDF by chapter" | Split | pypdf by page range |
| "what does this PDF say about X?" | Q&A over content | Extract full text, then answer |

---

## Reading / Extracting PDFs — pdfplumber (Primary)

`pdfplumber` is the best tool for layout-aware text extraction.

```python
import pdfplumber

# Text extraction
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            print(text)

# Table extraction
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                print(row)

# Extract all text as one string
with pdfplumber.open("document.pdf") as pdf:
    full_text = "\n".join(
        page.extract_text() or "" for page in pdf.pages
    )
```

### Extract Tables to DataFrame

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("report.pdf") as pdf:
    all_dfs = []
    for page in pdf.pages:
        for table in page.extract_tables():
            if table and len(table) > 1:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_dfs.append(df)

if all_dfs:
    combined = pd.concat(all_dfs, ignore_index=True)
    combined.to_excel("extracted_tables.xlsx", index=False)
```

---

## Creating PDFs — reportlab

Use reportlab for generating polished, formatted PDFs from scratch.

### Research Summary / Report

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

doc = SimpleDocTemplate(
    "research_summary.pdf",
    pagesize=letter,
    leftMargin=inch, rightMargin=inch,
    topMargin=inch, bottomMargin=inch,
)

styles = getSampleStyleSheet()
BRAND_BLUE = colors.HexColor("#1F497D")

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=20,
    textColor=BRAND_BLUE,
    spaceAfter=6,
)
heading_style = ParagraphStyle(
    "CustomHeading",
    parent=styles["Heading1"],
    fontSize=14,
    textColor=BRAND_BLUE,
    spaceBefore=16,
    spaceAfter=6,
    borderPad=4,
)
body_style = ParagraphStyle(
    "CustomBody",
    parent=styles["Normal"],
    fontSize=11,
    leading=16,   # line spacing
    spaceAfter=8,
)
caption_style = ParagraphStyle(
    "Caption",
    parent=styles["Normal"],
    fontSize=9,
    textColor=colors.grey,
    spaceAfter=4,
)

story = []

# Title block
story.append(Paragraph("Research Summary: Sleep Deprivation in College Students", title_style))
story.append(Paragraph("Prepared by Jane Doe  |  April 2025", caption_style))
story.append(Spacer(1, 20))

# Section
story.append(Paragraph("Overview", heading_style))
story.append(Paragraph(
    "This report summarizes current research on sleep deprivation among college students, "
    "covering prevalence, academic impact, and evidence-based interventions.",
    body_style
))

# Data table
story.append(Paragraph("Key Statistics", heading_style))
table_data = [
    ["Metric", "Finding", "Source"],
    ["Students sleeping <6 hrs", "60%", "American Sleep Association 2023"],
    ["GPA impact", "-0.4 per hour lost", "Curcio et al., 2024"],
    ["At-risk for depression", "2.5x more likely", "ACHA-NCHA 2023"],
]
t = Table(table_data, colWidths=[2.2*inch, 2.2*inch, 2.6*inch])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0, 0), (-1, 0), BRAND_BLUE),
    ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
    ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE",    (0, 0), (-1, 0), 10),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FC")]),
    ("FONTSIZE",    (0, 1), (-1, -1), 10),
    ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
    ("TOPPADDING",  (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(t)
story.append(Spacer(1, 16))

doc.build(story)
```

### CRITICAL: No Unicode Sub/Superscripts in ReportLab

Built-in fonts don't include unicode subscript/superscript glyphs — they render as black boxes.

```python
# WRONG — unicode subscript renders as black box
p = Paragraph("H₂O", styles['Normal'])

# CORRECT — use ReportLab XML tags inside Paragraph
p = Paragraph("H<sub>2</sub>O", styles['Normal'])
p2 = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

---

## Merging and Splitting PDFs — pypdf

```python
from pypdf import PdfWriter, PdfReader

# Merge multiple PDFs
writer = PdfWriter()
for filename in ["assignment1.pdf", "assignment2.pdf", "cover.pdf"]:
    reader = PdfReader(filename)
    for page in reader.pages:
        writer.add_page(page)
with open("combined.pdf", "wb") as f:
    writer.write(f)

# Split by page range
reader = PdfReader("textbook.pdf")
writer = PdfWriter()
for page in reader.pages[4:9]:    # pages 5-9 (0-indexed)
    writer.add_page(page)
with open("chapter1.pdf", "wb") as f:
    writer.write(f)

# Extract text
reader = PdfReader("document.pdf")
for page in reader.pages:
    print(page.extract_text())
```

---

## Command-Line Tools

```bash
# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Merge (qpdf)
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages 1-5
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# Remove password
qpdf --password=PASSWORD --decrypt encrypted.pdf decrypted.pdf
```

---

## Quick Reference

| Task | Best Tool |
|------|-----------|
| Extract text with layout | pdfplumber |
| Extract tables | pdfplumber |
| Create new PDF | reportlab |
| Merge PDFs | pypdf |
| Split PDFs | pypdf |
| Command-line merge | qpdf |
| OCR scanned PDF | pytesseract + pdf2image |

---

## QA Checklist

- [ ] Extracted text is complete — no missing sections or cut-off pages
- [ ] Tables extracted cleanly with correct columns
- [ ] Generated PDFs have no glyph errors (black boxes from unicode chars)
- [ ] Margins and layout look clean when opened
- [ ] File size is reasonable (< 5 MB for text reports)

---

## Dependencies

```bash
pip install pdfplumber pypdf reportlab
pip install pytesseract pdf2image  # for OCR on scanned PDFs
```
