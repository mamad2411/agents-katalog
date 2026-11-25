---
name: pdf-processing
description: Processes, extracts and verifies existing PDF files. Use whenever the user wants to read text or tables from a PDF, OCR a scanned PDF, merge, split, rotate or compress PDFs, inspect metadata, or check that extracted data matches the source, even if they only say "get the data out of this PDF". Every pipeline ends with a verification step. For creating new styled PDFs use pdf-atelier instead.
---

# pdf-processing

A repeatable workflow for reading, transforming and verifying existing PDF files. Extraction is never trusted blindly: every pipeline ends with a verification step.

```
pdf-processing/
├── SKILL.md
├── scripts/
│   ├── pdf_inspect.sh         health report: metadata, integrity, words per page, scanned verdict
│   └── verify_extraction.py   cross-check pdftotext vs pdfplumber per page (exit 1 on mismatch)
└── references/
    ├── ocr-and-rtl.md         OCR decision table, language data, Persian/Arabic/Hebrew fixes, tables
    └── recipes.md             split, merge, compress, encrypt, images, metadata, batch, Termux
```

## When to use

- Extract text or tables from digital PDFs
- OCR scanned PDFs
- Merge, split, rotate or compress PDFs
- Validate that extracted data matches the source document
- Inspect metadata, fonts and structure

To create a new styled PDF, use `pdf-atelier`. To process or verify an existing one, use this skill.

## Workflow

1. **Inspect**: run `bash scripts/pdf_inspect.sh input.pdf`. It reports page count, encryption, integrity and a verdict on the text layer.
2. **Choose strategy**: text layer present means direct extraction; missing or mixed means OCR (see `references/ocr-and-rtl.md`).
3. **Extract**: keep the page number with every extracted chunk.
4. **Normalize**: fix hyphenation, whitespace, encoding and RTL ordering.
5. **Verify**: run `python3 scripts/verify_extraction.py input.pdf`, then the manual checklist below.
6. **Report**: return the data with a confidence note and known gaps. Say which pages were flagged.

## Tool selection

| Task | Tool |
|------|------|
| Fast text extraction | `pdftotext` (poppler-utils) |
| Tables and layout | `pdfplumber` |
| Merge, split, rotate | `qpdf`, `pypdf` |
| OCR | `ocrmypdf`, `tesseract` |
| Integrity check | `qpdf --check` |

For ready commands (split, compress, encrypt, images, batch) read `references/recipes.md`.

## Core commands

```bash
pdfinfo input.pdf
pdftotext -layout input.pdf output.txt
ocrmypdf --skip-text -l eng+fas --deskew input.pdf output_ocr.pdf
qpdf --empty --pages a.pdf b.pdf -- merged.pdf
```

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        for table in page.extract_tables():
            print(f"page {i}:", table)
```

## Verification checklist

Automated first, manual second.

```bash
python3 scripts/verify_extraction.py input.pdf --tolerance 0.15
```

- Output page count equals source page count
- No page is flagged as low text unless it is truly an image page
- Numbers, dates and totals agree between two methods
- Sample 3 random pages and compare against the rendered image
- Table row and column counts match the source, including the total row
- Record a SHA-256 checksum of input and output files

```bash
sha256sum input.pdf output.pdf
pdftoppm -r 80 -f 3 -l 3 -png input.pdf check_page
```

## Output contract

When reporting results to the user, include:

| Field | Example |
|-------|---------|
| Source | `report.pdf`, 12 pages, sha256 `fa28...` |
| Method | `pdftotext -layout`, verified with `pdfplumber` |
| Flagged pages | pages 4 and 9 (low text), re-run with OCR |
| Confidence | high / medium / low with one reason |
| Known gaps | charts not extracted, footnotes merged into body |

## Common pitfalls

- Scanned PDFs return empty text, so run OCR first
- Multi-column layouts scramble reading order, so use `-layout` or crop regions
- RTL text (Persian, Arabic, Hebrew) may extract reversed, so verify against the render
- Ligatures and hyphenation break search, so normalize before indexing
- Never overwrite the original file; write to a new path

## Related skills

- `pdf-atelier`: creates styled PDFs; this skill processes and verifies existing ones
- `systematic-debugging`: apply when an extraction pipeline gives wrong output
- `multi-agent-orchestration`: use this skill as the extraction worker in a pipeline
