---
name: paleo-trim-context
description: 'Use when context window is large / token cost high / long session. Proactively trim, summarize, or drop stale content to save context tokens without losing the task state.'
version: 2.4.1
license: MIT
metadata:
  hermes:
    tags: [tokens, context, trim, summarize, efficiency]
    related_skills: [paleo, paleo-converse]
---

# paleo-trim-context
Keep context small. Drop stale, keep task state.

## Rules
- Summarize old tool output into 1-2 lines; keep only the result that matters.
- Drop: resolved errors, obsolete file reads, duplicate logs.
- Keep: current plan, open TODO, key IDs/paths, last decision.
- Use session_search / notes for history instead of re-pasting.
- Prefer code/script over long prose explanations in context.
- Pre-thinking compression (biggest savings): BEFORE the model reasons, compress retrieved docs / RAG context / long file dumps into key facts + a source pointer. Drop full-doc dumps.
- Effort pinning: trivial task -> signal low effort, no over-think. Reuse a prior conclusion instead of re-reasoning the same thing.

## Scope boundary (don't collide with siblings)
- Context hygiene + effort pinning + pre-thinking compression = THIS skill (runs automatically during the session).
- `paleo-converse` = explicit conversation-turn compression + dedup (on-demand, when the user points at history or context is heavy).
- `paleo-summary` = one bulky artifact (log / diff / dump / stdout) -> tight intisari.
- Hand off to those when the target is a specific turn-block or a single artifact; don't re-implement them here.

## When
- Long session (>20 turns), big file dumps, repeated similar output.
- Before calling an expensive model — shrink first.

## Gotchas
- Don't trim the user's latest instruction.
- Keep ground truth (file paths, IDs) — summarize derivations only.
- If unsure what's stale, ask once. Don't guess-drop critical state.
