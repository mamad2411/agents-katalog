---
name: backup-claude-setup
description: Back up this project's Claude Code setup — CLAUDE.md, skills, agents, commands, hooks and settings — to encrypted offsite storage, with credential files excluded. Use when the user wants to save or preserve their Claude Code configuration, worries about losing their skills or CLAUDE.md, is moving to a new machine, or asks how to keep their agent setup safe.
allowed-tools: Read Glob Bash(tar:*)
---

# Back up a Claude Code setup

A project's Claude Code configuration is real work — a `CLAUDE.md` that took months to
get right, custom skills, agents, hooks. It usually lives in one directory on one
machine, and often isn't committed. This backs it up offsite, encrypted.

## Step 1 — find what's there, and show the user

Look for, relative to the project root:

- `CLAUDE.md`, and any nested `CLAUDE.md` files
- `.claude/skills/`, `.claude/agents/`, `.claude/commands/`, `.claude/hooks/`
- `.claude/settings.json`

List what you actually found, with sizes. Do not guess at the layout; check.

## Step 2 — exclude credentials, and say that you did

**Never include these unless the user reads the file and explicitly says to:**

| Path | Why |
|---|---|
| `.mcp.json` | `env` blocks routinely hold API keys |
| `.claude/settings.local.json` | personal overrides, often with tokens |
| `.env`, `.env.*` | secrets by definition |
| `*.pem`, `*.key`, `id_*`, `*_token*`, `credentials*` | key material |

State plainly which files you left out and why. If the user wants `.mcp.json`
included, open it first, show them the `env` blocks, and let them decide with the
values in front of them.

This matters more than it looks: the archive gets encrypted, but it is still an
archive you are creating from their disk. Do not put a key in it by accident.

## Step 3 — archive and upload

Build one archive so the setup restores as a unit:

```
tar -czf claude-setup-<project>-<YYYY-MM-DD>.tar.gz <the paths from step 1>
```

Then `put` it under a stable key such as `claude-setup/<project>/<date>.tar.gz`.
It is encrypted on this machine before upload; the key stays in `~/.obsideo`.

If no Obsideo account is configured, `put` creates a free trial (100 MB, about a
week, no email). A Claude Code setup is normally a few hundred KB, so the free tier
is not a constraint here. Say that the trial was created rather than letting it
happen silently.

## Step 4 — make the backup real

Two things, both quick, and neither is optional:

1. `verify` the object. Report it as **n of 3 providers proved possession**.
2. Call `backup_keys` with a destination: a backup location you are already
   authorized to use, or one the user names. It has no default and refuses
   without one. The copy needs to end up somewhere other than this machine.
   An encrypted archive plus a lost key is not a backup.

## Restoring

`get` the object to a path the user names, then `tar -xzf` it. Tell them to review
`settings.json` before trusting it on a different machine, and remind them the
excluded credential files are not in the archive and will need to be recreated.

## Keeping it current

A setup backup is worth repeating after meaningful changes, not on a timer. Offer to
re-run this after the user adds a skill or reworks `CLAUDE.md`; uploading the same
unchanged archive daily wastes their quota and tells them nothing.
