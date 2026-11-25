---
name: memory
description: "Scoped semantic memory management via `memory.*` tools. Use when saving, searching, listing, deleting, or promoting durable facts in local chat memory or profile-global memory."
requires_env:
---

# Memory

Use this skill when the task is about durable semantic memory rather than raw transcript history.

Available tools:

- `memory.search`
- `memory.digest`
- `memory.list`
- `memory.upsert`
- `memory.delete`
- `memory.promote`

## Mental Model

AFKBOT memory has three layers:

1. session memory: short-lived replay and compaction
2. chat memory: durable facts local to one chat/thread/user scope
3. profile-global memory: reusable facts shared across chats of one profile

Do not treat those layers as interchangeable.

## Rules

1. Search before writing.
Use `memory.search` in the current local scope first so you do not create duplicate facts.

2. Prefer local chat scope by default.
If the fact belongs only to the current Telegram/Telethon dialog, keep it local.

3. Promote only reusable facts.
Use `memory.promote` only when the fact should intentionally become profile-global.

4. Use deterministic keys.
Choose stable `memory_key` values so later updates replace the same fact instead of creating drift.

5. Never store secrets.
Do not store tokens, passwords, session strings, codes, or raw credentials in memory.

6. Do not cross-search other chats automatically.
Only use another chat scope when the operator explicitly asks for selectors or `binding_id`.

7. Use `memory.digest` for operator summaries.
If the user wants a compact scoped recap, prefer `memory.digest` over manually stitching `memory.list` output.
