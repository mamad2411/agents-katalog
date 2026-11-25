---
name: pre-grooming-brief
description: Pre-grooming brief — team context, risks, aligned to story templates and AUTHORING_STANDARDS
model: sonnet-4-6
token_budget: {input: 6000, output: 2500}
---

> **PRD analysis:** Use `skills/shared/prd-gap-analyzer/` first; do not duplicate gap checks here.
>
> **Authoring standards:** Brief must remind teams that **Master/Sprint/Tech/Task** artifacts follow [`templates/AUTHORING_STANDARDS.md`](../../templates/AUTHORING_STANDARDS.md) (ADO-ready PRD lift, Figma/UI, traceability, non-regression).

# Pre-Grooming Brief Skill

Create a **pre-grooming** briefing so engineering can produce **master-story-template** / **sprint-story-template** / **tech-story-template** / **task-template** files without inventing scope.

## Brief contents

- **Executive summary**: Problem and outcome (no duplicate of full PRD—cite PRD §).
- **PRD readiness**: Summary of **prd-gap-analyzer** output; open gaps (especially **user-visible copy** tables).
- **Story overview**: Feature slices that map to **Master** then **Sprint** stories; initial AC references (not full duplicate of PRD).
- **Design context**: Links to **design-doc** §0, Figma, ADRs.
- **Team assignments**: Roles for story authoring and review.
- **Success criteria**: Metrics from PRD §3 / §8.
- **Risks & dependencies**: From PRD §10–12.
- **Suggested grooming agenda**: Order (PRD sign-off → Master → Sprint → Tech optional → tasks).

## Process

- Ingest PRD + gap analysis + any design links.
- Align bullets to **TEMPLATE_REGISTRY** story tier—not legacy DEPRECATED templates.

## Triggers

- Epic or large feature ready for grooming.
- After PRD approval and **prd-gap-analyzer** pass (or explicit waiver list).

## Inputs

- PRD (markdown), **prd-gap-analyzer** report, design links, team roster.

## Outputs

- `pre-grooming-brief.md` (or equivalent) with explicit **next steps** for story file creation (`sdlc story create master|sprint|tech|task`).

## Quality

- Brief does **not** replace PRD or full Master Story—points to templates and standards.
- Copy/notification gaps called out if check 8 failed.
