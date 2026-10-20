---
name: plan-goal
description: >
  Goal-driven iteration: define a measurable/evaluable/research gate, then
  modify → judge until it passes or the round cap hits. Use when the user
  says goal loop, drive this metric, rasen-goal, or /ultimate-sdd:goal.
license: MIT
metadata:
  author: andrewr303
  version: "2.3"
---

Done is a **condition**, not a document.

**Supporting files:** `references/rasen.md`, `templates/goal-plan.md`, `scripts/plan.py`.

Pipelines: `goal-measure` (command + threshold), `goal-evaluate` (rubric), `goal-research` (brief answered).

## define-goal (vet gate)

Write `docs/plan/goals/<slug>.md` from `templates/goal-plan.md`:

- Intent
- Measure command **or** rubric **or** research question
- Threshold / pass condition
- Round cap (default 5)
- What must not change

`define-goal` is a **vet** gate: show the measure command and wait. Never auto-approve a shell command you authored.

Start the matching pipeline: `plan.py run start --pipeline goal-measure|goal-evaluate|goal-research`.

## iterate

Each round:

1. Make the smallest change that could move the gate.
2. Run the measure / score the rubric / update the brief.
3. Record round n in the goal file (command, result, pass/fail).
4. Stop on pass, cap, or regression you cannot explain.

Do not silently lower the threshold.

## Guardrails

- Vet before any repeated command.
- Evidence is the command output or rubric table, not "looks better".
- After pass, offer retain + archive if a CHANGE exists.
