---
name: sdo-docx-formatting
description: Reusable .docx formatting conventions for formal standardization documents. Use when formatting headings, notes, enumerations, tables, figures, cross-references, citations, and text in technical standards documents. Applies across SDOs -- concrete style names are provided by the per-SDO drafting skill. Triggers include "format this document", "apply styles", "add cross-references", "insert table/figure", "format notes or citations".
---

# Standards Document Formatting

Apply these conventions for formal technical documents across all SDOs
(3GPP, ETSI, ITU-T). This skill describes **what** to do at the conceptual
level. Concrete Word style names vary per SDO and are provided by the
per-SDO drafting skill (`3gpp-drafting`, `etsi-drafting`, `itut-drafting`).

## Core rules

1. Apply formatting exclusively through **named paragraph and character styles**
   defined in the document template. Never apply direct/ad-hoc formatting
   (e.g., toggling bold, changing font size, or adding colour without a named
   style). If a required named style is missing from the document template,
   inform the user and offer to create the style definition before applying it.
2. Keep numbering and references **update-safe** -- use SEQ fields and
   bookmarks, never hard-coded numbers.
3. Use **non-breaking spaces** (`\u00a0`) for semantic units (number+unit,
   Figure/Table+number).
4. Use **real tab runs** (`<w:tab/>`), never spaces, for tab-separated
   structural elements (heading number+title, enumeration bullet+text,
   note label+text). See `sdo-docx-operations` for officecli patterns.

## Style-name abstraction

This skill uses **abstract style names**. Each SDO drafting skill provides
the concrete mapping. Example:

| Abstract name | Purpose | 3GPP / ETSI | ITU-T |
|---|---|---|---|
| `body-text` | Main body paragraphs | `Normal` | `Body Text` |
| `heading-1` through `heading-3` | Section headings | `Heading 1`--`Heading 3` | `Heading 1`--`Heading 3` |

Always consult the per-SDO drafting skill for the correct concrete style IDs.
If the per-SDO drafting skill is not available in context, ask the user which
SDO applies and use the example mappings in the table above as defaults.

## Conventions by domain

### Document mode (apply first)

Determine document class before applying structural rules:

- **Standards mode** (specifications, reports, Recommendations, Norms):
  use clause-centric structure (`N`, `N.M`, `N.M.P`), and treat
  normative references as an early clause (typically clause 2).
- **Meeting-document mode** (contributions, submissions, TDoc/TD):
  section-oriented structure is allowed by template/SDO practice, and
  reference sections are often placed near the end.

If uncertain, ask the user whether the document is a meeting document or
an actual standard.

### Headings (critical rules)

- **Never use MS Word automatic numbering** for clauses/sections. Use
  `<w:tab/>` between heading number and title.
- Numbering: `N` → `N.M` → `N.M.P`.
- In **standards mode**, use clause terminology (not section terminology)
  for internal structure and cross-references.
- `References` is not numbered when represented as a standalone heading.

### Enumerations (critical rules)

- **Never use MS Word built-in list feature.** Prefer en-dash (`–`)
  enumerations with `<w:tab/>` after the bullet.
- Styles: `enum-1`, `enum-2`, `enum-3` for hierarchy levels.

### Notes (critical rules)

- Format: `NOTE\u00a0N:\t<text>` (uppercase NOTE, non-breaking space, real
  tab). Omit number for single notes.
- Last note in a block → `note-main`; preceding notes → `note-continuation`.

### Tables and Figures (critical rules)

- Table caption **above**: `Table\u00a0N: <text>` with `{SEQ Table \* ARABIC}`
  field; bookmark `tbl_<name>` around the number part only.
- Figure caption **below**: `Figure\u00a0N: <text>` with `{SEQ Figure \* ARABIC}`
  field; bookmark `fig_<name>` around the number part only.
- **Never hard-code numbers.** Cross-ref with `{REF bookmark}`.

### Citations (critical rules)

- Each entry: `[N]\t<text>` using `reference-entry` style and `{SEQ Ref \* ARABIC}`
  field. Bookmark `ref_<name>` around the sequence field only.
- In **standards mode**, normative `References` are typically near the
  beginning (often clause 2). If a `Bibliography` exists, it is an
  informative end section/appendix and follows annexes.
- In **meeting-document mode**, a `References` section is commonly placed
  near or at the end.

### Text formatting (critical rules)

- Use `body-text` for paragraphs, `code-text` for inline code/filenames.
- Non-breaking spaces between number+unit and Figure/Table+number.
- Straight quotes only (`"`, `'`), never curly/typographic.

### Equations (critical rules)

- Display equations: single paragraph with style `equation`, structure
  `\t<equation>\t(<SEQ EQ>)`.
- Do **not** hard-code equation numbers. Use `{SEQ EQ \* ARABIC}`.
- Bookmark `EQ_<name>` around the numbered label for cross-referencing.
- Inline equations mixed with body text use `oMath` runs, no numbering.

______________________________________________________________________

Full details in reference files:

- [references/headings.md](references/headings.md)
- [references/enumerations.md](references/enumerations.md)
- [references/notes.md](references/notes.md)
- [references/tables-figures.md](references/tables-figures.md)
- [references/equations.md](references/equations.md)
- [references/citations.md](references/citations.md)
- [references/text-formatting.md](references/text-formatting.md)

## Cross-references

- `sdo-docx-operations` -- officecli patterns for tab-run injection, field-code injection, bookmark insertion
- `sdo-writing-style` -- prose quality rules for the textual content
- Per-SDO drafting skill (`3gpp-drafting`, `etsi-drafting`, `itut-drafting`) -- concrete style name mapping
