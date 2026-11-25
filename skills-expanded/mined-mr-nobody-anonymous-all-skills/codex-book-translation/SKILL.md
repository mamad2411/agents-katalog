---
name: codex-book-translation
description: "Produce publisher-grade translated books from source books or PDFs with agent-authored translation and polish: do not use machine-translation libraries, translation APIs, local translation models, or browser translation to generate the prose. Preserve figures/tables/notes, build EPUB or ebook outputs, and cross-check against original pages. Use for long-form literary, nonfiction, academic, technical, illustrated, textbook, report, or reference-book translation projects."
source: "https://github.com/hongfei/codex-book-translation"
source_repository: "hongfei/codex-book-translation"
source_path: "SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Publisher-Grade Book Translation and Ebook Production

Use this skill to turn any source book into a readable, deliverable translated edition. It applies to novels, nonfiction, academic books, manuals, biographies, illustrated books, textbooks, reports, and other long-form works.

## Role

Act as all of the following:
- Target-language publishing editor
- Domain translation reviewer
- Ebook production engineer
- Original-book comparison QA reviewer

If the target language is not specified and the user writes in Chinese, default to Simplified Chinese. If the source file, target language, or output format cannot be inferred, ask only the essential questions.

## Principles

- Treat the original book as authoritative: do not change structure, facts, numbers, quotations, figures, notes, or sequence without cause.
- Establish a page-by-page visual baseline first; extracted text is a working draft, not the authority.
- Do not treat Markdown as the only intermediate format. Markdown is suitable for translation drafts; structure and publishing semantics must live in JSON/XHTML.
- Translate faithfully without being literalistic; prefer target-language prose that readers understand naturally.
- The current AI agent must read context and author the translation and polish directly. Use scripts only for extraction, construction, checks, and issue localization.
- Do not delegate body-text translation to machine-translation tools or models: do not call Python translation libraries, local Hugging Face/Transformers translation models, DeepL/Google Translate/Baidu/Youdao APIs, browser page translation, or similar MT tools to generate draft prose.
- You may use dictionaries, terminology databases, authoritative references, or web search to verify terms and facts, but final translated sentences must be written by the agent from the source text, context, glossary, and target-language style.
- Create a glossary and style sheet for every project, then apply them consistently across the whole book.
- Do not turn complex pages into whole-page screenshots. Crop only real figures, tables, formulas, illustrations, or complex layout regions.
- When charts or tables cannot be reflowed reliably, use cropped images from the original page and remove broken OCR table remnants from body text.
- Notes must look and behave like notes, preferably close to the source text they annotate; do not let them become ordinary paragraphs or list items.

## Recommended Directory Layout

```text
book_project/
  original/
    source.pdf
    source-info.md
  pages/
    page-images/
      page-0001.png
  structure/
    page-map.json
    book-map.json
    segments.jsonl
  src/
    extracted-text/
    target-draft-md/
    target-xhtml/
  assets/
    display-crops/
    cover/
  epub/
    book.css
    formatting_decisions.json
  tools/
    extract_text.py
    build_epub.py
    validate_epub.py
  review/
    page-checks/
  dist/final.epub
```

For existing projects, follow the existing structure.

## Bundled Resources

When rendering, cropping, or checking images, prefer this skill's scripts:
- `scripts/render_pages.py`: Render PDF pages to per-page images.
- `scripts/crop_region.py`: Crop figures, tables, formulas, illustrations, and complex layout regions by coordinates.
- `scripts/make_contact_sheet.py`: Generate a review overview for cropped images.
- `scripts/validate_images.py`: Check for missing, blank, unusually sized, or duplicate images.

References:
- `references/workflow.md`: Complete visual-first workflow.
- `references/quality-checklist.md`: Human final-review checklist.
- `references/page-map.schema.json`: Recommended structure for `page-map.json`.
- `references/book-map.schema.json`: Recommended structure for `book-map.json`.
- `references/middle-format.md`: Guidance on intermediate-format choices.

Templates:
- `templates/page-map.example.json`: Example page-structure inventory.
- `templates/book-map.example.json`: Example whole-book logical map.
- `templates/crop-manifest.example.json`: Example batch-crop manifest.

## Workflow

### 1. Source Evidence

- Regardless of source format, first convert or render the source into per-page images as the visual authority. For PDFs, use `scripts/render_pages.py`.
- Confirm the source file, page count, edition, author, and copyright-page information.
- Extract text or Markdown as an editable working draft while preserving page anchors.
- Create `structure/page-map.json` to record each page's headings, body text, footnotes, figures, tables, sidebars, formulas, and special layouts.
- Mark OCR problems: broken words, broken URLs, headers/footers, page numbers, mixed columns, and table fragments.

### 2. Reconstruct Structure

- Consult both page images and the text working draft; page images determine structure, while the text draft supports editing.
- Build the chapter map before translating.
- Distinguish cover, copyright page, table of contents, preface, body, appendix, notes, bibliography, and index.
- Preserve heading hierarchy, note markers, cross-references, and image placement.
- Page-number comments may remain in working drafts; they must not leak into the final EPUB.

### 3. Intermediate Formats

Use layered intermediate formats:
- `page-map.json`: Page-level visual structure, recording what appears on each page.
- `book-map.json`: Whole-book logical structure, recording chapters, page ranges, source files, translation files, figures, notes, and order.
- `segments.jsonl`: Optional paragraph or segment alignment data for proofreading and breakpoint tracking.
- `target-draft-md/`: Optional translation drafts for manual editing and diffing.
- `target-xhtml/`: Publishing-semantic source, used as the primary EPUB build input.

