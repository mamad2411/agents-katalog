---
name: prd-gap-analyzer
description: PRD validation — completeness, clarity, testability, feasibility, and ADO-ready copy tables
model: sonnet-4-6
token_budget: {input: 3000, output: 1500}
---

> **Authoring standards:** Downstream **Master/Sprint** stories require liftable content from the PRD. See [`templates/AUTHORING_STANDARDS.md`](../../templates/AUTHORING_STANDARDS.md).

# PRD Gap Analyzer Skill

Validate PRD completeness and identify gaps **before** grooming and story generation.

## Validation checks

1. **Completeness**: Requirements and flows covered; nothing critical missing.
2. **Clarity**: Unambiguous, well-defined statements.
3. **Testability**: Each requirement mappable to verifiable AC.
4. **Feasibility**: Technical risks and constraints surfaced.
5. **Acceptance criteria**: Measurable, SMART where applicable.
6. **Dependencies**: External and internal dependencies documented.
7. **Constraints**: Business and technical constraints explicit.
8. **User-visible copy & notifications** *(blocks ADO-ready stories if empty)*: For any UX that shows text, **§6** (or equivalent) must include **tables** for notifications, errors, and key labels—all locales the product requires. Stories will **not** invent copy; gaps → `USER_INPUT_REQUIRED` or PRD fix. *(See `prd-template.md` subsection “User-visible copy, notifications & errors”.)*

## Analysis

- Map requirements to future **Master Story** sections (Outcome, 📎 PRD-sourced specifics, AC).
- Flag **id-only** references (e.g. “Notification N7”) without defined text in the PRD.
- Verify acceptance criteria are SMART where product committed to metrics.

## Triggers

- PRD received or uploaded (`sdlc doc convert` → markdown, then analyze).
- Before grooming or `story-generator` / `sprint-story-generator` runs.

## Inputs

- PRD markdown (prefer structure aligned with `templates/prd-template.md`).

## Outputs

- Gap analysis report with prioritized fixes.
- Checklist including **check 8** (copy tables).

## Quality

- All **8** checks addressed in the report.
- Actionable recommendations (owner: PM / design for copy gaps).
