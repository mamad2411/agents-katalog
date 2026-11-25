---
name: save-session-log
description: Keep conversation records and decision traces. Use when setting up transcript hooks, when the user asks where a decision came from, or when a host has no hook support.
---

# Save session log

Conversations are records. Decisions from them belong in the state tables.

## With hooks

Run `python .agents/tools/ws.py hooks enable <host>` once per tool.
The hooks copy each transcript to `docs/chats/<host>/<session>.md` and list it in `docs/chats/INDEX.md`.
Nothing else is needed during the session.

## Without hooks

Do not retype the conversation. Record its results instead:

| From the conversation | Record with |
| --- | --- |
| A decision | `ws add decision --set source="user 2026-10-31: <short quote>"` |
| A requirement change | `ws add` or `ws set` with `--source "user 2026-10-31"` |
| An open question | `ws add question` |
| A preference | `ws add preference` |

The source field keeps a short original quote in the user's language. That is enough to trace a
fact back to the conversation. A credential in the quote follows the project's credential rule.

`ws start` imports Kimi, Codex and Kiro sessions on its own. Cursor and Antigravity sessions are
imported with `ws chats import cursor` or `ws chats import antigravity`.

## Reconcile

After transcripts are copied, `ws reconcile` lists each user message that no row accounts for.
Read each one. If it holds a requirement, decision or preference that is not recorded, record it
first. Then mark it with the IDs, or with a reason such as `chat: thanks` or `question: status`.
Do this before the final checkpoint of a session.

## Rules

- Never store hidden reasoning or private host data. The capture redacts common English and Chinese forms
  of credentials, such as `password: ...` and `密码：...`, not every secret. It does so also under
  `"credentials": "plain"`, which keeps credentials as written only in the files the user named.
- A transcript does not override the state files.
- The machine-readable copy in `docs/chats/*/raw/` contains redacted visible turns and stays out of version
  control. When the host supplies no recipient receipt, record delivery as unknown.