Markdown does not carry complex tables, note anchors, figure coordinates, cross-page structure, or final publishing semantics. Store those details in JSON or XHTML.

### 4. Terminology and Style

Before translating, build project tables for:
- Proper names such as people, places, organizations, book titles, concepts, objects, products, and species
- Chapter-title translations
- Units, dates, percentages, currency, and formula handling
- Register and tone: literary, academic, technical, conversational, children's, historical, legal, religious, journalistic, and so on

For specialist books, create at least a small glossary first. For fiction, prioritize consistency for character names, places, forms of address, voice, and invented terms.

### 5. Batch Translation

For every batch:
- Have the agent write the translation directly from the source text, page screenshots, context, and glossary; do not run machine translation first and then patch it.
- If a project already contains suspected machine-translated drafts, treat them as low-trust references only; return to the source and retranslate or fully review each passage before reuse.
- Translate or revise against both page screenshots and the source working draft.
- Preserve numbers, dates, proportions, page references, quotations, note markers, and captions.
- Fix broken words, broken URLs, incorrect fractions, hard line breaks, and leftover hyphenation.
- Split long sentences according to target-language norms.
- Preserve the author's tone, rhythm, argument, ambiguity, humor, and qualifications.

### 6. Publisher-Grade Polish

- Remove translationese, source-language syntax, repeated words, and unnatural passive constructions.
- Keep paragraph lengths comfortable for ebook reading.
- Make lists, quotations, formulas, and examples easy to scan.
- For fiction, preserve character voice, point of view, and scene rhythm.
- For academic or reference books, preserve citations, definitions, bibliography, and index structure.
- For technical or procedural books, preserve warnings, steps, prerequisites, results, and exact meaning.

### 7. Figures, Tables, and Complex Layouts

For every figure, table, chart, and formula block, decide whether to:
- Reflow it if it can be reproduced reliably.
- Crop the original page region with `scripts/crop_region.py` if it cannot be reproduced reliably.
- Crop only the target content: do not crop whole pages or include surrounding body prose.
- Generate an overview with `scripts/make_contact_sheet.py`, then manually check for blank crops, wrong regions, cut-off content, excessive whitespace, or wrong page numbers.
- Add captions, descriptions, and alt text.
- Remove duplicate or broken OCR table text from the body.

### 8. Notes

Handle notes as high-risk content:
- Recognize `*`, `†`, `‡`, `\*`, and numbered notes.
- Prefer placing notes immediately after the annotated paragraph, or use popup/footnote styling close to the source text.
- If long notes, endnotes, or copyright requirements force back placement, provide clear bidirectional links.
- When one paragraph has multiple notes, preserve the original order and avoid moving all notes to the end of a chapter in a way that disrupts reading.
- Give note blocks distinct styling.
- Do not let asterisk notes become unordered lists.
- Do not let escaped `\*` leak as ordinary paragraphs.
- Do not misclassify decimals, numbered items, or years as notes.

Record uncertain numeric lines in the formatting-decision table.

### 9. Build the EPUB

During the build, check:
- `book-map.json`, `target-xhtml/`, and EPUB XHTML chapter order
- Cover, nav, NCX, OPF, CSS, and image assets
- Spine and table-of-contents order
- Whether images are included in the manifest
- Whether page-number comments are hidden
- Whether body text, headings, captions, notes, and table styles are readable
- Whether notes are near the corresponding source text or have reliable return links

Set `lang`, fonts, line height, punctuation, spacing, and quotation conventions for the target language.

### 10. Automated Validation

Run checks for every batch and final version:
- Source text, `book-map.json`, `page-map.json`, Markdown drafts, and XHTML structure
- Note, list, and image counts
- EPUB package structure
- ZIP integrity
- EPUBCheck
- XML/XHTML parsing
- OPF resource references
- Spine/nav order
- Leaked source-page comments
- Markdown syntax remnants
- Escaped-note remnants
- Numeric lines misclassified as notes
- Note anchors and return links
- Machine-translation artifacts: sentence-by-sentence literalism, drifting terminology, context errors, mechanical synonym swaps, or sudden register shifts.
- Use `scripts/validate_images.py` for basic image-asset checks.

Passing automated validation does not mean the book is complete; the final version still requires human review.

### 11. Human Final Review

At minimum, inspect:
- Opening pages and table of contents
- Several chapter openings
- All figure/table/screenshot pages
- Note-dense pages
- Appendices, endnotes, index, and back matter
- Narrow-screen or mobile view

Search for common remnants:

```text
⁄
. html
. com
<p>\*
Source PDF page:
```

Also search for project-specific OCR errors, broken names, bad links, wrong headings, leftover table fragments, and untranslated passages.

## Completion Criteria

- Final EPUB or requested format has been generated.
- In-scope chapters and back matter have been translated and manually polished.
- Body text was translated by the agent from source context; no machine-translation libraries, translation APIs, or local translation models were used to generate the prose.
- Figures and tables have been reflowed or cropped, then manually checked.
- Notes display correctly.
- Validation reports pass.
- EPUBCheck has no errors and preferably no warnings.
- The final report explains changes, validation, and known limitations.

## Final Response Template

```text
Done. Final file: [file](absolute/path/to/file.epub)

I completed publisher-grade translation/editing, figure and table handling, note cleanup, and final validation.
Validation passed: structure checks, EPUB cross-checks, ZIP integrity, EPUBCheck.

Reports:
- [Build report](absolute/path/to/report.md)
- [Cross-check report](absolute/path/to/report.md)
```

State any remaining limitations directly.
