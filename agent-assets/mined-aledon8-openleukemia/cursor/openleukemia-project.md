---
description: OpenLeukemia project instructions
globs:
  - "**/*"
alwaysApply: true
---

# Cursor Project Rules

OpenLeukemia is a patient-centered leukemia data platform for organizing medical data, tracking changes over time, extracting structured information from documents, and explaining validated model outputs.

## Always Follow

- Patient data belongs to the patient.
- Registration is not blanket consent.
- Consent must be separate, explicit, auditable, and revocable.
- AI may summarize, extract, and explain; it must not diagnose, recommend treatment, or make urgent clinical judgments.
- Read nearby code and docs before editing.
- Keep changes minimal and focused.
- Follow existing React, TypeScript, Supabase, FastAPI, and Python patterns.
- Run or recommend the relevant checks after changes.
- Do not rewrite unrelated files or add dependencies without clear need.

## Checks

- Frontend: `npm run lint:frontend`, `npm run typecheck:frontend`, `npm test --workspace frontend`, `npm --workspace frontend run build`.
- AI service from `ai-service/`: `python -m ruff check .`, `python -m pytest`, `python -m mypy app`.
