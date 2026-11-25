---
name: docx-ops
description: "Use this skill whenever the user wants a Word document (.docx). Key triggers: 'cover letter', 'resume', 'CV', 'application letter', 'reference letter', 'resignation letter', 'Word doc', '.docx', or any request to produce a professional document. Also use for reading/editing existing .docx files, inserting images or tables, or converting content into a polished Word document. Target users are busy college and working women — prioritize clean, professional output that gets results. Do NOT use for PDFs, spreadsheets, or presentations."
---

# DOCX — Cover Letters, Resumes, and Professional Documents

## Primary Use Cases (Creane Users)

| Request | Doc Type | Notes |
|---------|----------|-------|
| "write me a cover letter for [job]" | Cover letter | 1 page, tailored, no filler |
| "help me with my resume" | Resume | ATS-safe, 1-2 pages |
| "make a reference letter" | Reference letter | Formal, from referee's perspective |
| "write a resignation letter" | Resignation | Professional, bridges intact |
| "write a report on [topic]" | Report | Structured, headings, citations |
| "I need a business proposal" | Proposal | Executive summary + sections |

## Quality Standards

Every document must:
- Use **US Letter** page size (python-docx defaults to Letter; docx-js defaults to A4 — always set explicitly)
- Use **Calibri 11pt** body, **14-16pt bold** for name/title headers
- Have consistent **1-inch margins**
- Have **zero typos** — read back the content before delivering
- Be **ATS-friendly** for resumes (no tables, text boxes, columns, or headers/footers for key info — ATS parsers choke on them)

---

## Creating Documents — python-docx (Primary)

`python-docx` is the primary tool. It's already available in the Creane environment.

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
```

### Page Setup (Always Set Explicitly)

```python
doc = Document()
section = doc.sections[0]
section.page_width   = Inches(8.5)   # US Letter
section.page_height  = Inches(11)
section.left_margin  = section.right_margin = Inches(1.0)
section.top_margin   = section.bottom_margin = Inches(1.0)
```

### Cover Letter Pattern

Three paragraphs: hook (why this role + company), evidence (1-2 concrete wins with numbers), close (call to action). No filler, no "I am writing to express my interest."

```python
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import date

doc = Document()
sec = doc.sections[0]
sec.page_width = Inches(8.5); sec.page_height = Inches(11)
for attr in ('left_margin','right_margin','top_margin','bottom_margin'):
    setattr(sec, attr, Inches(1.0))

