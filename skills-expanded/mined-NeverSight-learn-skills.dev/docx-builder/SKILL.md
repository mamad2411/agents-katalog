---
name: docx-builder
description: Use this skill to create professional, fully-editable Word (.docx) documents — reports, letters, contracts, memos, manuals. Design the document as flowing HTML/CSS (preview it as an Artifact to iterate visually with the user), then run the included Playwright + python-docx pipeline to convert the HTML into native, editable Word content (real headings, paragraphs with per-run formatting, lists, tables, images) — not a screenshot dump. Trigger on "make a Word document", "build a docx", "write a report", "draft a letter/contract", "create documentation".
---

# DOCX Builder

Two-stage workflow: **design in HTML** (fast to iterate, easy to preview),
then **compile to native DOCX** (fully editable in Word — real headings,
paragraphs, lists, tables, not an image).

**This is a flowing document, not a slide/canvas.** Unlike the sibling
`pptx-builder`/`pdf-builder` skills (absolute pixel positions on a fixed
canvas), a Word document's content reflows — so this pipeline reads
**document order and computed style**, not pixel coordinates. Write the
HTML as a normal top-to-bottom page, no `position:absolute`. If what's
actually wanted is a pixel-exact one-pager/flyer, use `pdf-builder`
instead — that's a different authoring model, not just a different file
extension.

## Stage 0 — Pick a style (fonts + accent color)

Before writing any HTML, settle on a visual identity so headings, body
text and tables stay consistent throughout instead of improvising fonts
and colors section by section.

1. Publish `templates/style-gallery.html` as an **Artifact**. It shows 8
   named presets (A–H), each pairing a heading/body font choice with one
   accent color and a rule/table-header treatment. Ask the user to pick a
   letter, or to describe a tweak (e.g. "F but in blue").
2. **If the user already has a brand or template to match** — an existing
   `.docx`, a brand guideline, or explicit fonts/colors — skip the gallery
   and use that instead.
3. Whichever path was used, write down the resolved heading font, body
   font, accent color, and heading color before starting Stage 1 —
   `reference/style-presets.md` has the exact values for each lettered
   preset. Reuse those exact values in a shared `:root { --... }` CSS
   block across the document.

If the user explicitly says they don't care and to just use sensible
defaults, skip straight to Stage 1 with preset A (Corporate Report).

## Stage 1 — Design the document in HTML

Write one HTML file as a normal flowing page — no fixed-size `.page`
canvas, no `position:absolute`. **Every element that should become a
distinct Word block must carry a `data-docx="..."` attribute** — headings,
paragraphs, lists, tables, images, quotes, page breaks. Elements without
it are pure layout/typography scaffolding and are ignored by the
extractor.

Read `reference/conventions.md` before writing HTML — it documents the
full `data-docx` contract (block types, inline run formatting, page setup,
header/footer, list nesting) and what's not supported. Copy
`templates/document-template.html` as a starting point; it demonstrates
page setup, header/footer, heading levels, a paragraph with mixed
bold/italic/colored runs, nested bullet and numbered lists, a quote, a
page break, a table, and an inline icon.

Use small inline icons (16–24px) in contact/detail rows and short feature
lists — see `reference/icons.md` — but keep them sparse; this is body
text, not a slide.

Publish the HTML as an **Artifact** and iterate with the user until the
design is approved — do not run the conversion pipeline on unapproved
designs.

## Stage 2 — Compile to native .docx

Once the HTML is approved, from this skill's directory run:

```bash
python scripts/extract_docx.py <document.html> <work>/document.json <work>/images
python scripts/build_docx.py <work>/document.json <output>.docx
```

- `extract_docx.py` opens the HTML in headless Chromium, walks the body
  **in document order**, and records each tagged block's type, computed
  style, and per-run text formatting (plus list nesting depth and table
  cell data). It only measures a pixel box for `image`/`icon` elements
  (to size the picture) — everything else is style, not geometry.
- `build_docx.py` reads that JSON and creates a real `python-docx`
  document: page size/margins, running header/footer, Heading 1–3
  paragraphs with explicit run formatting layered over the named style,
  bullet/numbered lists (up to 3 nesting levels), native tables with cell
  shading, inline and standalone pictures, and page breaks.

Both scripts print warnings (not silent failures) for anything they had
to skip — read stderr after each run and fix the HTML rather than
ignoring warnings.

## Stage 3 — Verify (never skip this)

A `.docx` can be silently broken in two ways that nothing in Stage 2 will
warn you about — the same two classes of bug that have shown up for real
in the sibling `pptx-builder` pipeline, which shares the same OOXML family
of formats:

1. **Structural corruption** — invalid-per-schema XML (e.g. a duplicated
   element the schema only allows once) that Word silently "repairs" by
   dropping the offending content, with zero error anywhere in the Python
   pipeline.
2. **Overflowing/misapplied content** — the file opens perfectly and looks
   structurally valid, but a table is crushed too narrow, a heading style
   didn't apply, or text that should have wrapped got clipped instead.

Run both checks after every `build_docx.py`, before telling the user the
document is ready:

```bash
python scripts/verify_docx.py <output>.docx
python scripts/render_preview.py <output>.docx <work>/preview
```

`verify_docx.py` catches case 1 (zip/XML integrity, duplicate
schema-singleton elements, illegal characters, dangling image
relationships, a python-docx open check) and exits non-zero with a
specific list if anything is wrong.

`render_preview.py` catches case 2 — it converts the docx to PDF via
LibreOffice and rasterizes every page to PNG. **Actually open each PNG
with the Read tool and look at it** — comparing against the approved HTML
design — before reporting success. Requires LibreOffice (`winget install
TheDocumentFoundation.LibreOffice`) and `pip install pymupdf`.

Do not report a document as done on the strength of "the scripts ran
without warnings" alone. Only `verify_docx.py` passing *and* an actual
look at every rendered page count as done.

## Known limits (design around these, don't fight them)

- Not an absolute canvas — no pixel-exact placement of anything other
  than image/icon size. For that, use `pdf-builder` instead.
- Rich per-run formatting inside a table cell isn't supported — one style
  per cell (same limit as the sibling pptx pipeline).
- Numbered/bulleted lists support up to 3 nesting levels; deeper nesting
  falls back to a plain indented paragraph with a literal bullet
  character (no true auto-numbering).
- No generated table of contents, running section numbers, or multi-column
  header/footer layout — ask the user to add a TOC in Word itself (it
  needs Word's own field-update mechanism) once the file is open.
- Fonts are **not** embedded — Word substitutes at *open* time on whatever
  machine views the file if the exact font isn't installed there (the
  opposite constraint from `pdf-builder`, which embeds at generation
  time). Stick to common fonts (Calibri, Arial, Georgia, Times New Roman)
  unless the target machine is confirmed to have anything else.
- Stacking/reading order follows DOM order — write the HTML top-to-bottom
  in the order content should actually appear in the document.
- `data-docx="icon"` elements are rasterized (screenshot), so they're
  pictures, not editable shapes — use this only for actual small
  icons/logos, never as a shortcut for text or a table border.
