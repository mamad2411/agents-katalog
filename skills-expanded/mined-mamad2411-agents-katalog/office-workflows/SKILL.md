---
name: office-workflows
description: |
  Office and white-collar document workflows: spreadsheets, Word/PDF editing,
  PPT tables, OCR, form filling, and citation/formatting tasks. Use when the
  deliverable is an office artifact (.xlsx/.docx/.pdf/.pptx), a mail-merge /
  template fill, or requires faithful template preservation — especially when
  placeholders may be split across Word XML runs. Not for raw scientific
  numeric pipelines unless the output must be an office file.
---

# office-workflows

Load `safe-agent-scope` before any state-changing action; office deliverables do not waive sandbox, recipient, or injection rules.

## Why

Office tasks grade **artifact fidelity**: zero formula errors, preserved
templates, correct sheet/object names. Models often regenerate a whole file
and destroy the template — or "replace all placeholders" while leaving tokens
that Word had split across XML runs.

## Procedure

1. **Open and inspect** existing templates before writing.
2. **Enumerate fill sites from the data source first** — every key in the
   provided JSON/CSV/instruction is a fill candidate, even if a naive search
   of the file does not show a contiguous `{{KEY}}`. Also list conditional
   blocks (IF/END_IF). Do not stop while any data key is unapplied or any
   `{{` remains in the final artifact.
3. **Preserve conventions** — styles, named ranges, slide masters, form field IDs.
4. **Edits over rewrites** — modify in place when an input file is provided.
5. **Spreadsheets** — formulas must evaluate; no `#REF!` / `#DIV/0!`; document
   hardcoded inputs.
6. **PDF/OCR** — verify extracted text against a visual spot-check when tools allow.
7. **Final** — reopen the artifact; leftover-token search (including inside
   `.docx` XML); then `verify-task-output`.

## Word / OOXML — split placeholders

Word frequently stores one logical token as adjacent text runs, e.g. `{{COMP`
then `ANY_NAME}}`, often with different bold/italic on each half. Per-run
`replace` and regex over a single run miss these.

**Do this instead:**

1. Prefer `python-docx` (install if missing). Work at **paragraph** (and
   table-cell / header / footer) granularity: read the concatenated
   `.text`, replace every `{{KEY}}` from the data dict, then write the
   result back through the paragraph's runs (keep first-run formatting;
   clear the rest) so split pieces collapse.
2. Cover **body + tables + headers + footers**. Nested tables hold many
   offer/comp fields — skipping them fails graders that check cell text.
3. If editing raw `word/document.xml` inside the zip: detect leftovers by
   searching the **concatenation of all `w:t` values**, not each node alone.
   After edits, re-zip and confirm zero `{{` remain in that concatenation.
4. Conditionals: when the flag is yes/true, keep inner content and strip
   markers; when no, remove the whole block including markers.

**Sanity check before exit:** for every key in the data file, confirm the
value appears somewhere in the document text (tables included), and that a
search for `{{` returns nothing.

## Heuristics

- Match existing color/number formats instead of imposing a new standard
- For forms, fill required fields only; don't invent notarization
- Keep embedded objects (charts) linked to data ranges when possible
- Iterate data keys → document, not "regex hits in XML → data" (split runs
  make the latter a partial set)

## Anti-patterns

- Exporting CSV when an `.xlsx` with formulas was required
- Rebuilding a slide deck from scratch and losing layout
- Leaving placeholder text ("TODO", "Lorem", or any `{{TOKEN}}`)
- Replacing only contiguous tokens and declaring success
- Filling body paragraphs but ignoring nested tables / headers / footers
