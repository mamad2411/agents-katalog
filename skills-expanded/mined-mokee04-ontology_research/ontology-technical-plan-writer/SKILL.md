---
name: ontology-technical-plan-writer
description: Draft or refine a technical planning document template for an ontology project. Use when the user wants a technical proposal, planning brief, or reusable template that connects scope, competency questions, standards reuse, modeling approach, validation, governance, and execution phases without drifting into a business-only pitch.
---

# Ontology Technical Plan Writer

Read:

- `../refs/Total Guide.md`
- `../shared/references/templates.md`
- `./references/technical-planning-template.md`

Use this skill when the user wants a technical ontology planning document or a reusable template for one.

## Tasks

1. Decide whether the user needs a blank template, a lightly customized template, or a first populated draft.
2. Reuse existing planning artifacts when they exist, especially scope, competency questions, risks, and required standards.
3. Structure the document around technical decision-making, not business marketing language.
4. Prefer tables for scope, CQ summary, data feasibility, risks, approval gates, and open questions.
5. Keep planned work, completed evidence, and open assumptions clearly separated.
6. Mark approval gates, validation checkpoints, and unresolved questions explicitly.

## Outputs

Write or refine one of:

- `../exe/<run-id>/planning/technical-plan.md`
- a standalone markdown planning document when no run folder exists yet

## Guardrails

- do not present unverified research as settled fact
- do not collapse scope, modeling, and validation into one vague summary
- do not omit reuse-first or CQ-first rationale
- do not write a budget or sales deck unless the user asks for it
