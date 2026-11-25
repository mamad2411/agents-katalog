---
name: ontology-planning-team
description: Plan a domain ontology effort by clarifying scope, composing the working team, defining competency questions, and setting risk and approval gates before research begins.
---

# Ontology Planning Team

Read:

- `../refs/Total Guide.md`
- `../shared/references/skill-family-architecture.md`
- `../shared/references/templates.md`

Use this skill for the planning stage only.

## Planning Segments

| Segment | Goal | Required user feedback |
| --- | --- | --- |
| P1 Intent clarification | identify the real target outcome and constraints | yes |
| P2 Scope framing | define in-scope, out-of-scope, users, and success target | yes |
| P3 CQ drafting | turn goals into answerable questions | yes |
| P4 Planning package | team plan, risks, approval gates, technical plan | yes |

## Team Composition

Route planning work through:

- `ontology-domain-intake`
- `ontology-cq-designer`
- `ontology-technical-plan-writer` when the user wants a reusable technical planning document

## Tasks

1. Start by asking targeted clarification questions before drafting the ontology plan.
2. Ask the mandatory planning intake questions below unless the user has already answered them clearly.
3. Do not create `intent-clarification.md` or any other planning artifact until the user has answered enough intake questions to distinguish confirmed facts from assumptions.
4. Capture the answers in `intent-clarification.md` using a table that distinguishes confirmed facts, assumptions, and open questions.
5. Clarify domain, purpose, users, decisions to support, and scope boundaries.
6. Record out-of-scope areas and risk constraints.
7. Draft initial competency questions.
8. Identify which later team skills will be required.
9. Define human approval gates before research and release.
10. Pause after each segment and ask the user for confirmation, correction, or reprioritization.

## Mandatory Planning Intake Questions

Ask for concrete answers to these topics before drafting the planning package:

1. What is the first business or operational outcome this ontology must unlock?
2. Which 3 to 5 competency-question-like business questions matter most right now?
3. Who are the primary users and downstream systems?
4. What data already exists for each core entity or axis?
5. What predictions, classifications, or recommendations are expected later?
6. What is out of scope for the first release?
7. What privacy, consent, licensing, or governance constraints apply?
8. What deliverable shape does the user want from this phase?

## Outputs

Write or update:

- `../exe/<run-id>/planning/intent-clarification.md`
- `../exe/<run-id>/planning/scope.md`
- `../exe/<run-id>/planning/competency-questions.md`
- `../exe/<run-id>/planning/team-plan.md`
- `../exe/<run-id>/planning/risks.md`
- `../exe/<run-id>/planning/technical-plan.md` when a technical planning document is requested

## Exit Criteria

Do not hand off to research until:

- the user's target outcome has been clarified and acknowledged
- the mandatory planning intake questions have been answered enough to bound the work
- scope is bounded
- at least a starter CQ set exists
- required standards or constraints are named
- human review gates are explicit
- a planning checkpoint has been reviewed with the user
