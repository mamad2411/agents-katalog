---
name: asciidoc
description: Use when a task involves AsciiDoc syntax, document attributes, includes, conditionals, Asciidoctor publishing workflows, or HTML, PDF, and DocBook export from AsciiDoc sources.
---

# AsciiDoc and Asciidoctor Publishing

## Intent Router

Load sections based on the task:
- Attributes, includes, or conditionals -> `references/attributes-and-includes.md`
- Backend and PDF export choices -> `references/backends-and-pdf.md`
- Safe-mode behavior or failures -> `references/safe-mode-and-troubleshooting.md`

## Overview

This skill covers AsciiDoc authoring and Asciidoctor publishing.
Use it for source semantics, attributes, reusable partials, conditionals, and delivery through HTML, PDF, or DocBook backends.

The guidance follows the AsciiDoc language documentation and Asciidoctor documentation.

## Quick Start

Before promising an export, verify that the relevant Asciidoctor executable is available:

```bash
asciidoctor --version
# for PDF output, also verify the PDF backend
asciidoctor-pdf --version
# or set explicit overrides when the binaries live outside PATH
export ASCIIDOCTOR_PATH=/absolute/path/to/asciidoctor
export ASCIIDOCTOR_PDF_PATH=/absolute/path/to/asciidoctor-pdf
python asciidoc/scripts/build.py guide.adoc --to html --output guide.html
```

```bash
python asciidoc/scripts/build.py handbook.adoc --to pdf --output handbook.pdf --attribute toc=left
```

If the executable is missing, stop and surface the install guidance from `asciidoc/scripts/build.py` before continuing.

## Preferred Workflow

1. Model document structure and metadata with attributes first.
2. Keep includes predictable and relative to a stable project layout.
3. Preview in HTML before assuming PDF theming is correct.
4. Keep safe mode explicit when includes or external assets matter.
5. Narrow backend-specific failures to a minimal source file before changing theme or attribute layers.

## Authoring Guidance

This skill is the right fit for:
- book-style technical docs
- procedural docs with admonitions and callouts
- attribute-driven document variants
- partial-based publishing structures
- Asciidoctor backend export flows

## Export and Backends

Use `asciidoctor` for HTML and DocBook.
Use `asciidoctor-pdf` for PDF.

```bash
asciidoctor guide.adoc
asciidoctor-pdf guide.adoc
```

## Troubleshooting

Typical issues include attribute scope mistakes, include path problems, backend-specific rendering differences, and safe-mode restrictions.
Make the backend and safe mode explicit before debugging document content.

## Official References

Primary sources:
- AsciiDoc language docs: <https://docs.asciidoctor.org/asciidoc/latest/>
- Asciidoctor docs: <https://docs.asciidoctor.org/>

Deep-dive references for this skill:
- `references/attributes-and-includes.md`
- `references/backends-and-pdf.md`
- `references/safe-mode-and-troubleshooting.md`
