---
name: cursor-agent
description: Use Cursor Agent safely for bounded software tasks without unattended destructive actions.
category: development
aliases:
- cursor
- cursor-cli
- ai-ide
- agent
triggers:
- Use Cursor
- Run the Cursor agent
- Hand this to Cursor
- Cursor CLI
keywords:
- cursor
- cli
- agent
- ide
- tmux
- code
- ai
- automation
dependencies:
- optional:cursor-agent
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- cursor-agent
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- agent
- cli
- cursor
- development
- ide
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Cursor Agent

## Purpose
Drive the **Cursor CLI agent** (`agent`, formerly `cursor-agent`) from a non-interactive
shell, using tmux so the same session can be inspected, taken over, or detached. The
skill wraps prompt construction, model selection, and result capture in a single
operation that any other skill or tool can call.

## When to Use
- A coding task is best handled by Cursor's agent loop
- A long task should run in a tmux session the user can attach to
- Results should land in a file or be returned to the calling skill

## When NOT to Use
- The user wants Cursor's editor UI, not the CLI
- The task requires a different agent (route to `coding-agent`)
- No API key is set for Cursor

## Capabilities
- Construct a Cursor CLI command from prompt + flags
- Run it inside a named tmux session (`cursor-<ts>`)
- Capture the final output block and write it to a result file
- Stream progress into a log file
- Allow user takeover via `tmux attach -t <name>`
- Apply or reject the proposed diff with `apply` / `discard`

## Inputs
- `prompt` (string or path)
- `model` (e.g. `gpt-5`, `claude-3.7-sonnet`, `composer-1`) — default Cursor default
- `cwd` — default `$PWD`
- `timeout` — default 30 min
- `attach` — boolean, default false (run detached)

## Workflow
1. **Validate** that the `agent` (or `cursor-agent`) binary is on PATH.
2. **Build the command** with `--print`, `--model`, `--output text`, and the prompt.
3. **Open a tmux session** named `cursor-<unix-ts>`.
4. **Send the command** to the session; redirect output to `.cursor-logs/<ts>.log`.
5. **Heartbeat every 30 s** with elapsed time and last 5 log lines.
6. **On exit**: extract the final assistant message and write to `.cursor-logs/<ts>.out`.
7. **Report** session name, log path, output path, and diff summary.

## Tools
- `tmux` (required)
- `agent` / `cursor-agent` (required)
- `rg` / `grep` for log scrubbing

## Examples
**User:** "Run Cursor on this prompt."
**Response:** Started tmux session `cursor-1739097600`. Logs at
`.cursor-logs/1739097600.log`. Will report when done. Use
`tmux attach -t cursor-1739097600` to take over.

**User:** "Hand off this refactor."
**Response:** Cursor agent running, model `composer-1`, cwd `/repo`. ETA: <5 min.

## Safety
- Never apply a Cursor-proposed diff to a protected branch
- Redact `.env`, `*.pem`, and `id_rsa` from the working dir before launch
- Cap runs at 30 min; require `--no-cap` to extend
- Surface session name and `attach` command in every status

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
