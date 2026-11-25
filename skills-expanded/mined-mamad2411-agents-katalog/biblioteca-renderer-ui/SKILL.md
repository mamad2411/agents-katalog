---
name: biblioteca-renderer-ui
description: Use for Biblioteca Virtual React renderer changes in pages, components, state, styles, routing, table/detail/edit UX, empty states, loading states, Spanish copy, or visual design work that must preserve dynamic Excel columns.
---

# Biblioteca Renderer UI

Use this skill to make renderer changes without breaking dynamic workbook columns or the app's Spanish user experience.

## First Reads
1. `AGENTS.md`
2. `docs/design-guidelines.md`
3. `docs/product-rules.md` if table, detail, edit, fields, or enrichment are involved
4. `references/ui-change-checklist.md` for field-heavy or visual work

## Renderer Guardrails
- User-facing copy stays in Spanish.
- Documentation and code comments stay in English.
- Main table remains the operational center and shows all Excel columns by default.
- Detail and edit views must work from real workbook columns.
- Enrichment can make the detail page richer, but cannot appear in the table or write back to Excel.
- Keep components focused. Prefer small field utilities over page-level special cases.
- Preserve existing design direction unless the user asks for a redesign.

## Testing
- Use `tests/renderer` for React behavior and user interactions.
- Use `npm run typecheck` for cross-process contract confidence after renderer API changes.
- Consider `npm run test:e2e` only when app startup, routing, or Electron integration is affected.

## Review Prompt
Before finishing renderer work, answer:
- Did every workbook column still flow from `snapshot.columns`?
- Did I add any display-only data that could be mistaken for a workbook field?
- Is visible copy Spanish?
- Does the UI still make the active document and Excel-backed edits clear?
