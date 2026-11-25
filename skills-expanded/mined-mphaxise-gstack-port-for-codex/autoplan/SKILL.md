---
name: autoplan
description: Automatic planning pipeline for Codex. Use when the user wants one command to run the current planning stack and consolidate the result into a single reviewed plan.
---

# Autoplan

Use this skill when the user wants the repo's planning stack applied in one pass instead of invoking each planning skill manually.

This port is adapted from `garrytan/gstack` at commit `a3259400a366593e0c909dd9ac3e59752efd2488`.

## Important Adaptation

The current Codex port has the full upstream planning-review surface:

- `office-hours`
- `plan-ceo-review`
- `plan-eng-review`
- `plan-design-review`
- `plan-devex-review`

Run design review only when the plan has a user-facing UI or interaction surface. Run DX review only when the plan changes developer-facing APIs, tooling, setup, documentation, or operational workflows.

## Workflow

1. Read the plan, idea note, or repo context.
2. If the idea is still fuzzy or pre-plan, start with `office-hours`.
3. Apply the `plan-ceo-review` lens to pressure-test framing and scope.
4. Apply the `plan-eng-review` lens to pressure-test architecture, sequencing, and tests.
5. Apply `plan-design-review` and `plan-devex-review` conditionally.
6. Keep an explicit decision audit trail: auto-resolved execution details, user-owned taste or scope calls, and deferred work.
7. Consolidate the result into one recommended plan with implementation tasks and concrete next actions.

## Guardrails

- Do not claim that a conditional review ran unless its trigger applied and you actually used it.
- Ask at most one concise question when a real ambiguity would change the recommendation materially.
- Do not start implementation unless the user explicitly pivots from planning to coding.
- Prefer one final integrated recommendation over dumping three disconnected mini-reviews.

## Outputs

Always include:

- what inputs were reviewed
- whether `office-hours` was used
- CEO/framing findings
- engineering/execution findings
- design and DX findings or an explicit not-applicable note
- decision audit trail
- consolidated recommendation
- next 1-3 actions
