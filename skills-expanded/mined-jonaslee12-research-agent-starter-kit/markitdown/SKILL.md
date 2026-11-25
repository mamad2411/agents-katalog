---
name: markitdown
description: Use when converting PDFs, Word files, slides, spreadsheets, HTML, or other documents into Markdown for source review, literature ingestion, Obsidian notes, or RAG-ready knowledge-base preparation; check tool availability first and do not install dependencies without confirmation.
---

# MarkItDown

Use this skill when file content should be converted into clean Markdown for review, source notes, Obsidian, or knowledge-base ingestion.

## Purpose

Support document-to-Markdown conversion while preserving source discipline and privacy.

This skill is a wrapper for MarkItDown-style workflows. The MarkItDown CLI/package may not be installed. Always check availability before using it.

## Availability Check

Before using MarkItDown:

```bash
command -v markitdown
python -c "import importlib.util; print(bool(importlib.util.find_spec('markitdown')))"
```

If unavailable:

- do not install it automatically;
- use existing project-safe extraction methods when sufficient;
- ask the user before installing MarkItDown or any dependency.

## Workflow

1. Identify the file type and purpose of conversion.
2. Check whether the file contains sensitive or participant-identifiable data.
3. Decide the output location:
   - `knowledge-base/sources/` for source notes;
   - `research-wiki/` for project memory;
   - Obsidian vault for navigation notes;
   - private folders for sensitive material.
4. Convert to Markdown only when it improves review, citation audit, or knowledge ingestion.
5. Preserve source metadata:
   - original file path;
   - conversion date;
   - conversion method;
   - evidence status.
6. After conversion, run a quality check:
   - headings preserved enough;
   - tables readable enough;
   - no missing obvious sections;
   - citations/page references not invented.

## Privacy Rules

- Do not convert raw participant data into general project folders.
- Do not push converted private university materials to public GitHub templates.
- Do not use converted text as official source evidence if the conversion may have lost formatting or context.
- Label OCR or imperfect extraction as `NEEDS VERIFICATION`.

## Output Contract

```text
Conversion record:
- Source file:
- Output file:
- Method:
- Sensitive data check:
- Evidence boundary:
- Quality check:
- Next use:
```

