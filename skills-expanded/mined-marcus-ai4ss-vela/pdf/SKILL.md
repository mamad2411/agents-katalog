---

name: "pdf"

description: "Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction."

---





# PDF Skill



## When to use

- Read or review PDF content where layout and visuals matter.

- Create PDFs programmatically with reliable formatting.

- Validate final rendering before delivery.



For academic citation-evidence marking, use `evidence-based-literature-workflow` first. This PDF skill can help render pages and inspect screenshots, but it must not replace the citation evidence rules for body-text evidence, exact sentence highlighting, source-copy protection, and independent review gates.



For citation-evidence screenshots, verify that each highlight covers the complete evidence sentence or continuous sentence group. A search-hit highlight around only keywords is not a valid academic citation annotation. Clear stale screenshots, manual notes, and annotated PDFs from earlier rounds before final inspection.



## Workflow

1. Prefer visual review: render PDF pages to PNGs and inspect them.

   - Use `pdftoppm` if available.

   - If unavailable, install Poppler or ask the user to review the output locally.

2. Use `reportlab` to generate PDFs when creating new documents.

3. Use `pdfplumber` (or `pypdf`) for text extraction and quick checks; do not rely on it for layout fidelity.

4. After each meaningful update, re-render pages and verify alignment, spacing, and legibility.



## Optional structured extraction backend

Use OpenDataLoader PDF only when an existing PDF needs structured Markdown/JSON extraction for reading, evidence triage, or table/layout inspection.



Local wrapper:

```

powershell -ExecutionPolicy Bypass -File skills/scripts/run-opendataloader-pdf.ps1 INPUT.pdf -o OUTPUT_DIR -f markdown,json --pages 1-3 --quiet

```



Rules:

- It is a parser for already obtained PDFs, not a literature download route.

- Keep outputs inside the active project output directory.

- Do not use its Markdown as final citation evidence unless the original PDF location is checked against the citation-evidence rules.

- For scanned pages without text, the base parser may return images only; do not enable hybrid/OCR backends unless the task explicitly allows heavier model dependencies and a separate smoke test passes.

- The MCP server variant is not enabled by default. It needs a separate permission review because it exposes local PDF path access to an agent tool.



## Temp and output conventions

- Use `tmp/pdfs/` for intermediate files; delete when done.

- Write final artifacts under `output/pdf/` when working in this repo.

- Keep filenames stable and descriptive.



## Dependencies (install if missing)

Prefer `uv` for dependency management.



Python packages:

```

uv pip install reportlab pdfplumber pypdf opendataloader-pdf==2.4.6

```

If `uv` is unavailable:

```

python3 -m pip install reportlab pdfplumber pypdf opendataloader-pdf==2.4.6

```

System tools (for rendering):

```

# macOS (Homebrew)

brew install poppler



# Ubuntu/Debian

sudo apt-get install -y poppler-utils

```



If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.



## Environment

No required environment variables.



## Rendering command

```

pdftoppm -png $INPUT_PDF $OUTPUT_PREFIX

```



## Quality expectations

- Maintain polished visual design: consistent typography, spacing, margins, and section hierarchy.

- Avoid rendering issues: clipped text, overlapping elements, broken tables, black squares, or unreadable glyphs.

- Charts, tables, and images must be sharp, aligned, and clearly labeled.

- Use ASCII hyphens only. Avoid U+2011 (non-breaking hyphen) and other Unicode dashes.

- Citations and references must be human-readable; never leave tool tokens or placeholder strings.



## Final checks

- Do not deliver until the latest PNG inspection shows zero visual or formatting defects.

- Confirm headers/footers, page numbering, and section transitions look polished.

- Keep intermediate files organized or remove them after final approval.
