# AGENTS.md — Work contract for UX/UI work

You are designing or implementing user interfaces under **design-system-standard** `v0.2`.
This file is your employment contract for interface work.

Do **not** invent a one-off visual language, skip accessibility, or call a UI “done”
because it “looks fine” in one screenshot.

## Required workflow

```text
BEFORE UI WORK
    ↓
Read AGENTS.md + VERSION
    ↓
Read PRINCIPLES.md + REFERENCE-SOURCES.md
    ↓
Load applicable rules from rules/ (cite IDs)
    ↓
Check platforms/ + interaction/ for the surface
    ↓
Check states/ matrix
    ↓
Implement smallest consistent change
    ↓
Run / perform validation (npm run validate in this repo; a11y/tests in app)
    ↓
Return DESIGN REVIEW format (ai/compliance-format.md)
```

## Non-negotiable

1. Prefer **existing tokens and components** over new one-offs (DS-001, DS-002, UI-003, UI-005).
2. Every interactive control: accessible name, keyboard path, visible focus (A11Y-001, A11Y-004, A11Y-006).
3. Never use placeholder-only labels (UX-007).
4. Never ship color-only meaning (UI-004).
5. Never claim WCAG conformance without contrast, keyboard, and names.
6. Do not introduce a new color/spacing/type scale without tokens + docs.
7. Include states: default · hover · focus · active · disabled · loading · empty · error · success (+ permission/offline when relevant).
8. Cite **rule IDs** in compliance summaries.

## Hard stops

- Invisible focus (A11Y-006)
- Icon-only controls without names (UI-007 / A11Y-001)
- Forms without persistent labels (UX-007)
- Modals without APG behavior (CMP-005)
- Contrast failures on primary reading paths (A11Y-008)
- Hover-only critical actions on touch (RWD-003)

## Output

Use [`ai/compliance-format.md`](ai/compliance-format.md). Status FAIL if any applicable MUST is violated.

## Routing

| Need | Where |
|---|---|
| Rule by ID | `rules/` |
| Traceability | `compliance/` |
| Platforms | `platforms/` |
| Input methods | `interaction/` |
| States | `states/` |
| Data / money / dates | `data-display/` + DATA-* |
| i18n | `localization/` + I18N-* |
| Anti-patterns | `anti-patterns/` |
| Schemas | `schema/` |
