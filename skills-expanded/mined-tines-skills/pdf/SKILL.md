---
name: pdf
description: Read, extract from, create, fill, merge, split, and watermark PDF files with pdfplumber, pypdf, and ReportLab. Use whenever the user uploads a PDF to summarize, extract text or tables from, or fill in, or wants a PDF as output — a report, invoice, letter, certificate, or a combined or redacted copy of other PDFs.
license: Apache-2.0
compatibility: Tines 3B
---

# PDFs

Work with PDFs in Python through `execute`, adding the libraries you need to a `requirements.txt` in `files`: `pdfplumber==0.11.10` for extraction, `pypdf==6.20.1` for page and form operations, and `reportlab==5.0.1` for creating new PDFs. In a workflow step, add them to the step’s `requirements.txt` instead.

User uploads arrive under `/3b/uploads/<id>/<file>`, which every execution can read. Write output to a persistent volume, such as `volumes: ["documents"]` and `/storage/documents/report.pdf`, then call `showStorageFile` so the user can preview and download it. Never overwrite the user’s upload.

## Reading

For a short PDF, call `readStorageFile` on it: it returns the PDF for you to view directly, including its layout, charts, and scanned pages. Use code when the document is long, when you need exact values, or when you need tables as data:

```python
import pdfplumber

with pdfplumber.open("/3b/uploads/abc/invoice.pdf") as pdf:
    print(len(pdf.pages), pdf.metadata)
    for number, page in enumerate(pdf.pages, start=1):
        print(f"--- Page {number}")
        print(page.extract_text() or "[no text layer]")
        for table in page.extract_tables():
            for row in table:
                print(row)
```

A page with no text layer is a scan. OCR tools aren’t installed in the sandbox, so view those pages with `readStorageFile` instead. Use `page.crop((x0, top, x1, bottom))` to read one region, such as a header block or a single column of a multi-column layout.

## Creating

Use ReportLab’s Platypus layer. It flows paragraphs, tables, and images across pages, so you don’t position each line by hand.

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

styles = getSampleStyleSheet()

def footer(canvas, doc):
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(LETTER[0] - inch, 0.6 * inch, f"Page {doc.page}")

doc = SimpleDocTemplate("/storage/documents/report.pdf", pagesize=LETTER, title="Incident report",
                        leftMargin=inch, rightMargin=inch, topMargin=inch, bottomMargin=inch)
table = Table([["System", "Impact", "Status"], ["Okta", "Login delays", "Resolved"]],
              colWidths=[2 * inch, 2.75 * inch, 1.75 * inch], repeatRows=1)
table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F2F2")]),
]))
doc.build([
    Paragraph("Incident report", styles["Title"]),
    Paragraph("Login delays on <b>October 3</b> affected 4% of users for 22 minutes.", styles["BodyText"]),
    Spacer(1, 12),
    table,
], onFirstPage=footer, onLaterPages=footer)
```

- `Paragraph` takes a small HTML-like markup (`<b>`, `<i>`, `<font>`, `<br/>`), so escape `&`, `<`, and `>` in user text with `xml.sax.saxutils.escape`.
- ReportLab’s built-in fonts (Helvetica, Times, Courier) cover only Latin-1, so other characters render as black boxes. For other text, register a TrueType font. The sandbox includes Liberation fonts under `/usr/share/fonts/truetype/liberation/`, and they cover Latin, Greek, and Cyrillic: `pdfmetrics.registerFont(TTFont("Liberation", ".../LiberationSans-Regular.ttf"))`.
- Use A4 instead of Letter (`from reportlab.lib.pagesizes import A4`) for users outside North America.
- Add charts as images: render a PNG with matplotlib at 200 DPI or more and add it with `reportlab.platypus.Image(path, width=..., height=...)`, keeping the aspect ratio.
- For a document the user wants to edit afterward, produce a DOCX with the `docx` skill instead.

## Page operations and forms

```python
from pypdf import PdfReader, PdfWriter

writer = PdfWriter()
for path in ("/3b/uploads/a/cover.pdf", "/3b/uploads/b/body.pdf"):
    writer.append(path)
writer.add_metadata({"/Title": "Combined report"})
writer.write("/storage/documents/combined.pdf")
```

- **Split or extract pages:** `writer.append(reader, pages=(0, 3))` copies pages 1–3.
- **Rotate:** `page.rotate(90)`.
- **Watermark or stamp:** build a one-page PDF with ReportLab, then call `page.merge_page(stamp_page)` on each page.
- **Fill a form:** list the fields with `reader.get_fields()`. Then call `writer = PdfWriter(clone_from=reader)` and `writer.update_page_form_field_values(writer.pages[0], {"name": "Ada"}, auto_regenerate=False)`, and set `writer.set_need_appearances_writer(True)` so viewers draw the new values.
- **Password-protect:** `writer.encrypt(user_password)`. Open an encrypted input with `reader.decrypt(password)`.

Drawing a black box over text doesn’t redact it, because the text stays in the file and remains selectable. For real redaction, rebuild the affected pages without the text, or explain the limitation to the user.

## Check the result

Call `readStorageFile` on the output to view it as the user will: check page breaks, table overflow, fonts, and that nothing is cut off at the margins. Fix any problems, then call `showStorageFile` and tell the user the page count and what the document contains.
