# office/pdf-toolkit — skill payload

> Machine-readable contract: [`../pdf-toolkit.manifest.json`](../pdf-toolkit.manifest.json).
> This file is the narrative a host LLM reads before deciding to invoke the skill.

## What this skill does

Wraps the standard Python PDF stack (`pdfplumber` for text/tables, `pypdf` for
structure and split/merge, `reportlab` for new-document generation) behind a
single `operation` parameter, so an agent can manipulate PDFs without learning
three libraries.

Supported operations:

- `extract_text` — full text, optionally per-page.
- `extract_tables` — structured rows, one list per detected table.
- `fill_form` — fill an AcroForm with a `{field: value}` map and flatten.
- `split` — produce N output PDFs by page range.
- `merge` — concatenate multiple PDFs.

## When to use it

- You need data *out of* a PDF in machine-readable form.
- You need to fill a standard form (tax form, expense claim) at scale.
- You're stitching PDFs together for an audit pack.

## When **not** to use it

- The document is an invoice and you want structured invoice fields — call
  `finance/invoice-extract` instead; it composes this skill internally and
  also does field-mapping.
- You need OCR on a scanned image-only PDF — this skill can extract text
  layers but does not run OCR.
- The output target is editable Word — author with `office/docx-toolkit`
  and export to PDF separately.

## Determinism and risk

Determinism: **high** — same input, same output. Risk: **low** — pure
in-memory file manipulation, no external side effects.

## How it composes

Acts as a building block: `pdf.extract` ← `finance/invoice-extract`,
`pdf.write` ← `office/docx-toolkit` (export path), and any audit-pack
workflow that needs to concatenate evidence PDFs.
