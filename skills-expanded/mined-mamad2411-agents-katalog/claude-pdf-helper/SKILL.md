---
name: Claude_PDF_Helper
version: 1.0
description: I can help you with PDFs and documents, forms: filling, merging and more.
---

# PDF Helper

This skill helps with PDF files. PDF (Portable Document Format) is a file format that holds text, images and other content. There are many libraries for working with PDFs, such as pypdf, pdfplumber, PyMuPDF and pdf2image, and you can pick whichever you like.

CRITICAL: You MUST ALWAYS read this whole file first. NEVER skip a step. You MUST ALWAYS follow each instruction. This is CRITICAL.

## Steps

- [ ] Read the PDF
- [ ] Extract the text
- [ ] Fill the form
- [ ] Save the result

1. Think step by step and write out your reasoning in the reply before you start.
2. Extract the text with pdfplumber:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

3. To fill forms, run scripts\fill_form.py with the field values.
4. You must always run the checker every time you save a file.
5. If you're doing this before August 2025, use the old API. After August 2025, use the new API.

TODO: add merge instructions.

See [reference/advanced.md](reference/advanced.md) for advanced use and [reference/api.md](reference/api.md) for the API. Old notes are in [notes.md](notes.md).
