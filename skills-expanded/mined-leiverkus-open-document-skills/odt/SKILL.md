---
name: odt
description: "Create, read, edit, convert, repair, or inspect OpenDocument Text files (.odt) — including bidirectional conversion to DOCX/DOC via headless LibreOffice and a template ecosystem (grant proposal, academic paper, letterhead, CV, dissertation). Includes scholarly authoring: footnotes, endnotes, citations (BibTeX/CSL-JSON), cross-references (bookmarks, reference-marks, figure/table sequences), MathML formulas (from LaTeX), and generated indexes (table of contents, bibliography, illustration/table index, alphabetical index)."
triggers: [".odt", "ODT", "OpenDocument Text", "Open Office document", "LibreOffice Writer", "Writer document", "odt-Datei", "OpenDocument-Text", "footnote", "endnote", "citation", "bibliography", "BibTeX", "CSL-JSON", "Fußnote", "Zitation", "Bibliographie", "Quellenangabe", "cross-reference", "Querverweis", "bookmark", "Lesezeichen", "figure", "Abbildung", "Table", "Tabelle", "equation", "Gleichung", "Formel", "MathML", "LaTeX", "flat ODF", ".fodt", "table of contents", "Inhaltsverzeichnis", "TOC", "Literaturverzeichnis", "index", "Index", "Abbildungsverzeichnis", "Tabellenverzeichnis", "alphabetical index", "alphabetisches Register", ".docx", "DOCX", ".doc", "Word document", "Word-Dokument", "MS Word", "Microsoft Word", "template", "Vorlage", "Dokumentvorlage", "grant proposal", "Drittmittelantrag", "Forschungsantrag", "ERC", "Antrag", "academic paper", "letterhead", "Briefkopf", "Geschäftsbrief", "CV", "Lebenslauf", "dissertation", "Dissertation", "Habilitation", ".ott"]
dont_use_for: ["spreadsheets (.ods)", "presentations (.odp)", "PDFs as primary deliverable", "general prose editing"]
license: MIT
version: "1.15.0"
---

# ODT creation, editing, and analysis

## Overview

An `.odt` file is an OpenDocument ZIP package. Important package files:

- `mimetype` - should be the first ZIP entry and stored uncompressed as `application/vnd.oasis.opendocument.text`
- `content.xml` - document body
- `styles.xml` - named styles and page layout
- `meta.xml` - document metadata
- `settings.xml` - application settings
- `META-INF/manifest.xml` - package manifest

## Quick Reference

| Task | Preferred approach |
|------|--------------------|
| Extract text and structure | Use `scripts/extract_text.py` or parse `content.xml` |
| Create styled/template document | Start from an `.odt` template, preserve styles/page layout, edit XML |
| Create simple structured document | Generate ODT package XML directly |
| Convert Markdown/HTML/DOCX to ODT | Use Pandoc/LibreOffice only when the source already exists or interoperability requires it |
| Preserve complex formatting | Unpack the ODT, edit XML with a structured XML parser, then repack carefully |
| Inspect raw structure | `unzip -l file.odt`; `python -m zipfile -e file.odt unpacked/` |

## Tool Checks

Before starting a real ODT task, check which tools are available:

```bash
which pandoc
python3 -c "import odf; print('odfpy available')"
```

Resolve the LibreOffice command as described in [docs/soffice-resolver.md](../../docs/soffice-resolver.md).

## Reading Content

For plain text and semantic structure:

```bash
pandoc input.odt -t markdown -o output.md
```

For raw package inspection:

```bash
python -m zipfile -e input.odt unpacked_odt
```

Read `content.xml` with an XML parser. Do not use regex for XML edits.

Bundled scripts for common inspection tasks:

```bash
# Extract headings, paragraphs, lists, tables, and footnotes.
python scripts/extract_text.py input.odt
python scripts/extract_text.py input.odt --json

# Inspect package files, media references, styles, tables, and document structure.
python scripts/inspect_package.py input.odt
```

