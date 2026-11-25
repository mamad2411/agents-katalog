---
name: pdf-processing-pro
description: Production-ready PDF processing with forms, tables, OCR, validation, and batch operations. Use when working with complex PDF workflows in production environments, processing large volumes of PDFs, or requiring robust error handling and validation.
---

# PDF Processing Pro

Production-ready PDF processing guidance with comprehensive error handling and support for complex workflows (forms, tables, OCR, batch operations).

## Core patterns (tool-agnostic)

- **Text extraction**: Use robust libraries (e.g., pdfplumber) and validate output per page.
- **Form workflows**: Detect fields, validate data against schemas, then fill; revalidate outputs.
- **Table extraction**: Combine multiple extractors and normalize columns; handle merged cells explicitly.
- **OCR for scanned PDFs**: Preprocess pages (deskew/denoise) before OCR; store page-level confidence and flag low-confidence regions.
- **Batch operations**: Process PDFs page-by-page to control memory; log per-file successes/failures with timestamps and error details.

## Reliability practices

- Wrap PDF operations in try/except; include filename, operation, and stack trace in logs.
- Validate inputs (paths, expected fields, schemas) before processing.
- Use structured logging with timestamps, operation, result, duration.
- Never log sensitive PDF contents; sanitize before sending to external services.
- For large jobs, checkpoint outputs (per-file artifacts) so you can resume after failures.

## Troubleshooting tips

- **File not found/invalid**: Confirm path/permissions; verify file is not encrypted/corrupted.
- **OCR quality issues**: Increase DPI during rasterization, deskew, and denoise before OCR.
- **Table extraction errors**: Try alternate parsers/settings; manually define column boundaries when automated detection fails.
- **Memory issues**: Stream pages instead of loading whole documents; free resources after each file.
