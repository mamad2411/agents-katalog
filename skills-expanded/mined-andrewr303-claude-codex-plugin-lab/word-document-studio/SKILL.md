---
name: word-document-studio
description: Create, edit, review, redline, comment, polish, transform, and export Word, DOC, and DOCX files. Use for Word documents, DOCX deliverables, legacy DOC conversion, clean copies, tracked changes, comments, table of contents, headers, footers, title pages, report layout, and Word-to-PDF export.
---

# Word Document Studio

Use this skill for all Word, `.doc`, and `.docx` work.

## Required resources

Read the relevant resources before acting:

- `../../docx-win/SKILL.md` for Windows Microsoft Word COM automation.
- `../../docx-win/references/document-quality-map.md` for no-template polished Word deliverables.
- `../../docs/skills/documents/SKILL.md` for DOCX rendering, OOXML utilities, Google Docs preparation, accessibility, comments, tracked changes, metadata, redaction, and structural QA.
- `../../beautiful-prose/SKILL.md` and `../../beautiful-prose/references/ai-tells.md` for substantial prose generation or rewriting.
- `../../visual-design-skill.txt` for cover pages, title pages, and visually polished report packaging.

## Default workflow

1. Identify user intent: create, edit, redline, review, redesign, convert, clean, export, or compare.
2. Copy the source file before modifying it.
3. If source is `.doc`, convert to `.docx` before heavy edits.
4. Preserve source styles and structure unless redesign is requested.
5. For new or heavily redesigned documents, choose a document archetype and style system before writing code.
6. Use Word styles, section breaks, fields, headers, footers, tables, captions, comments, and tracked changes as real Word structures.
7. Use beautiful-prose resources before drafting or rewriting substantial prose.
8. Update fields, TOC, page numbers, captions, and cross-references before final save.
9. Export PDF or render pages for layout QA when formatting matters.
10. Deliver a new `.docx`, plus PDF only when requested or useful.

## Edit modes

- `clean copy`: apply edits and remove temporary comments/revisions only when requested.
- `tracked changes`: turn on tracking before edits; preserve reviewability.
- `comments`: add comments at the relevant range, not in a detached appendix.
- `review only`: add critique/comments without silently rewriting.
- `redesign`: rewrite layout system and visual hierarchy, but preserve factual meaning.
- `faithful reconstruction`: match a source PDF or image as closely as practical in editable Word form.

## Word design requirements

- Use a title page or title block when the artifact warrants it.
- Use real heading styles.
- Use readable type sizes and clear hierarchy.
- Avoid walls of text unless the document genre requires them.
- Use tables only for genuine tabular data.
- Give tables explicit widths, padding, alignment, and repeated headers when needed.
- Keep captions, charts, and tables paired with their explanations.
- Avoid fake bullets, manual numbering, and ad hoc formatting drift.

## Verification

Before delivery, when tooling is available:

- Save the final `.docx`.
- Export to PDF or render page images.
- Inspect every final page for clipping, overlap, missing glyphs, broken tables, bad page breaks, broken headers/footers, and unintended blank areas.
- Confirm comments/tracked changes/clean-copy state matches the user's request.

If Word COM or rendering is unavailable, use structural checks from the bundled documents package and disclose that visual render QA was not run.
