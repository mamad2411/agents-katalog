---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
---

Spin up a **background agent** to do the research, so you keep working while it reads.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it where the repo already keeps such notes; match the existing convention, and if there is none, put it somewhere sensible and say where.

## Purpose
Delegate high-trust research to a background agent and save cited findings as Markdown in the repo.

## When NOT to use
- Quick factual lookups that need no document.
- Opinion or secondary-source summaries.

## Inputs
The question, repo conventions for notes.

## Edge cases and failure handling
- Only secondary sources available -> say so and mark confidence lower.
- Sources disagree -> list each with citation; do not merge silently.

## Validation
- Every claim has a primary-source citation; file saved in the conventional location; path reported.

## Output requirements
Path to the Markdown findings file and a 3-line summary.

## Example
```text
"How does Stripe handle idempotency?" -> background agent reads official docs/API reference -> writes docs/notes/stripe-idempotency.md with cited claims.
```

## Related skills
research (parent), paper-lookup, deep-research

## When to use
The user wants a topic researched or docs/API facts gathered by a background agent.
