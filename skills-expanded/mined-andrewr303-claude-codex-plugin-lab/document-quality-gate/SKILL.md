---
name: document-quality-gate
description: Verify final Word, PDF, PowerPoint, and document artifacts before delivery. Use for render QA, export checks, accessibility, metadata/privacy checks, comments/tracked changes state, file provenance, page/slide inspection, and final artifact handoff.
---

# Document Quality Gate

Use this skill before delivering a final document, PDF, or presentation.

## Required resources

Read relevant resources:

- `../document-word-pdf/references/quality-gates.md`
- `../../docs/skills/documents/SKILL.md` for DOCX rendering, accessibility, comments, tracked changes, metadata, redaction, and OOXML checks.
- `../../docx-win/SKILL.md` for Word COM verification.
- `../../pptx-win/SKILL.md` and `../../pptx-win/references/visual-qa-rubric.md` for slide QA.
- `../../agents/office-com-validator.md` and `../../agents/visual-critic.md` as checklists.

## Gate by artifact

### DOCX

- Final `.docx` exists.
- Source was copied before edits.
- Fields and TOC updated if present.
- Comments/tracked changes state matches user request.
- PDF or page-image render produced when possible.
- Every final page inspected.

### PDF

- Final `.pdf` exists.
- Page count checked.
- Pages rendered/opened when possible.
- No clipping, broken fonts, bad orientation, missing images, unreadable charts, or table overflow.
- Redaction is real when redaction was requested.

### PPTX

- Final `.pptx` exists.
- Slide count checked.
- Notes preserved unless removal requested.
- Slide images exported when possible.
- Every final slide inspected.
- PDF exported if requested.

### Prose

- Beautiful-prose resources applied.
- No unsupported facts or citations.
- No AI-tell patterns left in the final copy.

### Data

- Totals reconcile.
- Units, currency, and dates are visible.
- Assumptions are labeled.
- Chart visuals match source data.

## Handoff language

Use precise verification status:

- `render verified`: final pages/slides were rendered and inspected.
- `export verified`: final format was exported and basic artifact checks passed.
- `static checks passed`: package or structural checks passed, visual render not inspected.
- `not run`: check skipped with reason.
- `blocked`: missing app, missing renderer, missing credentials, or unavailable dependency prevented verification.

Do not say "verified" by itself.
