---
name: gemini-cli-habits
description: >-
  use this when starting a Gemini CLI session, after a bad run you want
  to rewind, or before changing settings — /stats, /rewind, /skills,
  /settings
license: MIT
metadata:
  portability: gemini-cli
---
# gemini-cli-habits

Gemini CLI instance of **session-hygiene** — read that skill first for the
portable doctrine. This skill is only Gemini CLI mechanics.

Sources: [geminicli.com/docs/cli/commands](https://geminicli.com/docs/cli/commands/),
[geminicli.com/docs/cli/rewind](https://geminicli.com/docs/cli/rewind/),
[geminicli.com/docs/cli/skills](https://geminicli.com/docs/cli/skills/).

Google replaced the unpaid Gemini CLI with Antigravity CLI on 2026-06-18 for some
tiers. Commands below are from current Gemini CLI docs. Do not copy them onto
Antigravity without checking that product's reference.

## When
- Starting a Gemini CLI REPL.
- After a bad run — `/rewind` or Esc Esc.
- Before changing what the agent may run — `/settings` / `/permissions`.

## Session checks
- `/stats` (`/stats session`) — token usage, cache savings, session duration.

## Rewind options (escalating)
1. Cancel the in-flight turn.
2. **`/rewind`** (Esc Esc) — pick a prior turn; rewind chat, revert files, or both.
3. **`/restore [tool_call_id]`** — revert files from one tool call (checkpointing on).
4. **`/resume`** — session browser. **`/compress`** — shrink chat context.
5. **`git` recovery** — last resort. Git is the ground truth.

## Slash commands worth knowing
- `/skills list` / `enable` / `disable` / `reload`.
- `/settings` — edit `.gemini/settings.json`.
- `/model` — pick the model.
- `/mcp` — servers. `/tools` — tool list.
- `/init` — write `GEMINI.md`.
- `/memory reload` — reread context files.

## Skills and settings
Project: `.gemini/skills/`, `.agents/skills/`.
User: `~/.gemini/skills/`, `~/.agents/skills/`.
Settings: `~/.gemini/settings.json` or `/settings`.
Custom slash commands: `~/.gemini/commands/` or `.gemini/commands/` (`.toml`).

## Related
session-hygiene
