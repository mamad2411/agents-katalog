---
name: cursor-habits
description: >-
  use this when starting a Cursor session, after a bad run you want
  to rewind, or before changing CLI permissions — /rewind, /summarize,
  /config
license: MIT
metadata:
  portability: cursor
---
# cursor-habits

Cursor instance of **session-hygiene** — read that skill first for the
portable doctrine. This skill is only Cursor CLI mechanics.

Sources: [cursor.com/docs/cli/reference/slash-commands](https://cursor.com/docs/cli/reference/slash-commands),
[cursor.com/docs/cli/reference/configuration](https://cursor.com/docs/cli/reference/configuration).

## When
- Starting a Cursor Agent CLI session.
- After a bad run — `/rewind` or `/clear`.
- Before changing what the agent may run — `/config` and the permissions lists.

## Session checks
No official `/context` on the published CLI slash list.
- `/summarize` (`/compress` alias) — shrink the conversation.

## Rewind options (escalating)
1. **Cancel mid-run** — stop the current turn.
2. **`/rewind`** — jump back to a previous message (enable the `rewind` flag in
   `cli-config.json` if it is off).
3. **`/clear`** (`/new`, `/new-chat`, `/newchat`) — start a new chat.
4. **`/fork`** — copy this chat into a new session.
5. **`git` recovery** — last resort.

## Slash commands worth knowing
- `/model` — pick the model.
- `/plan` — Plan mode.
- `/ask` — read-only Ask mode.
- `/config` — interactive CLI settings.
- `/sandbox` — sandbox and network access.
- `/resume` — open recent chats.

## Settings backup
Back up `~/.cursor/cli-config.json` (Windows: `%USERPROFILE%\.cursor\cli-config.json`)
and the project `.cursor/cli.json` before labs that reset harness config.
Permissions live under `permissions.allow` / `permissions.deny` in those files.
Skills live in `.cursor/skills/` and `~/.cursor/skills/`.

## Related
session-hygiene
