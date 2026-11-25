---
name: hermes-for-agents
description: "A concise guide for other AI agents (Claude Code, Codex, etc.) on how to use, control, and interact with Hermes Agent — CLI, config, skills, cron, gateway, delegation, and memory."
author: minimx
---

# Hermes Agent — Quick Guide for Other AI Agents

You are running alongside Hermes Agent on this machine. This guide teaches any AI agent (Claude Code, Codex, etc.) how Hermes works and how to use it.

## What Hermes Is

Hermes Agent is an open-source AI agent framework by Nous Research. It provides:
- **Full toolkit**: file, terminal, web, browser, messaging
- **Persistent memory** across sessions
- **Skills**: reusable knowledge that loads every session
- **Cron jobs**: scheduled unattended tasks
- **Multi-platform gateway**: Telegram, Discord, WeChat, iMessage, etc.
- **Profiles**: isolated instances with separate configs

This instance runs under **profile: default** on macOS Sequoia.

## Key Paths

| What | Where |
|------|-------|
| Config | `~/.hermes/config.yaml` |
| Secrets | `~/.hermes/.env` |
| Skills | `~/.hermes/skills/` |
| Session DB | `~/.hermes/state.db` |
| Logs | `~/.hermes/logs/gateway.log` |
| Cron output | `~/.hermes/cron/output/` |
| Profiles | `~/.hermes/profiles/<name>/` |
| Source code | `~/.hermes/hermes-agent/` |

## CLI Cheatsheet

Spawn Hermes from your terminal or delegate to it:

```bash
hermes                          # Interactive
hermes chat -q "query"          # One-shot
hermes chat -q "query" -Q       # Quiet mode, no banner
hermes -s skill1,skill2         # Preload skills
hermes --continue               # Resume last session
hermes config set key value     # Set config value
hermes doctor                   # Health check
hermes skills list              # List installed skills
hermes cron list                # List cron jobs
hermes cron create "0 9 * * *"  # Create job
hermes cron run <id>            # Trigger now
hermes gateway status           # Platform connections
hermes profile list             # List profiles
hermes mcp list                 # List MCP servers
hermes sessions list            # Past sessions
```

## Subagent Spawning

Use `delegate_task(goal, context, toolsets)` to spawn subagents. Up to 3 parallel. Each gets isolated context + terminal.

For durable background Hermes instances:
```bash
tmux new-session -d -s agent1 'hermes'
tmux send-keys -t agent1 'Build X' Enter
tmux capture-pane -t agent1 -p
```

## Cron Key Params

```python
cronjob(action="create", schedule="30m", prompt="...", deliver="origin")
```

- `schedule`: `"30m"`, `"every 2h"`, `"0 9 * * *"`, ISO timestamp
- `deliver`: `"origin"` (current chat), `"local"` (save file), `"all"` (all platforms)
- `no_agent=True`: script IS the job, no LLM cost, stdout delivered
- `script`: path to pre-run script (stdout = prompt context)
- `workdir`: run from project dir (loads its AGENTS.md)
- 3-minute hard timeout

## Memory

Two stores: `memory` (agent notes) and `user` (user profile). Save durable facts only — no task progress or temporary state.

## Toolset Reference

| Toolset | Use For |
|---------|---------|
| terminal | Shell, process mgmt |
| file | Read/write/search/patch |
| web | Search + extract |
| browser | Page automation |
| delegation | Subagent spawn |
| cronjob | Scheduled tasks |
| memory | Cross-session facts |
| session_search | Past convos |
| vision | Image analysis |
| skills | Manage skills |
| messaging | Cross-platform send |
| todo | Task tracking |
| clarify | Ask user questions |

Enable/disable per platform via `hermes tools`, takes effect on `/reset`.

## Machine Conventions

- **Security**: API keys/env vars only. Never hardcode secrets.
- **Git**: github.com/mrtsels
- **Python**: 3.11.15, prefer `uv`. PEP 668 enforced.
- **Proxy**: Shadowrocket port 1082
- **WeChat**: Primary channel. API rate limited (~3/min).