def para(doc, text="", bold=False, size=11, after=6, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    return p

# Header
para(doc, "JANE DOE", bold=True, size=14)
para(doc, "jane.doe@email.com  |  (555) 123-4567  |  linkedin.com/in/janedoe")
para(doc)  # spacer

# Recipient block
para(doc, date.today().strftime("%B %d, %Y"))
para(doc)
para(doc, "Hiring Manager")
para(doc, "Cleveland Clinic")
para(doc)

# Salutation
para(doc, "Dear Hiring Manager,")
para(doc)

# Body — write real, tailored content here
para(doc, "[Hook: why this role at this company — specific, not generic.]")
para(doc)
para(doc, "[Evidence: one or two accomplishments with numbers. 'I reduced X by 20%', 'managed Y patients per shift', etc.]")
para(doc)
para(doc, "[Close: enthusiasm + call to action. Keep it short.]")
para(doc)

# Sign-off
para(doc, "Sincerely,")
para(doc)
para(doc, "Jane Doe")

doc.save("cover_letter.docx")
```

### Resume Pattern (ATS-Safe)

ATS systems fail on: tables, text boxes, columns, graphics, headers/footers. Use plain paragraphs only.

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

doc = Document()
sec = doc.sections[0]
sec.page_width = Inches(8.5); sec.page_height = Inches(11)
for attr in ('left_margin','right_margin','top_margin','bottom_margin'):
    setattr(sec, attr, Inches(1.0))

BLUE = RGBColor(0x1F, 0x49, 0x7D)

def section_heading(doc, text):
    """Section label with a colored bottom border — no table, ATS-safe."""
    p = doc.add_paragraph()
    r = p.add_run(text.upper())
    r.bold = True; r.font.size = Pt(11); r.font.color.rgb = BLUE
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after  = Pt(3)
    # Bottom border
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F497D')
    pBdr.append(bottom)
    pPr.append(pBdr)

def bullet_item(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(text).font.size = Pt(10.5)
    p.paragraph_format.space_after = Pt(2)

def job_line(doc, title_company, dates):
    """Job title + right-aligned dates on same line using tab stop."""
    p = doc.add_paragraph()
    r1 = p.add_run(title_company); r1.bold = True; r1.font.size = Pt(11)
    r2 = p.add_run(f"\t{dates}"); r2.font.size = Pt(10.5)
    p.paragraph_format.tab_stops.add_tab_stop(Twips(9360), WD_ALIGN_PARAGRAPH.RIGHT)
    p.paragraph_format.space_after = Pt(2)

# --- Name ---
name_p = doc.add_paragraph()
name_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
nr = name_p.add_run("JANE DOE"); nr.bold = True; nr.font.size = Pt(18)

contact_p = doc.add_paragraph()
contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
contact_p.add_run("jane@email.com  |  (555) 123-4567  |  City, ST  |  linkedin.com/in/janedoe").font.size = Pt(10)

# --- Summary (2-3 lines max) ---
section_heading(doc, "Summary")
p = doc.add_paragraph()
p.add_run("Nursing student with clinical experience in ICU and med-surg. Strong patient advocate, 3.8 GPA.").font.size = Pt(10.5)

# --- Experience ---
section_heading(doc, "Experience")
job_line(doc, "Clinical Extern — Cleveland Clinic", "Jun 2024 – Present")
bullet_item(doc, "Assisted RNs with 8-12 patients per shift in 32-bed med-surg unit.")
bullet_item(doc, "Reduced patient call light response time by 18% through proactive rounding.")

# --- Education ---
section_heading(doc, "Education")
job_line(doc, "B.S. Nursing — Cleveland State University", "Expected May 2025")
p = doc.add_paragraph(); p.add_run("GPA: 3.8  |  Dean's List 3 semesters").font.size = Pt(10.5)

# --- Skills ---
section_heading(doc, "Skills")
doc.add_paragraph().add_run("Epic EMR, IV Therapy, Patient Assessment, HIPAA, BLS/ACLS Certified").font.size = Pt(10.5)

doc.save("resume.docx")
```

### Tables (Non-Resume Documents Only)

```python
from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def shade_cell(cell, hex_color, text_color=None):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)
    if text_color:
        for run in cell.paragraphs[0].runs:
            run.font.color.rgb = RGBColor.from_string(text_color)

table = doc.add_table(rows=1, cols=3)
table.style = 'Table Grid'

# Header row
hdr = table.rows[0].cells
for i, label in enumerate(["Column A", "Column B", "Column C"]):
    hdr[i].text = label
    shade_cell(hdr[i], '1F497D', 'FFFFFF')
    hdr[i].paragraphs[0].runs[0].bold = True

# Data rows
for row_data in [["A1", "B1", "C1"], ["A2", "B2", "C2"]]:
    row = table.add_row().cells
    for i, val in enumerate(row_data):
        row[i].text = val
```

## Advanced: docx-js (Complex Formatting)

When python-docx can't do it (complex tab stops, multi-column layouts, automatic TOC), use docx-js.

```bash
npm install -g docx
```

```javascript
const { Document, Packer, Paragraph, TextRun, AlignmentType,
        HeadingLevel, LevelFormat, TabStopType, TabStopPosition } = require('docx');
const fs = require('fs');

// CRITICAL: Always set US Letter — docx-js defaults to A4
const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },  // 1440 DXA = 1 inch
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [/* content */]
  }]
});

Packer.toBuffer(doc).then(buf => fs.writeFileSync("output.docx", buf));
```

### Critical docx-js Rules
- **Never use `\n`** — use separate `Paragraph` elements
- **Never use unicode bullets** (`•`) — use `LevelFormat.BULLET` with numbering config
- **Always `WidthType.DXA` for tables** — PERCENTAGE breaks in Google Docs
- **Tables need dual widths** — `columnWidths` on table AND `width` on each cell, both must match
- **Use `ShadingType.CLEAR`** — never SOLID (causes black cell backgrounds)
- **`PageBreak` must be inside a `Paragraph`** — standalone breaks XML

## Reading / Editing Existing Documents

```python
from docx import Document

doc = Document("existing.docx")

# Read all text
for para in doc.paragraphs:
    print(para.style.name, ":", para.text)

# Find and replace
for para in doc.paragraphs:
    for run in para.runs:
        if "OLD TEXT" in run.text:
            run.text = run.text.replace("OLD TEXT", "NEW TEXT")

doc.save("updated.docx")
```

## QA Checklist

- [ ] US Letter page size (8.5 x 11 inches)
- [ ] No typos in name, job title, company, dates
- [ ] Consistent font and sizes throughout
- [ ] Cover letter: 3 focused paragraphs, fits on 1 page
- [ ] Resume: no tables or text boxes (ATS-killers)
- [ ] File opens cleanly in Word and Google Docs

## Dependencies

```bash
pip install python-docx
npm install -g docx   # only for complex formatting needs
```
