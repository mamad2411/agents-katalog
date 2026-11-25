---
name: kordoc-parse-document
description: Use when converting Korean document files into readable text with `npx` and kordoc. Covers HWP, HWPX, and PDF parsing to Markdown or JSON, including metadata, outline, warnings, and page count. Trigger for requests such as reading a government document, extracting document contents, summarizing a Korean office file, or parsing a local .hwp/.hwpx/.pdf with `kordoc:parse_document`.
---

# kordoc: parse_document

Use the public CLI first. This skill maps to the `parse_document` intent in `src/mcp.ts`, but without MCP.

## Input Requirements

- Require exactly one target document.
- Require the user to attach the document or provide a concrete local path.
- Accept only supported formats: `.hwp`, `.hwpx`, `.pdf`.
- Do not proceed if the document is missing or the path is ambiguous.

## Default Command

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- \
  kordoc /abs/path/document.hwpx
```

Use JSON when the caller needs blocks or metadata:

```bash
npm exec --yes --package=kordoc --package=pdfjs-dist -- \
  kordoc /abs/path/document.hwpx --format json --silent
```

## Workflow

1. Resolve the target file to an absolute path.
2. Confirm the extension is `.hwp`, `.hwpx`, or `.pdf`.
3. Use plain CLI output for human reading.
4. Use `--format json` when the task needs `metadata`, `outline`, `warnings`, or `blocks`.
5. Summarize the parsed content instead of dumping the whole document unless the user asked for raw output.

## Guardrails

- Install `pdfjs-dist` alongside `kordoc`; the package may fail to load without it.
- Preserve warnings about image-based PDFs, skipped elements, or hidden text filtering.
- Do not claim OCR happened unless the execution path explicitly used an OCR-capable custom script.
- If the file is large, summarize key sections first.
- Refuse to continue when no supported document was provided.
