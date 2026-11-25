---
name: prd-writer
description: Draft structured PRDs with problem, goals, use cases, and RACI. For AI/agent surfaces, add jobs, autonomy, failure behavior, and evals as acceptance criteria.
---

# PRD Writer

Write a PRD that a team can implement and test. For AI surfaces, evals are part of the spec — not an appendix you skip.

## When to use

- User asks for a PRD, spec, or requirements doc
- Formalizing an idea into something buildable

## Before drafting

Read, in order:

1. `knowledge/products/<product>/brief.md`
2. `evals.md` if it exists
3. `memory/decisions/` for rejected options
4. Org context in `knowledge/_template/` or `knowledge/examples/` only if needed

Do not invent strategy that is not in those files. If context is missing, say so.

## Standard PRD

Follow `references/prd-template.md`:

1. Header + RACI
2. Current state
3. Customer and business problem statements
4. Ideal state
5. Goals / metrics
6. Features
7. Use cases with acceptance criteria (P0/P1/P2)
8. NFRs
9. Evidence
10. Milestones
11. Open questions

## If the surface is AI

Also follow `references/ai-prd.md`:

- Jobs, not model capabilities
- Autonomy table (alone / confirm / forbidden)
- Failure behavior (stuck, missing evidence, never guess)
- Evals as acceptance criteria — every P0 maps to an eval
- Cost, latency, loop cap
- What launch copy is allowed to claim

Write or update `knowledge/products/<product>/evals.md`. Use the `eval-brief` skill if the golden set does not exist yet.

## Workflow

1. Ask only for what files do not already contain (one short batch).
2. Draft in markdown in `workspace/drafts/` unless the user names another path.
3. Flag any requirement with no metric or eval as open, not P0.

## Rules

- Specific beats vague. "Be helpful" is not a requirement.
- Not everything is P0.
- Link evidence. If there is none, write **Missing**.
- Rejected alternatives belong in a decision record, not a buried FAQ.
