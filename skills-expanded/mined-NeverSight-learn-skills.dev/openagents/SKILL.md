---
name: openagents
description: |
  Multi-agent workflow orchestration hub for AI coding agents.
  Shows agent status, repo health, available commands, and next steps.
  Use when the user types "openagents" or wants to check
  the multi-agent setup health. Status check detects which agents are
  installed, verifies skills and rules symlinks, and reports
  ecosystem health. Use `openagents-doctor` for repairs.
allowed-tools: Read Write Glob Grep Bash(test:*) Bash(echo:*)
  Bash(pwd:*) Bash(ls:*) Bash(find:*)
version: 1.12.0
author: Luis Bovo <luis@luis.dev>
license: MIT
user-invocable: true
tags: [openagents, multi-agent, orchestration, hub]
---

# openagents

Multi-agent workflow orchestration hub. Run `openagents` for the
default status workflow.

## Status check

Detect agent → verify skill and rules symlinks → report ecosystem health.

Read [references/status.md](references/status.md) for the full workflow.

## Available commands

| Invocation | Installed as | Action |
|------------|-------------|--------|
| `openagents` | openagents | Show agent status, repo health, next steps |
| `openagents-global` | openagents-global | Agent detection + handshake + symlinks |
| `openagents-init` | openagents-init | Scaffold AGENTS.md + .agents/rules/ |
| `openagents-add` | openagents-add | Create and register new skills or rules |
| `openagents-rules` | openagents-rules | Deep codebase analysis -> generate rules |
| `openagents-rm` | openagents-rm | Remove project artifacts (rules, skill, all) |
| `openagents-doctor` | openagents-doctor | Diagnose and repair broken setup |
| `openagents-info` | openagents-info | Show version, agents, distribution channels |
| `openagents-upgrade` | openagents-upgrade | Update openagents to latest version |
| `openagents-uninstall` | openagents-uninstall | Remove openagents skill globally |

## Invocation

Each subcommand is installed as an independent skill (`openagents-global`,
`openagents-init`, etc.). Invoke with hyphens:
- **opencode**: `skill({ name: "openagents-global" })` for `openagents-global`
- **claude-code**: `/openagents-global` (standalone) or `/openagents:openagents-global` (plugin)
- **cursor/zed**: `/openagents-global`

## Capability constraints

| Tool | Purpose | Scope |
|------|---------|-------|
| Read, Write, Glob, Grep | Read/write project and skill files | Local filesystem only |
| Bash(test:*) | Check file existence, env vars, agent detection | Read-only checks |
| Bash(echo:*) | Report status to user | No side effects |
| Bash(pwd:*) | Resolve project root | Read-only |
| Bash(ls:*) | List project files for analysis | Read-only |
| Bash(find:*) | Discover files for rule generation | Read-only |

The skill does NOT execute downloaded code, make network requests,
install packages, or fetch remote content. All operations are
local filesystem operations.

## Agent detection matrix

Multi-signal strategy: env vars -> config dirs -> binaries (first match wins).
<!-- Matrix sync: update both openagents/SKILL.md and openagents-global/SKILL.md when adding agents -->

| Agent | Env var / Config dir | Binary | Auto-discovers ~/.agents/ |
|-------|---------------------|--------|--------------------------|
| opencode | `OPENCODE_CALLER` / `~/.config/opencode/` | `opencode` | Yes |
| claude-code | `CLAUDE_CODE_SSE_PORT` / `~/.claude/` | `claude` | Yes |
| cursor | `CURSOR_TRACE_ID` / `~/.cursor/` | `cursor` | No (symlink) |
| codex | `CODEX_CONFIG_DIR` / `~/.codex/` | `codex` | Yes |
| cline | `CLINE_CONFIG_DIR` / `~/.clinerules` | `cline` | Yes |
| zed | `ZED_CONFIG_DIR` / `~/.zed/` | `zed` | No (symlink) |
| gemini-cli | `GEMINI_API_KEY` / `~/.gemini/` | `gemini` | Yes |
| antigravity | `~/.antigravity/` | `antigravity` | Yes |
| deepagents | `~/.deepagents/` | `deepagents` | Yes |
| github-copilot | -- | `github-copilot` | Varies |
| kimi-code-cli | `~/.kimi/` | `kimi` | Yes |
| mimocode | `~/.mimocode/` | `mimo` | Plugin |
| warp | `~/.warp/` | `warp` | Yes |
| amp | `~/.amp/` | `amp` | Yes |