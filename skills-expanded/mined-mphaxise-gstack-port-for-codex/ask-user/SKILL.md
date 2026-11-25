---
name: ask-user
description: Gate execution at a real decision point by asking the user a small explicit question.
---

# Ask User

Use this skill when another workflow cannot safely proceed without a human choice.

## Workflow

1. State the decision that blocks progress.
2. Offer 2-3 concrete options when possible.
3. Explain the practical consequence of each option in one sentence.
4. Wait for the user's answer before taking the gated action.

## Guardrails

- Do not ask questions whose answer can be discovered from the repo.
- Do not bundle many unrelated choices into one question.
- Do not continue past a destructive or privacy-sensitive decision without consent.
