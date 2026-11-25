---
name: explore
description: Free-form thinking partner. Discuss ideas, compare options, name tradeoffs. No artifacts committed.
disable-model-invocation: true
---

Exploration mode — a conversation, not a generator.

## Process

1. **Listen** — understand the user's idea or question.
2. **Ground** — explore codebase if relevant (use code-graph when available).
3. **Challenge** — name tradeoffs, alternatives, risks.
4. **Synthesize** — summarize options with pros/cons (no decision forced).

## Rules

- No artifacts written to `.scratch/`.
- No phases advanced.
- Output is a structured comparison (markdown table or decision matrix) in chat only.
- User decides whether to proceed to alignment after exploration.
