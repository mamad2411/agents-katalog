---
name: pdf-processor
description: Inspect, extract, search, render, merge, split, create, convert, and validate PDF documents. Use for text and page extraction, scanned or image-heavy review, document assembly, chapter/page separation, Office-to-PDF delivery, PDF-to-DOCX conversion, and visual quality assurance of final office artifacts.
---

# PDF Processing

## Inspect before processing

Run `mcp__pdf__process` with `operation: "get-info"` before reading or modifying a PDF. Record page count, page size, metadata, encryption state, outline, and whether useful text is extractable.

Do not assume that a PDF with no extracted text is empty. Render representative pages to determine whether it is scanned, image-based, malformed, or protected.

## Choose the operation

- Use `extracttext` with an explicit page range for targeted reading and summarization.
- Use `search` with an explicit page range to locate terms without loading the whole document.
- Use `render` to return one page immediately for focused visual inspection.
- Use `to-images` to convert all or selected pages to predictably numbered PNG files for batch review; always set `pages` for large documents unless every page is required.
- Use `merge` only after confirming source order; inspect the merged page count and boundaries.
- Use `split` with explicit pages and clear output naming.
- Use `mcp__convert__convert` for Office-to-PDF and PDF-to-DOCX conversion.
- Use the PDF `create` operation only for simple text output. Create a styled source document with DOCX/PPTX or a suitable PDF library, then convert or export it for professional layouts.

The built-in PDF tool does not perform general OCR, form-field filling, annotation, redaction, signing, or password removal. Do not claim those actions succeeded. Use visual review, desktop software, or a purpose-built workflow only when available and authorized.

## Preserve meaning and order

- Keep page order, orientation, dimensions, bookmarks, and document boundaries intentional.
- Preserve the original file and write to a new output by default.
- Do not treat visual concealment as redaction; underlying PDF content may remain recoverable.
- Do not remove passwords, signatures, permissions, or security controls without explicit authorization.
- When summarizing, distinguish extracted text from visual interpretation and cite page numbers.
- When converting to editable formats, warn that pagination, fonts, tables, columns, and reading order may change.

## Process large documents efficiently

1. Inspect structure and outline.
2. Search or extract only relevant page ranges.
3. Render pages whose layout or images affect interpretation.
4. Summarize sections before combining conclusions.
5. Keep page-number references aligned with the original PDF.

## Validate before delivery

Read [quality-and-safety.md](references/quality-and-safety.md) and apply checks proportional to risk. At minimum:

1. Reopen the output and confirm page count, order, dimensions, and expected content.
2. Use `to-images` for the first, last, transition, rotated, and content-dense pages; convert every page for short or presentation-critical documents.
3. Check blank pages, clipping, font substitution, low-resolution images, broken links, and accidental metadata disclosure.
4. Compare source and output after conversion, merge, or split.
5. Remove temporary renders from the delivery folder and state any unverified security, accessibility, or fidelity issue.
