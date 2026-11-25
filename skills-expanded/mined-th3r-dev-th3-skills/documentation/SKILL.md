---
name: documentation
description: >-
  Documentation toolkit, one skill with sub-skills. (1) doc-style: write and build documentation for any
  work product (API, deploy or update, system, feature, release, test round) in one house style, seven
  fixed skeletons, a TH Sarabun theme with change highlighting, and a matching PDF + DOCX from one
  Markdown source; (2) pdf-operations: merge, split, extract, reorder, rotate or overlay PDF pages
  through an existing pdf-lib pipeline instead of reimplementing it. Use WHENEVER the user wants to
  document, write up, report on or hand over something ("write an API spec", "เขียนเอกสาร",
  "ทำรายงานอัปเดต", "make a user guide", "changelog for this release", "export as PDF and Word"),
  make a document match the house style, or merge / split / rotate / stamp PDFs. Read the sub-skill's
  SKILL.md before acting.
---

# documentation: sub-skills

| When the work is… | Read | Scripts |
|---|---|---|
| "write an API spec", "เขียนเอกสาร", "user guide", "README", "changelog", "export as PDF and Word" | [`doc-style/SKILL.md`](doc-style/SKILL.md) + [`references/doc-types.md`](doc-style/references/doc-types.md) | `doc-style/scripts/build_doc.py` (Markdown → HTML/PDF/DOCX) |
| "merge these PDFs", "split into pages", "rotate / reorder pages", "stamp an overlay" | [`pdf-operations/SKILL.md`](pdf-operations/SKILL.md) | none: reuses the project's `pdf-lib` pipeline |

They chain: `doc-style` builds the PDF; `pdf-operations` merges it with annexes or stamps it.

## Rules every sub-skill keeps

- **Ground every fact in the source.** A document states only what the code, ticket or output shows.
- **Reuse before building.** One theme file, one existing PDF pipeline; no second copy of either.
