---
name: coding-agent
description: Delegate bounded coding work to an installed coding-agent CLI with explicit scope and verification.
category: development
aliases:
- codex
- claude-code
- headless-agent
- ai-coding
- autopilot
triggers:
- Run the coding agent
- Use Codex
- Use Claude Code
- Spin up an agent to fix this
- Hand this off to an agent
keywords:
- codex
- claude
- code
- agent
- headless
- cli
- autonomous
- coding
- ai
dependencies:
- optional:codex-or-claude-cli
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- coding-agent
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
- claude
- code
- codex
- coding
- development
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

# Coding Agent

## Purpose
Launch, monitor, and inspect a headless coding agent (Codex CLI, Claude Code, OpenCode,
or Pi) as a managed background process. The skill turns "do this fix in another
process" into a single call with deterministic start, streaming output, and clean
shutdown.

## When to Use
- The user wants a non-interactive coding task run by an AI agent
- A long-running refactor or test run should happen in the background
- A second model should attempt a task in parallel
- The user wants logs, status, or a diff pulled from an agent process

## When NOT to Use
- The task needs human-in-the-loop review per step (use a foreground agent)
- The user has no API key or local credentials for any supported agent
- The action is destructive on a protected branch (require explicit confirmation)

## Capabilities
- Launch a supported coding agent CLI with a prompt, model, and workspace
- Stream stdout/stderr to a log file and optionally back to chat
- Detect idle, finished, and errored states
- Apply or reject the agent's proposed diff
- Restart from the last good checkpoint on failure
- Reuse a running tmux/screen session for manual takeover

## Inputs
- `agent` (one of `codex`, `claude`, `opencode`, `pi`)
- `prompt` (string or path to prompt file)
- `model` (optional, agent default if omitted)
- `cwd` (working directory)
- `timeout` (default 30 min)
- `apply_changes` (boolean, default false — always require review)

## Workflow
1. **Validate inputs** — agent name, prompt non-empty, cwd exists, API key set.
2. **Start the agent** in a background process, redirecting output to a log.
3. **Heartbeat every 30 s** — print elapsed time and last 5 log lines.
4. **On timeout**: terminate the process, summarize progress, leave the diff staged.
5. **On finish**: show a short diff summary; wait for user to `apply` or `discard`.
6. **On error**: capture the failure, suggest a smaller prompt retry.

## Tools
- Process control (`start-process`, `kill`, `wait`)
- Optional: `tmux`/`screen` for session reuse
- Log file in `<cwd>/.agent-logs/<agent>-<ts>.log`

## Examples
**User:** "Have Codex fix the failing test in `tests/test_parser.py`."
**Response:** Codex started in `/repo`, model `gpt-5`. Heartbeat at 30 s. Will
report when idle and stage the patch.

**User:** "Run Claude Code on this prompt in another process."
**Response:** Claude Code started. Logs at `.agent-logs/claude-2026-02-09T10-15.log`.
Use `tail -f` to watch, or wait for the finish summary.

## Safety
- Never auto-apply agent diffs to protected branches
- Always require explicit `apply` or `discard`
- Cap a single run at 30 min by default; require an override to extend
- Redact secrets in any streamed output

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
