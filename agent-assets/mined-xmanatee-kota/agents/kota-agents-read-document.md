# Read Document Module

This directory owns the `read_document` capability pack — extracts plain text from document files using available system tools.

- Supports PDF, DOCX, RTF, ODT, EPUB, and HTML formats.
- Uses system tools (`pdftotext`, `textutil`, `pandoc`) — no npm dependencies.
- Classified as `safe` / `discovery` kind in guardrails.
- The format-to-extractor map owns provider selection. The tool validates the
  public request and maps extraction failures; extractors only adapt system
  command output.

## Boundaries

- Does not own general file read (that belongs in `filesystem/`).
- Does not own web page fetching or HTML scraping (that belongs in `web-access/`).
- Falls back gracefully when a required system tool is not installed; does not install system dependencies itself.
- Tests cover request validation, provider selection, and distinct command
  failures without copying the provider matrix or mutating host platform
  state.
