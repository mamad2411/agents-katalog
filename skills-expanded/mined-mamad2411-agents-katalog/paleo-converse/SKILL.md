---
name: paleo-converse
description: 'Use when user says "compress conversation", "condense chat", "summarize history", "too long context", or a session has many old turns. Condense prior conversation turns into a tight summary, merge near-duplicate messages, keep the last N turns verbatim. Saves context tokens without losing task state. Off: "stop condensing" / "keep full history".'
version: 2.4.1
license: MIT
metadata:
  hermes:
    tags: [tokens, context, conversation, compression, dedup]
    related_skills: [paleo, paleo-trim-context]
---

# paleo-converse
Conversation compression. Shrink old turns, keep recent verbatim.

## Rules
- Merge consecutive near-duplicate messages (same ask re-phrased) into one.
- Condense turns older than the last N (default 6) into a tight summary: goals, decisions, open questions, key values.
- Keep the last N turns verbatim — do not rewrite the user's most recent intent.
- Preserve: file paths, commands, IDs, code snippets, error strings, decisions.
- Drop: chit-chat, repeated confirmations, "ok great thanks", filler.
- Never summarize away the current task or a pending question.

## Levels
- `lite`: merge duplicates only, keep all turns.
- `full` (default): merge + condense turns older than N.
- `ultra`: condense everything older than the last 3 turns.

## Switch
- `paleo-converse` / `condense chat` on. `stop condensing` / `keep full history` off.
- `paleo-converse N=8` sets the retained verbatim window.

## Gotchas
- Don't compress the turn you're acting on — only history.
- If the user references "what we said earlier" ambiguously, keep a bit more context.
- High-stakes (legal/spec/config review): keep exact quotes.
