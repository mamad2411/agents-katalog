---
name: plan-tune
description: Planning-preference tuning workflow for Codex. Use when recurring plan questions, scope choices, or explanation style should be captured and reused across future planning work.
---

# Plan Tune

Use this skill when the user wants the planning workflow to learn their preferences around questions, scope, and communication style.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify the repeated friction:
   - too many questions
   - too little explanation
   - recurring scope choice disagreements
2. Capture the preference as a durable planning note.
3. Apply that note to future planning skills when relevant.

## Guardrails

- Do not overfit one-off frustration into a permanent preference.
- Keep the tuned preference clear, durable, and easy to reverse.
- Prefer explicit notes over vague "remember this" language.
