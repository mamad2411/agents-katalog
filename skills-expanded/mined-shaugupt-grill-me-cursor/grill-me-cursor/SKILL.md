---
name: grill-me-cursor
description: Interview the user relentlessly about a plan or design using Cursor's batched multiple-choice question tool. Use when the user wants to stress-test a plan, get grilled on their design, or mentions "grill me" inside Cursor.
---

Cursor-flavored variant of the `grill-me` skill. Same goal — interview the user relentlessly about every aspect of a plan until you reach shared understanding, walking down each branch of the design tree and resolving dependencies between decisions — but optimized for Cursor's `AskQuestion` tool so you spend fewer round-trips and tokens.

## Core behavior

- Walk the design tree depth-first-ish: resolve foundational decisions before dependent ones.
- For every question, include your recommended answer. Mark it in the option label (e.g. append `(recommended)`) and give a one-line rationale either in the question prompt or in a short message accompanying the `AskQuestion` call.
- If a question can be answered by exploring the codebase, explore the codebase instead of asking.
- Keep going until the plan is fully resolved or the user tells you to stop. Don't stop after the first batch.

## Batching with `AskQuestion`

Default to asking ~5 questions per round via a single `AskQuestion` call.

Rules for batching:
- Only batch questions that are roughly independent — i.e. the answer to one doesn't change whether another question is still meaningful.
- If later questions depend on earlier answers, split the dependent ones into the next batch.
- It's fine to ask fewer than 5 (or even 1) when the tree narrows to a single tightly-coupled decision. Don't pad batches with filler.
- It's fine to ask more than 5 when many sibling decisions are genuinely independent (e.g. picking defaults for several unrelated config knobs).

`AskQuestion` constraints to respect:
- Each question needs ≥2 options. If the real answer space is open-ended (numbers, names, free text), either:
  - Offer representative buckets plus an `Other — I'll type it` option, then read the user's follow-up message, or
  - Skip `AskQuestion` for that question and ask in plain text.
- Use `allow_multiple: true` only when the decision is genuinely multi-select (e.g. "which of these platforms should we support?"). Default to single-select.
- Give each question a stable, unique `id` so you can map answers back unambiguously.
- Keep option labels short and decision-shaped ("Postgres", "SQLite", "DynamoDB"), not essay-shaped.

## Question quality

Each question should:
- Target a concrete decision, not open-ended brainstorming.
- Surface the trade-off in the prompt (one short sentence is enough).
- Include the recommended option clearly marked.
- Avoid leading the user — if you genuinely don't have a recommendation, say so and present the options neutrally.

## Loop

1. Read / explore enough context to know the next ~5 independent open decisions.
2. Send one `AskQuestion` call with those questions.
3. When answers come back, briefly acknowledge, note any follow-up implications, and update your mental model of the plan.
4. Identify the next batch (now possibly unlocked by the previous answers) and repeat.
5. When the tree is resolved, summarize the final agreed-upon plan in plain text so the user has a single artifact to review.

## Fallback

If `AskQuestion` isn't available in the current session for any reason, degrade to the original `grill-me` behavior: ask one question at a time in plain text, still with a recommended answer.
