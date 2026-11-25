---
name: pdf-document-transformer
description: Extract, analyze, reconstruct, edit, improve, redact, convert, and export PDFs. Use for PDF-to-Word, PDF-to-PPTX, revised PDFs, scanned PDFs, OCR, flattened PDF reconstruction, presentation PDFs, redaction, metadata/privacy cleanup, and final PDF export from Word or PowerPoint.
---

# PDF Document Transformer

Use this skill when the source, target, or final consumed artifact is a PDF.

## Required resources

Read the relevant resources before acting:

- `../word-document-studio/SKILL.md` when the output should be editable Word.
- `../presentation-document-studio/SKILL.md` when the output should be editable PowerPoint or a presentation PDF.
- `../document-quality-gate/SKILL.md` before delivery.
- `../../beautiful-prose/SKILL.md` and `../../beautiful-prose/references/ai-tells.md` for substantial prose changes.
- `../../visual-design-skill.txt` for visual redesign or title pages.

## PDF intake classification

Classify the PDF first:

- Text-layer PDF: extract text, tables, images, page count, and structure.
- Scanned/image-only PDF: use OCR when available; label uncertain text.
- Flattened design PDF: reconstruct layout in Word or PowerPoint; exact editability is limited.
- Presentation PDF: rebuild as PPTX when editing slides matters.
- Form or contract PDF: preserve fields and legal/financial meaning; do not alter obligations without explicit instruction.

## Transformation paths

- PDF to polished Word: extract/reconstruct into `.docx`, improve prose/layout, render, optionally export PDF.
- PDF to revised PDF: edit source-native file if available; otherwise reconstruct in DOCX/PPTX and export new PDF.
- PDF to PowerPoint: rebuild each page/slide into editable slide structure where practical.
- Word/PPTX to PDF: use Word or PowerPoint export, not screenshot assembly, unless no native exporter is available.
- Redacted PDF: redact source text/assets carefully, then verify redaction is not just a visual overlay.

## Reconstruction standards

- Preserve reading order, headings, tables, figures, footnotes, and captions where possible.
- Recreate useful structure, not just pasted text.
- Mark OCR uncertainty and illegible regions.
- For financial, legal, medical, or compliance documents, preserve source wording unless the user explicitly requests rewriting.
- Do not claim pixel-perfect reconstruction unless the rendered output proves it.

## PDF visual standards

- Check page count and orientation.
- Watch for clipped text, missing fonts, rasterized low-resolution text, bad page breaks, oversized margins, and table overflow.
- Verify charts and tables remain readable.
- If source was scanned, inspect critical names, numbers, dates, IDs, and totals at high fidelity before using them.

## Delivery

Deliver the final requested file type. If the user asked for editability and a final PDF, deliver both `.docx`/`.pptx` and `.pdf`.
