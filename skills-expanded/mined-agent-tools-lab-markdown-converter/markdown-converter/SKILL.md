---
name: markdown-converter
description: Convert PDF to Markdown, including scanned PDFs with bundled local OCR; convert DOCX, XLSX, PPTX, HTML, CSV, JSON, XML, and TXT to editable Markdown; and convert Markdown to searchable PDF, Office, ebook, publishing, data, text, and image formats. Use when Codex or Claude needs a private, network-free document converter, Markdown formatter, or verified non-empty output without installing conversion dependencies or adding watermarks.
---

# Markdown Converter

Use the bundled command-line runtime. It processes files locally and does not call a website or conversion API. Resolve the absolute directory containing this `SKILL.md` and keep it in a task-scoped variable such as `MARKDOWN_CONVERTER_DIR`; do not assume the current working directory is the Skill directory.

## Convert a file

Use Node.js 20 or newer:

```bash
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" INPUT --to FORMAT -o OUTPUT
```

Common examples:

```bash
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" report.pdf --to markdown -o report.md
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" scan.pdf --to markdown --ocr-language eng -o scan.md
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" report.docx --to markdown -o report.md
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" workbook.xlsx --to markdown -o workbook.md
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" deck.pptx --to markdown -o deck.md
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" notes.md --to pdf -o notes.pdf
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" notes.md --to docx -o notes.docx
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" notes.md --to png -o notes.png
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" notes.md --to card --theme dark -o notes-card.png
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" notes.md --to html --stdout
```

Add `--locale en|es|ja|zh-CN|de` for generated labels and document metadata. The locale also selects the default PDF OCR language. Override it with `--ocr-language eng|spa|deu|jpn|chi_sim`. OCR is automatic only when a PDF page has no readable text layer; add `--no-ocr` to reject such pages instead. Card accepts `--theme light|dark`. Add `--force` only when the user authorized replacing the destination.

Run the following command before promising an unfamiliar conversion:

```bash
node "$MARKDOWN_CONVERTER_DIR/scripts/runtime/convert.mjs" --capabilities
```

Read `references/format-matrix.md` before promising fidelity for PDF, binary, publishing, or visual formats.

## Supported inputs

- Markdown, HTML, TXT, CSV, JSON, and XML
- PDF with an existing text layer
- Image-only PDF pages through bundled local OCR for English, Spanish, German, Japanese, and Simplified Chinese raster scans
- DOCX through local Mammoth extraction
- XLSX through the bounded SheetJS parser
- PPTX through local OOXML text extraction

Every non-Markdown input first becomes editable Markdown. A second requested output is generated from that intermediate.

PDF extraction preserves readable content rather than the original page layout. OCR is limited to 20 image-only pages per file and may need proofreading. It does not promise handwriting, exact tables, equations, multi-column reading order, or arbitrary vector-only pages. Never upload a user's PDF to a service as a hidden fallback.

## Supported outputs

- Markdown, formatted Markdown, HTML, TXT, CSV, and Markdown token JSON
- Searchable and selectable A4 PDF with embedded CJK-capable fonts
- DOCX, XLSX, PPTX, and EPUB
- LaTeX, AsciiDoc, RTF, reStructuredText, legacy Confluence Wiki Markup, and Notion-oriented Markdown
- Reveal HTML slides, WeChat HTML, and mind-map JSON
- PNG, JPG, and a designed 1280×960 Card image

The PDF writer creates real text objects; it does not turn each page into a screenshot. Search, selection, and copying therefore work for supported characters. Remote Markdown images become readable alt-text placeholders and links are represented as text/link annotations where the writer supports them. Emoji coverage remains font-dependent.

PNG/JPG use a bundled renderer and reject documents taller than 16,000 px instead of silently cutting them off. Card is a designed summary and visibly shortens long bodies; it is not a full-document screenshot.

## Verify the result

Run the bundled verifier on every generated artifact:

```bash
python3 "$MARKDOWN_CONVERTER_DIR/scripts/verify_output.py" /absolute/path/report.md --format markdown
python3 "$MARKDOWN_CONVERTER_DIR/scripts/verify_output.py" /absolute/path/notes.pdf --format pdf
python3 "$MARKDOWN_CONVERTER_DIR/scripts/verify_output.py" /absolute/path/report.docx --format docx
python3 "$MARKDOWN_CONVERTER_DIR/scripts/verify_output.py" /absolute/path/notes.png --format png
```

Treat a failed verifier as a failed conversion. For a PDF output, also confirm that representative text can be extracted, not merely that `%PDF` and page objects exist. For OCR input, compare names, numbers, headings, and at least one paragraph with the visible scan. For other outputs, compare representative headings, paragraphs, lists, tables, links, code, and non-ASCII text with the source.

## Safety and truth rules

- Preserve the input file and use a different explicit output path.
- Refuse an existing destination unless the user authorized `--force`.
- Do not install dependencies: the committed runtime, OCR worker, models, fonts, and renderer are bundled.
- Do not send source text, filenames, or output content to a network service.
- Do not add logos, watermarks, attribution footers, product names, or promotional links to generated artifacts.
- Do not claim pixel-perfect parity. State losses involving layout, fonts, embedded media, formulas, comments, tracked changes, macros, presenter notes, vendor syntax, or OCR uncertainty.
- Treat Confluence output as legacy Wiki Markup, not universal modern Cloud paste.
- Treat Markdown preview behavior as CommonMark/GFM-oriented, not proprietary renderer emulation.

## Completion checklist

- Input and destination paths are explicit and different.
- Source remains recoverable.
- CLI exits successfully and reports `"local": true` and `"network": false`.
- Output is non-empty and passes `verify_output.py`.
- Searchable PDF output has a non-empty extractable text layer.
- OCR-derived Markdown has been spot-checked against the scan.
- Representative semantic content survives within the documented boundary.
- Losses and approximations are stated plainly.
- Final response links to the local output artifact.
