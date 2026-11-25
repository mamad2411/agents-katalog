---
name: context-scope-tags
description: "Context-scoping protocol using explicit tags to prevent context bleed in chat (especially Telegram). Use when the user asks to isolate a topic, scope the assistant to a specific project/topic, request a /ctx or /context_def cheat sheet, or mentions tags like [Isolated Context], [ISO], [SCOPE], [GLOBAL], [NOMEM], [REM]."
---

# Context Scope Tags (Chat Protocol)

## Tag parsing rules

- Tags must appear **at the start** of the user's message (one per line or chained).
- Prefer short tags, but accept long-form equivalents.
- Tags **do not override** safety policies, tool policies, or access controls.

## Supported tags

### Isolation / scope

- `\[ISO: <topic>\]` or `\[Isolated Context: <topic>\]`
  - Treat as a **fresh topic**.
  - Do **not** pull in other conversation/project context unless the user explicitly re-provides it.
  - Allowed implicit carry-over: universal safety rules + a few stable user prefs (timezone, “don’t overwrite configs”, etc.).

- `\[SCOPE: <topic>\]` or `\[Scoped Context: <topic>\]`
  - Restrict reasoning to the named scope.
  - If missing details inside the scope, ask clarifying questions.

- `\[GLOBAL\]` or `\[Global Context OK\]`
  - Cross-topic reuse is allowed.
  - When reusing prior context, **call out what you reused**.

### Memory intent

- `\[NOMEM\]` or `\[No Memory\]`
  - Do not store durable/long-term memories from this exchange.

- `\[REM\]` or `\[Remember\]`
  - If the message contains a preference/decision/setting, store it as a short durable memory.

## Default behavior (no tags)

- Be conservative about cross-topic mixing.
- If the user complains about context mixing, suggest using the tags above.

## Command-style cheat sheet responses

When the user sends `/ctx` or `/context_def`, respond with a short, copy/pasteable cheat sheet:

- Tags + one-line meaning
- 2 examples:
  - `\[ISO: token-currency\]\[NOMEM\] write a manifesto`
  - `\[SCOPE: openclaw-mem\] implement feature flag wiring`

## Telegram note (optional)

Telegram slash commands cannot contain dashes.
Use `/context_def` (underscore), not `/context-def`.
