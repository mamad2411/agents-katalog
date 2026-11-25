---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX Skill

Work with Word documents (.docx files) for creation, editing, and analysis.

## Dependencies

```bash
npm install docx           # JavaScript library for creation
pip install python-docx    # Python library for reading/editing
# Also: pandoc, LibreOffice (for conversion), poppler (for PDF comparison)
```

## Document Creation (JavaScript/Node.js)

Use the `docx` npm package for creating documents:

```javascript
const { Document, Paragraph, TextRun, Table, TableRow, TableCell, HeadingLevel, PageSize } = require("docx");
const fs = require("fs");

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: {
          width: 12240,  // Letter width in DXA (8.5" × 1440)
          height: 15840, // Letter height in DXA (11" × 1440)
        }
      }
    },
    children: [
      new Paragraph({
        text: "Document Title",
        heading: HeadingLevel.HEADING_1,
      }),
      new Paragraph({
        children: [
          new TextRun("Normal paragraph text. "),
          new TextRun({ text: "Bold text", bold: true }),
          new TextRun({ text: " and italic", italics: true }),
        ],
      }),
    ],
  }],
});

// Save
const buffer = await Packer.toBuffer(doc);
fs.writeFileSync("output.docx", buffer);
```

## Critical Rules

- **Set page size explicitly** — docx-js defaults to A4, not Letter
- **Always use DXA units** for table widths (never percentages)
  - 1 inch = 1440 DXA
  - Letter width = 12240 DXA (8.5")
  - A4 width = 11906 DXA
- **PageBreak must be in Paragraph** — not standalone
- **Smart quotes**: Encode as XML entities in raw XML editing

## Tables

```javascript
const table = new Table({
  rows: [
    new TableRow({
      children: [
        new TableCell({
          children: [new Paragraph("Cell 1")],
          width: { size: 4320, type: WidthType.DXA },  // 3 inches
        }),
        new TableCell({
          children: [new Paragraph("Cell 2")],
          width: { size: 4320, type: WidthType.DXA },
        }),
      ],
    }),
  ],
  width: { size: 8640, type: WidthType.DXA },  // 6 inches total
});
```

## Document Editing (Python)

```python
from docx import Document

doc = Document("input.docx")

# Read paragraphs
for para in doc.paragraphs:
    print(para.style.name, para.text)

# Edit paragraph
doc.paragraphs[0].text = "New title"

# Add paragraph
doc.add_paragraph("New paragraph text")

doc.save("output.docx")
```

## XML Editing

For fine-grained edits, unpack and edit the XML directly:

```bash
# Unpack
cp input.docx input.zip
unzip input.zip -d input_unpacked/

# Edit word/document.xml directly
# Use Edit tool for string replacement — DO NOT write Python scripts for this

# Repack
cd input_unpacked
zip -r ../output.docx .
```

**Use the Edit tool directly for string replacement — do not write Python scripts.**

## Conversion

```bash
# To PDF
pandoc input.docx -o output.pdf
libreoffice --headless --convert-to pdf input.docx

# From Markdown
pandoc input.md -o output.docx

# To HTML
pandoc input.docx -o output.html
```

## Headers and Footers

```javascript
const doc = new Document({
  sections: [{
    headers: {
      default: new Header({
        children: [new Paragraph("Header text")],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
        })],
      }),
    },
    children: [...],
  }],
});
```

## Google Docs Compatibility

- Avoid complex nested tables
- Use standard heading styles (Heading 1, 2, 3)
- Stick to common fonts (Arial, Times New Roman, Calibri)
- Test tracked changes compatibility if using XML edits
