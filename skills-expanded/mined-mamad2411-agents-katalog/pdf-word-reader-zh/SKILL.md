---
name: pdf-word-reader-zh
description: End-to-end document understanding for `.pdf`, `.docx`, and `.pptx` (auto convert to PDF). Use when users ask to read, summarize, extract, analyze, compare, audit, or fully understand document content with evidence-based chunk citations.
---

# PDF Word Reader ZH

## Purpose

Turn a document path into three analysis artifacts:

- structured extraction
- chunked evidence index
- understanding report scaffold

Use this skill when output quality requires traceable evidence, not only a short summary.

## Input Support

- `.pdf`
- `.docx`
- `.pptx` (convert to PDF first)

For `.doc`, convert to `.docx` before using this skill.

## One-Command Execution

```bash
python scripts/prepare_document_context.py "<input-file>" --output-dir "output/document-understanding"
```

## Decision Flow

1. Detect input type by extension.
2. If `.pptx`, convert to PDF:
- Prefer `soffice` when available.
- Fallback to Microsoft PowerPoint COM on Windows.
3. Extract content:
- PDF: page text + table extraction; use OCR fallback for low-text pages.
- DOCX: paragraphs + table extraction.
4. Normalize and chunk long text into stable chunk IDs (`C001`, `C002`, ...).
5. Generate understanding scaffold with evidence index.

## Output Contract

Write the following files to output directory:

- `01_extracted.json`
- `02_chunks.json`
- `03_understanding_report.md`

### `01_extracted.json`

Must include:

- `source_file`
- `file_type`
- `full_text`
- structure fields (`pages` or `paragraphs/tables`)
- warnings and runtime metadata when available

### `02_chunks.json`

Must include:

- `chunk_count`
- `chunks[]` with fields:
- `chunk_id`
- `char_count`
- `estimated_tokens`
- `text`

### `03_understanding_report.md`

Must include:

- document profile
- key lines
- chunk evidence index
- deliverable template for final analysis

## Recommended Parameters

- `--disable-ocr`: disable OCR fallback
- `--max-pages N`: quick verification on first N pages
- `--fail-on-empty`: stop when no text extracted

## Error Handling Rules

If conversion/extraction fails:

1. Return a concrete cause (missing dependency, unsupported format, conversion error).
2. Provide exact next action (install command or format conversion step).
3. Do not fabricate extracted content.

If extracted text is low quality:

1. Keep warnings in output metadata.
2. Continue chunking with available text.
3. Explicitly mark uncertainty in report.

## Dependency Baseline

Install Python deps:

```bash
python -m pip install -r requirements.txt
```

Recommended system tools:

- `tesseract` + `chi_sim`
- `pdftoppm` (Poppler)
- `soffice` (LibreOffice), or Microsoft PowerPoint (Windows)

## Final Analysis Rules

When producing final conclusions from output artifacts:

1. Read all chunks before writing conclusions.
2. Cite chunk IDs for key claims, e.g. `[C003][C011]`.
3. Separate facts from assumptions.
4. List missing evidence and unresolved questions.
5. Keep numeric claims exactly aligned with extracted text.

## Minimal Working Examples

PDF:

```bash
python scripts/prepare_document_context.py "./report.pdf" --output-dir "./out"
```

DOCX:

```bash
python scripts/prepare_document_context.py "./report.docx" --output-dir "./out"
```

PPTX:

```bash
python scripts/prepare_document_context.py "./slides.pptx" --output-dir "./out"
```