---
name: product
description: Product management — PRD, Master/Sprint stories (ADO-ready), analytics, gap analysis
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

> **Authoring standards:** [templates/AUTHORING_STANDARDS.md](../../templates/AUTHORING_STANDARDS.md)

# Product Management Skill

## Capabilities

- **PRD:** Use **`templates/prd-template.md`** — include **user-visible copy / notifications** tables when UX has strings (feeds Master/Sprint ADO lift).
- **Master Story:** `skills/shared/story-generator/` + **`templates/story-templates/master-story-template.md`** (📎 PRD-sourced specifics, 🎨 UI & design).
- **Sprint Story:** `skills/shared/sprint-story-generator/` + **`sprint-story-template.md`**.
- **PRD Review / gap analysis:** `skills/shared/prd-gap-analyzer/` for quality; do not skip notification/copy gaps if stories depend on them.
- **Analytics:** Success metrics and events—traceable to PRD §8 and story Measurement sections.

## Process Flow

1. Align on **AUTHORING_STANDARDS** (ADO-ready, no redundant sections).
2. PRD completeness (including copy tables when applicable).
3. Master Story from PRD (verbatim lift for notifications/errors).
4. Sprint breakdown with non-redundant measurement vs validation.
5. Grooming-ready handoff to engineering (Tech Story optional via tech lead).

## Quality Standards

- Work items readable **without** opening PRD for copy already in PRD.
- Testable acceptance criteria; **USER_INPUT_REQUIRED** where facts are missing.
- Clear traceability: PRD ids → Master → Sprint.

## Skill Triggers

- Feature definition, PRD refresh, story generation, grooming prep.
