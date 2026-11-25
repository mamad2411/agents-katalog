---
name: strike-valley-docx
description: Convert Markdown into branded Strike Valley Studio DOCX documents that remain editable in Pages or Word. Use for reports, proposals, memos, and assessments that need studio branding and Pages-compatible layout.
---

# Strike Valley DOCX

Produce an editable document that preserves the source's structure and follows
the studio's visual specification. Keep Markdown as the source of truth and
put recurring layout fixes in the renderer so future documents benefit.

## Render the document

Use [scripts/render_branded_docx.py](scripts/render_branded_docx.py) for normal
Markdown conversion. Infer metadata from the source; ask only about ambiguity
that affects the document. Relevant fields are title, recipient, author, date,
and TOC placement. For consultancy reports, default to a TOC after the first
section and omit author and version number unless the user requests them.

Run from the skill directory or resolve its script path explicitly. Use `uv`
for dependencies:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run --with python-docx --with Pillow python scripts/render_branded_docx.py INPUT.md \
  -o OUTPUT.docx \
  --title "Document Title" \
  --prepared-for "Name, Role" \
  --date "26 Mar 2026" \
  --toc after-first-section
```

Only input and output paths are required. The renderer exports a sibling PDF
through Pages by default; this requires available, permitted Pages automation.
Use `--no-pdf` to skip that export.

## Judge the result

Read [Visual specification](references/visual-invariants.md) to assess branding
and [Quality bar](references/quality-bar.md) to choose representative checks.
When appearance matters, inspect the cover, TOC, and a later body page in Pages.
Check any structures the document relies on, such as nested lists and tables.
Judge alignment by how the page reads at a glance.

Fix content, source ordering, and per-document metadata in the Markdown or
render inputs. Fix recurring list, style, header/footer, and import defects in
the renderer. A one-off editorial adjustment can stay local; repeated manual
repair signals a renderer problem.

Before changing header/footer mechanics, read
[Pages compatibility](references/pages-compatibility.md). Its known limitations
matter even when the generated DOCX looks structurally correct. For renderer
work, consult [Pipeline architecture](references/pipeline-architecture.md).
