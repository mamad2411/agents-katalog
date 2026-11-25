---
name: codex-habits
description: >-
  use this when starting a Codex session, after a bad run you want
  to rewind, or before changing approvals — /status, /compact,
  /permissions, /skills
license: MIT
metadata:
  portability: codex
---
# codex-habits

Codex instance of **session-hygiene** — read that skill first for the
portable doctrine. This skill is only Codex mechanics.

Sources: [developers.openai.com/codex/cli/slash-commands](https://developers.openai.com/codex/cli/slash-commands),
[developers.openai.com/codex/ide/slash-commands](https://developers.openai.com/codex/ide/slash-commands),
[developers.openai.com/codex/app/commands](https://developers.openai.com/codex/app/commands).

## When
- Starting a Codex CLI, IDE, or app thread.
- After a bad run — `/compact`, `/new`, or `/resume`.
- Before changing what the agent may run — `/permissions`.

## Session checks
- `/status` — thread ID, **context usage**, rate limits, model, approval mode.

## Rewind options (escalating)
1. Cancel the in-flight turn.
2. **`/compact`** — summarize earlier turns to free context.
3. **`/new`** — fresh conversation. **`/clear`** — clear transcript (CLI). **`/resume`** — saved session picker. **`/fork`** — copy the thread.
4. **`git` recovery** — last resort. Git is the ground truth.

There is no `/rewind` slash on Codex. Do not invent one.

## Slash commands worth knowing
- `/model` — pick the model.
- `/permissions` — approval preset (Auto, Read Only, custom).
- `/skills` — browse and attach a local skill. App composer also uses `$` to invoke a skill.
- `/init` — write an `AGENTS.md` scaffold.
- `/mcp` — connected servers.
- `/review` — review uncommitted changes.

## Skills and settings
Project: `.codex/skills/`, `.agents/skills/`.
User: `~/.codex/skills/`, `~/.agents/skills/`.
Config: `config.toml` (Codex home). Features such as `/goal` need `[features] goals = true` or `codex features enable goals`.

## Related
session-hygiene
