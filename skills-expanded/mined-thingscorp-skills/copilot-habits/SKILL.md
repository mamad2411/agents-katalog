---
name: copilot-habits
description: >-
  use this when starting a Copilot CLI session, after a bad run you want
  to rewind, or before changing permissions — /context, /compact,
  /undo, /permissions
license: MIT
metadata:
  portability: copilot
---
# copilot-habits

Copilot instance of **session-hygiene** — read that skill first for the
portable doctrine. This skill is only Copilot CLI mechanics.

Sources: [docs.github.com Copilot CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference),
[docs.github.com Copilot CLI skills](https://docs.github.com/copilot/how-tos/copilot-cli/customize-copilot/create-skills).

## When
- Starting a Copilot CLI session — check `/context` early.
- After a bad run — `/undo` or `/clear`.
- Before changing what the agent may run — `/permissions`.

## Session checks
- `/context` — context-window usage (system prompt, tools, messages, free space).
- `/usage` — session stats and token totals.

## Rewind options (escalating)
1. **Cancel mid-run** — stop the current turn.
2. **`/undo`** (`/rewind` alias) — rewind picker; conversation only, or conversation + files.
3. **`/compact`** — summarize history to free context.
4. **`/clear`** (`/new`) — start a new conversation.
5. **`git` recovery** — last resort.

## Slash commands worth knowing
- `/model` — pick the model.
- `/skills list` — available skills. `/skills info` — one skill's path.
- `/skills` — enable or disable a skill. `/skills add` — extra skills directory.
- `/skills reload` — pick up skills added this session.
- `/settings` (`/config` alias) — user settings dialog.
- `/permissions` — mode (`default`, `assisted`, `allow-all`, `show`).
  `/allow-all` and `/yolo` alias `/permissions allow-all`.
- `/sandbox` — local sandbox.
- `/resume` — previous session.

## Settings backup
Back up `~/.copilot/settings.json` (override dir with `COPILOT_HOME`)
and the repo `.github/copilot/settings.json` before labs that reset
harness config. `~/.copilot/config.json` is the legacy settings location
(migrated to `settings.json` on startup) — do not edit settings there.

## Related
session-hygiene
