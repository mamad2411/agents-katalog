---
name: pdf-production
description: Produces and verifies professional PDFs: selects the generation engine from the document rather than by habit, builds cover, contents, pagination, headers, footers and metadata, then inspects the rendered pages for clipping, overflow, orphans, broken tables, missing glyphs and wrong page numbers. A generated PDF is not a finished PDF until it has been looked at.
license: MIT
metadata:
  category: publishing
  version: 1.0.0
  depends_on: [document-core, document-design]
  outputs: [pdf, render-verification-report, generation-recipe]
---

# PDF Production

A PDF is the only deliverable format whose defects are invisible in the
source. Text that fits in Markdown clips in a PDF. A table that renders on
screen breaks across a page. A font that displays correctly in the editor
drops accented capitals in the output.

Therefore the rule that governs this skill: **a generated PDF is not a
finished PDF until the rendered pages have been inspected.** Not the source.
The pages.

Governed by `document-core` for content and `document-design` for layout.
This skill owns the engine, the pipeline and the verification.

## 1. Engine selection

There is no correct default. Choose from the document.

| Engine | Strong at | Weak at | Choose when |
|---|---|---|---|
| Headless Chromium | HTML and CSS fidelity, web fonts, complex layout, SVG, charts | large documents, memory, reproducibility across versions | the document is already HTML, or the layout is complex |
| WeasyPrint | CSS Paged Media, running headers, page counters, reproducibility | very recent CSS, JavaScript | a paginated document from HTML, deterministic output wanted |
| Typst | typography, tables, references, fast compilation, readable source | ecosystem maturity, unusual layouts | a structured technical or report document, produced repeatedly |
| LaTeX | mathematics, long-document typography, bibliographies | learning cost, toolchain size, debugging | mathematics, or a house template already exists |
| Markdown via a converter | speed, simple documents | pagination control, precise layout | a short internal document where layout is not a requirement |
| A library building the PDF directly | exact placement, forms, filling an existing template | everything else, including changing the design later | filling a fixed form, or stamping an existing PDF |

Decision procedure:

1. Is the source already HTML, or does it need CSS layout? Chromium or
   WeasyPrint.
2. Does it need running headers, page counters or precise pagination?
   WeasyPrint or Typst, not a Markdown converter.
3. Is it mathematics? LaTeX.
4. Is it produced repeatedly and reviewed in version control? Prefer a text
   source: Typst, LaTeX or HTML, not a binary or a manual process.
5. Is it a fixed official form? A library, filling fields.

Constraints that override preference:

- **Verify the engine exists before promising a PDF.** Check the command runs.
  A pipeline that assumes an engine is a pipeline that fails on someone else's
  machine.
- Prefer what the project already uses. A second engine is a second set of
  fonts, a second CSS dialect and a second class of bug.
- Prefer an engine installable without a browser or a full distribution when
  the document is simple. Do not install 300MB to produce a two-page letter.
- Record the engine and its version in the recipe. The same source with a
  different version does not produce the same pages.

## 2. Structure

| Element | Rule |
|---|---|
| Cover | title, subtitle, version, date, author or organisation, recipient; no header or footer, not counted in the numbering the reader sees |
| Metadata | title, author, subject, keywords, language; set in the document, not left to the exporter |
| Table of contents | generated from the headings, never typed; page numbers regenerated after the final edit |
| Sections | starting on a new page for formal deliverables, and on an odd page for double-sided printing |
| Page breaks | controlled: never immediately after a heading, never separating a caption from its object |
| Headers | document title and current section; suppressed on the cover |
| Footers | page number, version, date |
| Page numbers | `n of N` where the document may be printed and separated |
| Annexes | numbered separately, listed in the contents |

Typography and layout are decided by `document-design` and applied here. This
skill does not re-decide them.

## 3. Font embedding

The most common silent PDF defect.

- Every font is embedded. A PDF referencing a font the reader lacks is
  substituted, and the substitution changes the pagination.
- Every font contains every glyph of the output language. Verify by rendering
  a sample containing the accented characters, capitals included, the currency
  symbols and any special punctuation, then looking at it.
- A missing glyph renders as a box, a blank or a substituted character. All
  three are invisible in the source and obvious in the render.
- Where the document mixes scripts, verify each script separately.

```bash
pdffonts document.pdf
```

Every row must show an embedded font. Any row showing a non-embedded font is a
defect, not a warning.

## 4. Verification

Mandatory. Automated checks first, then the eyes, because the eyes catch what
no check describes.

### Automated

```bash
pdfinfo document.pdf                    # pages, size, title, author, language
pdffonts document.pdf                   # every font embedded
pdftotext document.pdf - | head -50     # text extractable, reading order sane
qpdf --check document.pdf               # structural integrity
```

Checks:

