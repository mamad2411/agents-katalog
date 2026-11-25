---
name: unfreeze
description: Clear a prior edit boundary in Codex. Use when a frozen scope should be widened and broader edits are now allowed.
---

# Unfreeze

Use this skill when an earlier `freeze` boundary should be removed or widened.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. State that the prior scope boundary is no longer active.
2. Confirm the new effective edit scope.
3. Continue work with the updated boundary.

## Guardrails

- Do not keep pretending a freeze boundary exists once it has been cleared.
- If the user only wants a partial expansion, state the new scope explicitly.
