---
name: codex
description: Independent second-opinion workflow for Codex. Use when the user wants an adversarial review, a second-pass challenge, or a separate consultation mode inside the current workflow.
---

# Codex

Use this skill when the user wants a deliberately independent second opinion instead of a continuation of the same reasoning path.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Modes

- `REVIEW`: pass/fail second review
- `CHALLENGE`: adversarial attempt to break the current plan or code
- `CONSULT`: focused consultation on a hard question

## Workflow

1. Choose the mode explicitly.
2. Restate the work product or question under review.
3. Re-check it from a different angle, reusing `cross-modal-review` patterns when helpful.
4. Report agreement, disagreement, and confidence clearly.

## Guardrails

- Do not simply repeat the first analysis in softer words.
- Keep the second opinion meaningfully independent.
- If there is no real disagreement, say so plainly.
