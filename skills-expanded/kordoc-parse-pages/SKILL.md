---
name: kordoc-parse-pages
description: Use when parsing only part of a Korean document with `npx` and kordoc. Trigger for requests such as extracting pages 1-3, reading selected pages from HWP, HWPX, or PDF, limiting work on large files, or running `kordoc:parse_pages` with a page-range string.
---

# kordoc: parse_pages

This skill maps directly to the `parse_pages` intent in `src/mcp.ts`. Use the public CLI.

## Input Requirements

- Require exactly one target document.
- Require the user to attach the document or provide a concrete local path.
- Accept only supported formats: `.hwp`, `.hwpx`, `.pdf`.
- Require an explicit page range such as `1-3` or `1,3,5-7`.
- Do not proceed if the document or page range is missing.

## Commands

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- \
  kordoc /abs/path/document.hwpx --pages 1-3
```

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- \
  kordoc /abs/path/document.hwpx --pages 1,3,5-7 --format json --silent
```

## Workflow

1. Resolve the document path to an absolute path.
2. Normalize the requested range such as `1-3` or `1,3,5-7`.
3. Use plain output for reading tasks.
4. Use JSON when the caller needs structured blocks or metadata.
5. Repeat the exact requested range in the answer.

## Guardrails

- PDF page selection is exact.
- HWP and HWPX page slicing is section-based and approximate.
- If the user asks for one page from a non-PDF document, warn about that approximation.
- Refuse to continue when no supported document was provided.
