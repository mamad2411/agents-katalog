---
name: office-hours
description: YC-style product and project framing for Codex. Use when the user has a new idea, wants to brainstorm whether something is worth building, or needs sharper framing before plan review.
---

# Office Hours

Use this skill when the task is still pre-plan and the highest-leverage move is to sharpen the problem before design or implementation.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Modes

Pick exactly one mode and make it explicit:

- `STARTUP MODE`: default for products, businesses, user demand, or "is this worth building?" questions
- `BUILDER MODE`: default for side projects, internal tools, open source, or learning-oriented ideas

If the right mode is obvious, choose it and say why. If the choice would materially change the recommendation and is not obvious, ask one concise question and wait.

## Workflow

1. Read only the materials needed to understand the idea and current constraints.
2. Choose a mode and state the reason.
3. Pressure-test the idea around the core questions:
   - who feels the pain now
   - what they do today instead
   - why the timing matters
   - what the narrowest useful wedge is
   - what should be observed before expanding scope
4. Reframe the idea in plain language around the real user outcome.
5. Recommend the next move:
   - stop
   - narrow the idea
   - continue into `plan-ceo-review`
   - continue into `plan-eng-review`
6. If the user wants a saved planning artifact, write or update a concise doc in `docs/`.

## Guardrails

- Do not jump to architecture before the problem framing is good enough.
- Do not over-answer with generic startup advice; stay grounded in the repo or idea context.
- Ask at most one concise question at a time.
- Do not start implementation unless the user explicitly pivots from planning to coding.

## Outputs

Always include:

- selected mode and why
- sharper problem framing
- current status quo
- narrowest wedge
- what to observe or validate next
- next 1-3 actions
