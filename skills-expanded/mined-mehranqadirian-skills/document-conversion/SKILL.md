---
name: document-conversion
description: Converts documents between Markdown, Word, HTML, PDF, EPUB and plain text with pandoc, including right-to-left Persian, Arabic and Hebrew layouts. Use whenever the user asks to convert, export or turn one document format into another, such as markdown to docx, docx to markdown, html to pdf, or wants a readable offline copy of notes, even if they only say "give me this as a Word file". Never overwrites the input and verifies the result.
---

# document-conversion

Convert a document to another format without losing structure, and check the result. PDF is a one way street: pandoc cannot read it, so extraction goes through `pdf-processing`.

```
document-conversion/
├── SKILL.md
├── scripts/
│   └── convert_doc.sh          pandoc wrapper: docx, html, pdf, epub, md, txt; --rtl, --toc
└── references/
    └── formats-and-rtl.md      format choice, conversion matrix, RTL checklist, fixes
```

## When to use

- Markdown to Word, HTML, PDF or EPUB
- Word to Markdown or HTML
- Making a shareable PDF from notes
- Persian, Arabic or Hebrew documents that must keep right-to-left direction

For a beautiful designed PDF, use `pdf-atelier`. For reading data out of an existing PDF, use `pdf-processing`.

## Workflow

1. **Pick the target** with the table in `references/formats-and-rtl.md`. If the user did not say, ask what the file is for.
2. **Convert**: `bash scripts/convert_doc.sh notes.md docx --rtl --toc --title "Report"`
3. **Verify** (checks are listed in the reference): page count, text sample, images, RTL direction.
4. **Report** the output path, size and anything that did not survive.

## Commands

```bash
bash scripts/convert_doc.sh notes.md docx
bash scripts/convert_doc.sh notes.md html --rtl
bash scripts/convert_doc.sh notes.md pdf --rtl --toc --out report.pdf
bash scripts/convert_doc.sh report.docx md
```

PDF uses the first available route: `wkhtmltopdf` from HTML, then LibreOffice from DOCX, then XeLaTeX. In Termux, prefer docx or html and make the PDF on a computer.

## Rules

- Never overwrite the input; the script refuses when output equals input
- Use `--rtl` for Persian, Arabic and Hebrew, and check one page visually
- Do not promise a faithful PDF to Word conversion; say it is lossy
- Mention features that will not convert: comments, tracked changes, complex tables, fonts
- Keep source Markdown in version control; treat converted files as build outputs

## What to report back

| Field | Content |
|-------|---------|
| Output | path, format, size |
| Options used | rtl, toc, title, route for PDF |
| Verified | page count, text sample, RTL check |
| Lost or changed | items that did not survive |

## Related skills

- `pdf-atelier`: designed, themed PDFs from scratch
- `pdf-processing`: extract and verify content from existing PDFs
- `termux-setup`: install pandoc and manage files on a phone