- [ ] Page count matches expectation. An unexpected extra page is a defect.
- [ ] Metadata present and correct: title is the title, not the filename.
- [ ] Language set, so screen readers pronounce correctly.
- [ ] Every font embedded.
- [ ] Text extractable. Nothing that should be text is an image.
- [ ] Extraction order matches reading order.
- [ ] File size proportionate. A 40MB text document means unoptimised images.
- [ ] Structure valid.

### Visual

Automated checks pass on documents that are visibly broken. Render the pages
and look at them.

```bash
pdftoppm -png -r 110 document.pdf page   # one image per page
```

Then inspect every page, or every page of a long document's first twenty plus
a systematic sample plus every page containing a table or a figure.

| Defect | What it looks like |
|---|---|
| Clipped text | a line cut at the margin, or a descender shaved |
| Overflow | text past the margin, or into the header or footer |
| Orphan heading | a heading alone at the foot of a page |
| Widow line | one line of a paragraph alone at the top of a page |
| Broken table | header on one page, rows on the next with no header |
| Empty page | an unintended blank, usually from a forced break |
| Missing glyph | a box, a blank, or a wrong character in accented text |
| Wrong page numbers | contents disagreeing with the pages |
| Inconsistent typography | one heading at the wrong size, usually the last one edited |
| Broken image | absent, stretched, pixelated, or cropped |
| Unreadable content | a table shrunk to fit, a caption at 6pt |
| Overlap | a figure over text, a footer over the last line |
| Wrong cover | the previous version's date, or a placeholder never replaced |

### Print

For anything that will be printed:

- [ ] Printed in greyscale, on paper, and read. Every distinction survives.
- [ ] Nothing enters the binding margin or the unprintable edge.
- [ ] Links show their target in a footnote or an annex.
- [ ] Double-sided pagination correct: sections start where intended.

Where printing is impossible, render at print resolution, convert to
greyscale, and inspect. State that this was done instead of a physical print,
rather than implying a print check that did not happen.

## 5. Reproducibility

A PDF produced once by hand is a PDF nobody can correct.

- The source is text and lives in version control. The PDF is an artefact.
- Generation is one command, recorded in the recipe.
- The recipe records the engine, its version, the fonts and the command.
- Regenerating from an unchanged source produces the same pages. Where the
  engine embeds a timestamp, the byte output differs and the pages do not;
  compare rendered pages, not bytes.
- Never edit the PDF by hand. Edit the source and regenerate, or the next
  regeneration silently discards the correction.

```markdown
## Generation recipe
Engine:   weasyprint 62.3
Fonts:    Source Serif 4 2.100, Source Sans 3 2.045, both embedded
Source:   docs/handover.md, docs/print.css
Command:  make handover.pdf
Verified: 2026-08-11, 34 pages, all fonts embedded, pages rendered and inspected
```

## 6. Accessibility and size

- Set the document language. Without it, a screen reader guesses.
- Reading order must match visual order; verify by extracting the text.
- Images that carry information need alternative text where the engine
  supports it, and a caption in every case.
- Never distribute a scanned image of text as a document. It is unsearchable,
  inaccessible and unquotable.
- Compress images to their display size. A 4000px screenshot on a 600px column
  is 40 times the necessary bytes.
- Keep the file small enough to email. Where it cannot be, split it or link the
  annexes.

## 7. Protocol

1. Confirm the content passed the `document-core` gate and the layout passed
   `document-design`.
2. Select the engine with section 1. Verify it is installed and record its
   version.
3. Verify font glyph coverage for the output language by rendering a sample
   and looking at it.
4. Build the structure of section 2 and set the metadata.
5. Generate.
6. Run the automated checks of section 4.
7. Render the pages to images and inspect them. This step is not optional and
   is not replaced by the automated checks.
8. Fix defects in the source, never in the PDF, and regenerate.
9. Re-inspect the pages the fixes touched, plus the pages after them, because
   a pagination fix moves everything downstream.
10. Perform the print check where the document will be printed.
11. Record the recipe and the verification report.
12. Name the file as an index entry and deliver.

## 8. Auto-critique

Score 0 to 5: engine chosen from the document and verified installed, fonts
embedded and glyph coverage checked by rendering, structure complete, metadata
correct, automated checks run, pages rendered and actually inspected, defects
fixed in the source, re-inspection after pagination changes, print check where
applicable, recipe recorded and reproducible.

Threshold: no axis below 3, average at least 4. For a document leaving the
organisation, average at least 4.3.

Automatic failure: delivering a PDF whose pages were never rendered and
looked at, a non-embedded font, a hand edit to the PDF, or a contents page
whose numbers were not regenerated after the final edit.

## 9. Interfaces

- Upstream: `document-design`, `technical-writing`, `user-documentation`,
  `report-writing`, `administrative-writing`.
- Downstream: `self-critique`, `client-handover`.
- Related: `document-core` section 7 gates 9 to 11 are executed here.
