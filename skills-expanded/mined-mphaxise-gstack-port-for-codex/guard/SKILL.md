---
name: guard
description: Maximum-safety workflow for Codex. Use when the task needs both destructive-action caution and a strict edit boundary.
---

# Guard

Use this skill when the safest mode is to combine `careful` and `freeze`.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Set the edit boundary.
2. Flag destructive actions before taking them.
3. Prefer the smallest reversible change inside the boundary.

## Guardrails

- Do not violate either the scope boundary or the destructive-action warning discipline.
- If the best fix requires broader access, pause and realign before continuing.