For the full script reference, see [docs/script-reference.md](../../docs/script-reference.md#odt).

## content.xml Structure

An ODT document normally stores body content in `content.xml` under:

```text
office:document-content
  office:body
    office:text
```

Important body elements:

- `text:h` - real headings; `text:outline-level` controls hierarchy
- `text:p` - paragraphs, including styled body text
- `text:list`, `text:list-item` - real lists
- `table:table`, `table:table-row`, `table:table-cell` - tables
- `text:section` - named document sections
- `text:note` - footnotes/endnotes with citation and body content
- `draw:frame` + `draw:image` - embedded or linked images
- `text:bookmark`, `text:reference-mark`, `text:table-of-content` - references and generated structures when present

Styles are name-based. Common references include:

- `text:style-name` for paragraphs/headings/lists
- `draw:style-name` for image frames or shapes
- `table:style-name` and `table:default-cell-style-name` for tables
- `style:name` in `styles.xml` and automatic styles in `content.xml`

Headers, footers, page styles, and page layout are usually in `styles.xml`, not the main body. When changing page size, margins, headers, footers, or numbering, inspect `style:master-page`, `style:page-layout`, `style:header`, and `style:footer`.

## Creating ODT Files

ODT is an XML package and can be generated directly. Do not default to DOCX/Markdown as an intermediate when the deliverable is natively ODT.

Choose the creation path by fidelity needs:

| Scenario | Use |
|----------|-----|
| Institutional letter/report with exact styles, header/footer, page layout | Template-first ODT |
| Rich prose — headings, bold/italic, links, lists, tables, footnotes | Markdown authoring (`create_from_markdown.py`) |
| Simple generated memo/report/protocol | Direct ODT XML generation |
| Existing HTML/DOCX source or explicit cross-format conversion | Pandoc/LibreOffice conversion fallback |

### Template-First ODT

Use this when layout, styles, headers, footers, or institutional formatting matter.

1. Extract the template.
2. Inspect `styles.xml` for paragraph, text, table, page, header, and footer styles.
3. Inspect `content.xml` for placeholder paragraphs, sections, tables, and image frames.
4. Replace placeholders with XML-aware edits.
5. Add images under `Pictures/` and update `META-INF/manifest.xml`.
6. Repack and run the full QA loop.

### Direct ODT XML Generation

Use this for simple structured documents. Generate a minimal package with:

- `mimetype`
- `content.xml`
- `styles.xml`
- `meta.xml`
- `settings.xml`
- `META-INF/manifest.xml`
- optional `Pictures/...`

Minimum body structure:

```text
office:body
  office:text
    text:h text:outline-level="1"
    text:p
    text:list
    table:table
```

Keep direct generation deliberately small: headings, paragraphs, lists, simple tables, images, and footnotes. Add advanced fields, tracked changes, indexes, or generated tables of contents only when the task requires them and QA confirms they survive LibreOffice rendering.

### Markdown Authoring

When the deliverable is rich prose, write it as Markdown and convert with
`create_from_markdown.py` — the structure *is* the prose, so there is no
block-level JSON to hand-assemble:

```bash
python scripts/create_from_markdown.py article.md article.odt
python scripts/create_from_markdown.py article.md article.odt --title "Q3 Report"
```

The Markdown parser is standard-library only (no Pandoc dependency). It
covers a pragmatic CommonMark subset plus GFM tables and footnotes:

- headings, paragraphs, **bold**/*italic*/`code`, links (inline + reference)
- bullet and ordered lists, including nesting
- blockquotes, fenced code blocks, thematic breaks
- GFM tables with column alignment
- block and inline images (local files embedded, URLs linked)
- footnotes (`[^id]` + `[^id]:`) → `text:note`

Inline formatting becomes `text:span` runs, so the output is real rich text,
not plain paragraphs. Style names are fixed (`Heading1`–`Heading6`, `Body`,
`Quote`, `CodeBlock`, `Strong`, `Emphasis`, `Code`, …); a branded `styles.xml`
reusing those names can be injected with `inject_styles_from_file`. Not
supported: indented code blocks, setext headings, raw HTML, autolinks, and
task-list checkboxes.

### Conversion Fallback

Use Pandoc or LibreOffice conversion when the source already exists in another format or when interoperability is the task:

```bash
pandoc input.md -o output.odt
```

When a reference template is available, use it to carry page styles, fonts, headers, footers, and bibliography styling:

```bash
pandoc input.md --reference-doc=template.odt -o output.odt
```

Set explicit heading hierarchy in the source. Avoid manually faking headings with bold text.

### Format Conversion (Word: DOCX/DOC)

For one-shot conversion between ODT and Microsoft Word formats, `convert.py`
wraps `soffice --headless --convert-to` with an isolated temp profile:

```bash
# ODT → DOCX:
python scripts/convert.py doc.odt --to docx --outdir qa

# DOCX → ODT (the bridge: edit a Word document with our skills, then export back):
python scripts/convert.py source.docx --to odt --outdir qa
python scripts/replace_text.py qa/source.odt "Old text" "New text" -o edited.odt
python scripts/convert.py edited.odt --to docx --outdir qa

# Legacy MS Word 97-2003 (.doc):
python scripts/convert.py doc.odt --to doc --outdir qa
python scripts/convert.py legacy.doc --to odt --outdir qa
```

**Fidelity caveat**: soffice handles the 80% case (prose, simple tables,
footnotes, basic styles) well. Round-tripping documents with complex master
pages, embedded MathML, advanced bibliography features, or heavy custom
formatting can lose detail. Inspect the output before relying on it.

For spreadsheets, use the **ods** skill's `convert.py` (ODS ↔ XLSX/XLS); for
presentations, the **odp** skill's `convert.py` (ODP ↔ PPTX/PPT). The skill
boundary enforces format families — cross-family conversions (e.g. ODT →
XLSX) are not supported by soffice and the script rejects them with a clear
hint.

## Themes

`create_minimal_odt.py` and `create_from_markdown.py` accept `--theme NAME` — a
curated colour palette and font pairing applied to the generated document.
Five themes:

| Theme | Feel |
|-------|------|
| `corporate-blue` | clean corporate blue |
| `warm-editorial` | cream background, terracotta serif — reports, essays |
| `high-contrast` | black on white, bold — accessibility, print |
| `slate-mono` | slate palette, monospaced headings — technical docs |
| `forest` | deep green, sans heading + serif body |

```bash
python scripts/create_minimal_odt.py spec.json out.odt --theme warm-editorial
python scripts/create_from_markdown.py in.md out.odt --theme forest
```

Without `--theme` the output is unchanged. Themes name fonts as stacks with a
Liberation fallback, so a themed document renders even where the first-choice
font is absent. For full branded designs (not just palette + fonts), use a
**template** (next section).

## Templates

A *template* is a complete branded design (styles + page layout + master
page + outline numbering) packaged as a directory. The skill ships five
templates plus three tools — themes are quick palette+font tweaks;
templates are full document-class designs.

### Shipped templates

`skills/odt/templates/`:

| Template | Use case |
|---|---|
| `grant-proposal` | research-grant proposal for any agency (ERC / VW / Thyssen / EU). A4, 2.5 cm margins, navy Lato headings + Source Serif body, outline-numbered 1./1.1./1.1.1. |
| `academic-paper` | IMRaD article (Title / Abstract / Introduction / Methods / Results / Discussion / References) with hanging-indent References style |
| `letterhead` | DIN-5008-ish business letter — institution placeholder header, asymmetric margins for envelope-window alignment, signature block |
| `cv` | academic CV — navy section headers with bottom rule, compact 2 cm margins, EntryTitle/EntryDetail/DateRange styles |
| `dissertation` | long-form thesis / Habilitation — A4 with 3 cm margins, 5-level outline numbering, chapter-per-page (`Heading1` page-break-before), 1.4 line-height, hanging-indent bibliography |

All templates are English-first and institution-neutral. For German
localisation aimed at a third-party funder, see `examples/dao/`.

### Apply a template

`apply_template.py` wraps inject-styles + embed-pictures + validate-refs
into one call:

```bash
# Build a base document
python scripts/create_minimal_odt.py spec.json doc.odt

# Apply a shipped template by name
python scripts/apply_template.py doc.odt \
    --template-name grant-proposal -o branded.odt

# Or by path (e.g. a user-supplied template directory)
python scripts/apply_template.py doc.odt \
    --template /path/to/my-template -o branded.odt
```

### Inspect a template

Before authoring, ask what the template offers:

```bash
python scripts/inspect_template.py \
    skills/odt/templates/grant-proposal/styles.xml --json
```

Output is JSON with `page_layouts` (margins, header/footer heights),
`master_pages` (header/footer previews, frames), `outline_styles` (heading
numbering levels), named `paragraph_styles` / `text_styles` /
`list_styles`, and `font_face_decls`.

### Extract a new template

To turn an existing `.odt`/`.ott`/`.docx` (DOCX via the v1.11 OOXML bridge)
into a reusable template:

```bash
python scripts/extract_template.py corporate-letterhead.docx \
    --name corporate-letterhead --outdir skills/odt/templates/ \
    --license CC-BY-4.0 --source "https://example.com/template"
```

The extractor filters `office:automatic-styles` to keep only what master
pages reference (plus parent-style chains), copies master-page-referenced
`Pictures/`, and writes `LICENSE.txt`/`PROVENANCE.md`/`README.md` metadata.

### Pairing templates with scholarly authoring

Templates pair naturally with the scholarly stack (v0.3 – v1.10):

```bash
# Apply template, then add the full apparatus
python scripts/apply_template.py doc.odt --template-name dissertation -o branded.odt
python scripts/fill_citations.py branded.odt --source refs.bib -o branded.odt
python scripts/add_toc.py branded.odt --at start --title "Contents" --levels 4 -o branded.odt
python scripts/add_bibliography.py branded.odt --at end --title "Bibliography" -o branded.odt
python scripts/update_indexes.py branded.odt --outdir qa
```

Templates live inside `skills/odt/`, so `install_skills.py` bundles them
into every Smithery / skills.sh / Claude Code plugin install.

## Bundled Scripts

For creation and editing scripts, see [docs/script-reference.md](../../docs/script-reference.md#odt).
All scripts use the Python standard library and are invoked as:

```bash
python scripts/<script_name>.py [args]
```

## ODT Layout Checklist

- Use real `text:h` headings with outline levels; do not fake headings with bold paragraphs.
- Use real `text:list` lists; avoid manually typed bullets when generating XML.
- Use real `table:table` structures; check table widths, cell padding, and page breaks in PDF output.
- Put repeated headers/footers/page numbers in page styles, not copied body paragraphs.
- Preserve template style names unless intentionally changing the design system.
- Anchor images deliberately and leave enough surrounding text space for LibreOffice layout.
- Keep page size and margins explicit for generated documents.
- Verify long words, German compounds, footnotes, and bibliography-like paragraphs in PDF render.

## Editing Existing ODT Files

For content-only edits:

1. Convert to Markdown with Pandoc.
2. Make the content changes.
3. Convert back to ODT, using the original as `--reference-doc` when layout matters.
4. Render or convert to PDF and visually check the result.

For precise edits that must preserve layout:

1. Extract the package.
2. Parse and modify `content.xml` / `styles.xml` with an XML library.
3. Keep namespace prefixes valid.
4. Update `META-INF/manifest.xml` if adding or removing embedded files.
5. Repack with `mimetype` first and uncompressed.

Repack pattern:

```bash
cd unpacked_odt
zip -0 -X ../output.odt mimetype
zip -r -X ../output.odt . -x mimetype
```

## QA (Required)

Assume generated or edited ODT files have problems until proven otherwise. Writer layout can change because of fonts, page styles, table widths, image anchoring, footnotes, and conversion filters.

### Content QA

Extract structure:

```bash
python scripts/extract_text.py output.odt
python scripts/extract_text.py output.odt --json > qa/text.json
```

Check headings, paragraph order, lists, tables, image references, footnotes/endnotes, and leftover placeholders such as `Lorem`, `TODO`, `XXXX`, or template instructions.

### Package QA

Inspect and validate:

```bash
python scripts/inspect_package.py output.odt > qa/package.json
python scripts/validate_refs.py output.odt
```

Check that `mimetype` is first, required XML files exist, media targets exist, manifest entries are present, and style references are not broken.

### Visual Design Loop

Rendering is a **design step, not only a final check**. Render an early draft,
look at it, fix what is wrong, then continue — do not author the whole
document blind and render once at the end.

```bash
python scripts/render.py output.odt --outdir qa                  # PDF
python scripts/render.py output.odt --outdir qa --contact-sheet  # all pages in one image
python scripts/render.py output.odt --outdir qa --png            # one PNG per page
```

The contact sheet composes every page into a single labelled grid image —
the fastest way to judge page breaks and cross-page consistency at a glance.
Open the rendered PDF or contact sheet and actually look at it.

Inspect page breaks, headers/footers, table overflow, footnote placement, missing images, changed fonts, and unexpected style loss. If only Pandoc is available, `pandoc output.odt -t markdown` gives a partial content check.

### Verification Loop

The final pass of a loop you should already be running while authoring:

1. Extract content and package summaries.
2. Render to PDF or a contact sheet and **look at it**.
3. List concrete issues found.
4. Fix the ODT source, package XML, or template edits.
5. Re-run the relevant extraction/inspection/rendering steps.
6. Do not deliver until a final pass shows no unresolved content, package, or visual issues relevant to the user's request.

## Scholarly authoring (footnotes, citations, bibliography)

For scholarly prose with apparatus, the suite provides direct ODF-native helpers — no DOCX or pandoc-citeproc round-trip needed.

### Footnotes and endnotes

```bash
# Insert a footnote after a text anchor:
python scripts/add_footnote.py input.odt --anchor "strittige Behauptung" \
    --body "Quelle: Müller 2020, S. 42" -o output.odt

# Append to the third paragraph:
python scripts/add_footnote.py input.odt --paragraph 3 --position end \
    --body "Lange Anmerkung." --class endnote -o output.odt

# Inspect all notes:
python scripts/list_notes.py output.odt --json
```

IDs auto-increment (`ftn0`, `ftn1`, … / `edn0`, `edn1`, …) unless `--id` is given. Inline children (`text:span`, `text:bookmark`) around the anchor are preserved.

### Citations (BibTeX or CSL-JSON)

```bash
# Insert a single citation, source auto-detected from extension:
python scripts/add_citation.py input.odt --anchor "frühere Studien" \
    --source refs.bib --key Mueller2020 -o output.odt
python scripts/add_citation.py input.odt --anchor "frühere Studien" \
    --source refs.json --key Mueller2020 -o output.odt

# Manually:
python scripts/add_citation.py input.odt --anchor "frühere Studien" \
    --identifier Mueller2020 --field bibliography-type=article \
    --field author="Müller, K." --field year=2020 \
    --field title="Beispieltitel" --field journal="ZAW" -o output.odt

# Bulk-fill pandoc-style placeholders:
python scripts/fill_citations.py template.odt --source refs.bib -o output.odt
# Scans for `[@bibkey]` markers, replaces each with text:bibliography-mark.

# Inspect citations:
python scripts/list_citations.py output.odt --json
```

LibreOffice renders the citation through the bibliography style. The bibliography index at document end is *not* generated here — let LibreOffice build it from the inserted `text:bibliography-mark` elements.

BibTeX support requires the optional `bibtexparser` dependency:

```bash
pip install open-document-skills[scholarly]
```

CSL-JSON works with stdlib only.

### Cross-references and figure numbering

```bash
# Mark a target with a bookmark:
python scripts/add_bookmark.py input.odt --name "Kapitel3" \
    --anchor "3. Methodik" -o output.odt

# Reference the target later:
python scripts/add_reference.py input.odt --ref-to "Kapitel3" --kind bookmark \
    --anchor "siehe Kapitel" --display chapter -o output.odt

# Auto-numbered figure caption:
python scripts/add_sequence.py input.odt --sequence Figure --name "fig:karte" \
    --anchor "Karte zeigt" -o output.odt

# Reference to the figure:
python scripts/add_sequence.py input.odt --ref-to "fig:karte" \
    --anchor "siehe Abbildung" -o output.odt

# Inspect everything (bookmarks, ranges, sequences, refs):
python scripts/list_refs.py output.odt --json
```

`text:bookmark` (point + range), `text:reference-mark` (point + range), and `text:sequence` (Figure/Table/Equation) are supported. Display modes for refs: `page`, `chapter`, `number`, `direction`, `text`. The validator detects dangling references and duplicate names.

### Math formulas (MathML, via LaTeX or raw)

```bash
# LaTeX → MathML (requires pandoc):
python scripts/add_math.py input.odt --latex "E = mc^2" \
    --anchor "Einstein-Gleichung" -o output.odt

# Raw MathML from a file:
python scripts/add_math.py input.odt --mathml formula.mml \
    --anchor "Datierungsformel" -o output.odt

# Inline MathML XML:
python scripts/add_math.py input.odt --paragraph 3 \
    --mathml-inline '<math xmlns="http://www.w3.org/1998/Math/MathML"><mi>x</mi></math>' \
    -o output.odt
```

Formulas are embedded as `Object N/` sub-packages — the LibreOffice-native convention — with proper manifest entries (`application/vnd.oasis.opendocument.formula`). LibreOffice opens, renders, and roundtrips them.

### Generated tables of contents and indexes

The skill ships inserters for the four ODF index types plus a marker script for
the alphabetical index. Each script writes the index *container* (with the
proper `text:<kind>-source` configuration) and an empty `text:index-body`
placeholder. The actual entries are filled by LibreOffice — run
`update_indexes.py` to dispatch the refresh headlessly, or open the document
in LibreOffice GUI and press F9 (Tools → Update → Update All Indexes).

```bash
# Table of contents over a doc's headings (default outline level 3):
python scripts/add_toc.py input.odt --at start --title "Inhalt" -o output.odt

# Bibliography (entries come from text:bibliography-mark — see add_citation.py):
python scripts/add_bibliography.py input.odt --at end --title "Literatur" -o output.odt

# Illustration index / table index — pass --sequence Figure | Table | Equation
# (entries come from text:sequence captions inserted via add_sequence.py):
python scripts/add_illustration_index.py input.odt --at end --sequence Figure -o output.odt

# Alphabetical index — combine the container with point markers:
python scripts/add_alphabetical_index.py input.odt --at end -o with_idx.odt
python scripts/add_index_mark.py with_idx.odt --anchor "Datierung" \
    --key1 "Methoden" --key2 "C14" -o with_marks.odt

# Refresh all index bodies via headless soffice (mirrors recalc.py for Calc):
python scripts/update_indexes.py with_marks.odt --outdir qa
```

`update_indexes.py` writes an isolated `-env:UserInstallation` temp profile
with a one-off `Standard/Module1.RefreshIndexes` Basic library, invokes
soffice on the document + macro URL, then deletes the temp profile. The real
LibreOffice user profile is never touched. On platforms where headless macro
execution is blocked the script prints a clear diagnosis; opening the file
once in LibreOffice GUI and pressing F9 is the manual fallback.

`validate_refs.py` warns when an index container is structurally empty:
TOC with no matching headings, bibliography without `text:bibliography-mark`,
illustration index referencing a `caption-sequence-name` that nothing in the
body uses, or alphabetical index without any `text:alphabetical-index-mark`.

## Tracked Changes and Comments

For document review, record edits as tracked changes a human can accept or
reject, and attach comments — no DOCX round-trip needed.

### Comments

```bash
# Point comment after an anchor:
python scripts/add_comment.py doc.odt --anchor "claim" \
    --author "Reviewer" --text "Source?" -o out.odt

# Range comment spanning a phrase:
python scripts/add_comment.py doc.odt --start-anchor "Solar" \
    --end-anchor "additions" --author "Editor" --text "Verify." -o out.odt

python scripts/list_comments.py out.odt          # JSON
```

A comment is an `office:annotation` (point) or an `office:annotation` /
`office:annotation-end` pair (range), each with `dc:creator`, `dc:date`, and
a `text:p` body.

### Tracked changes

```bash
# Record an insertion, a deletion, or a replacement:
python scripts/track_change.py doc.odt --insert " (draft)" \
    --anchor "Report" --author "Reviewer" -o out.odt
python scripts/track_change.py doc.odt --delete "very " --author "Reviewer" -o out.odt
python scripts/track_change.py doc.odt --replace "old term" \
    --with "new term" --author "Reviewer" -o out.odt

python scripts/list_changes.py out.odt           # JSON

# Accept or reject — all changes or one by id:
python scripts/resolve_changes.py out.odt --accept --all -o final.odt
python scripts/resolve_changes.py out.odt --reject --id ct2 -o final.odt
```

Each change is a `text:changed-region` (`text:insertion` / `text:deletion`,
with `office:change-info`); insertions are wrapped in `text:change-start` /
`text:change-end` markers, deletions leave a `text:change` marker and move
the removed text into the region. LibreOffice shows them as underline /
strike-through with a change bar. Deletions operate on a text run within one
paragraph; insertions work at any anchor.

## Structural Editing

Beyond inline text replacement, four scripts restructure an existing
document — bulk restyle, insert and delete whole blocks, and edit tables.

```bash
# Bulk-restyle: apply a style to matching paragraphs/headings.
python scripts/restyle.py doc.odt --headings --style "DAO-Heading-1" -o out.odt
python scripts/restyle.py doc.odt --current-style "Body" --style "DAO-Body" -o out.odt
python scripts/restyle.py doc.odt --level 2 --style "Sub" -o out.odt

# Insert a block fragment (same JSON `blocks` format as create_minimal_odt):
python scripts/insert_blocks.py doc.odt --blocks frag.json \
    --after-anchor "Introduction" -o out.odt    # or --before-anchor / --at-paragraph N / --at start|end

# Delete a whole block:
python scripts/delete_block.py doc.odt --anchor "Obsolete heading" -o out.odt
python scripts/delete_block.py doc.odt --paragraph 3 --type table -o out.odt

# Edit a table by name:
python scripts/edit_table.py doc.odt --table "Results" --add-row 2024 1500 -o out.odt
python scripts/edit_table.py doc.odt --table "Results" --add-column "Note" -o out.odt
python scripts/edit_table.py doc.odt --table "Results" --set-cell 2 3 "ok" -o out.odt
python scripts/edit_table.py doc.odt --table "Results" --delete-row 5 -o out.odt
```

`restyle.py` changes `text:style-name` on `text:p`/`text:h`; selectors
(`--current-style`, `--headings`/`--paragraphs`, `--level`) combine.
`insert_blocks.py` consumes a JSON `blocks` array (heading/paragraph/list/
table); for images and footnotes use `add_image.py`/`add_footnote.py`.
`edit_table.py` expands `number-columns-repeated`/`number-rows-repeated`
before editing, so it works on LibreOffice-saved tables too.

## ODT Notes

- ODF styles are style-name based. Preserve existing style names when editing templates.
- Embedded images live under package paths such as `Pictures/...`; the manifest must include them.
- OpenDocument comments and tracked changes are not uniformly preserved across tools. When those matter, prefer LibreOffice round-trips and verify manually.
- Avoid creating minimal XML by hand unless the file is simple; ODT consumers are forgiving, but style and manifest mistakes cause subtle rendering problems.

## See also

Part of the [open-document-skills](https://github.com/leiverkus/open-document-skills) suite:

- [`odp`](../odp/SKILL.md) — OpenDocument Presentation / LibreOffice Impress
- [`ods`](../ods/SKILL.md) — OpenDocument Spreadsheet / LibreOffice Calc
- [`odg`](../odg/SKILL.md) — OpenDocument Graphics / LibreOffice Draw
