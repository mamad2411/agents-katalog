---
name: claude-code-in-slack
description: Runs a local daemon connecting your machine to the Claude Code in Slack server.
  Receives tasks from Slack, drives Claude Code locally via @anthropic-ai/claude-agent-sdk,
  and streams results back. Use to set up credentials, start/stop the daemon, and check status.
  use when "claude-code-in-slack", "setup slack bridge","connect to slack", or any mention of managing the Claude Code in Slack daemon.
argument-hint: "setup | start | stop | status | logs [N]"
---

# Claude Code in Slack — Client Skill

You are managing the Claude Code in Slack client daemon.
User data and config are stored at `~/.claude-code-in-slack/`.

First, locate the skill directory by finding this SKILL.md file:

- Use Glob with pattern `**/skills/**/claude-code-in-slack/SKILL.md` to find its path, then derive the skill root directory from it.
- Store that path mentally as SKILL_DIR for all subsequent file references.

## Command parsing

Parse the user's intent from `$ARGUMENTS` into one of these subcommands:

| User says (examples)                | Subcommand |
| ----------------------------------- | ---------- |
| `setup`, `configure`, `init`        | setup      |
| `start`, `start daemon`, `connect`  | start      |
| `stop`, `stop daemon`, `disconnect` | stop       |
| `status`, `daemon status`           | status     |
| `logs`, `logs 100`, `show logs`     | logs       |

Extract optional numeric argument for `logs` (default 50).

## Config check (applies to `start`, `stop`, `status`, `logs`)

Before running any subcommand other than `setup`, check if `~/.claude-code-in-slack/config.env` exists:

- **If it does NOT exist:**
  - In Claude Code: tell the user "No configuration found" and automatically start the `setup` wizard using AskUserQuestion.
  - In other environments: tell the user "No configuration found. Please run `/claude-code-in-slack setup` first." and stop.
- **If it exists:** proceed with the requested subcommand.

## Subcommands

### `setup`

Read the setup guide from `SKILL_DIR/references/setup.md` and follow its instructions exactly.

### `start`

**Pre-check:** Verify `~/.claude-code-in-slack/config.env` exists (see "Config check" above). Do NOT proceed without it.

Run: `bash "SKILL_DIR/scripts/daemon.sh" start`

Show the output to the user. If it fails, tell the user:

- Check recent logs: `/claude-code-in-slack logs`
- Re-run setup if config is invalid: `/claude-code-in-slack setup`

### `stop`

Run: `bash "SKILL_DIR/scripts/daemon.sh" stop`

Show the output to the user.

### `status`

Run: `bash "SKILL_DIR/scripts/daemon.sh" status`

Show the output to the user.

### `logs`

Extract optional line count N from arguments (default 50).
Run: `bash "SKILL_DIR/scripts/daemon.sh" logs N`

## Notes

- Always mask the TOKEN value in output (show only first 4 and last 4 characters if you must display it)
- **Never start the daemon without a valid config.env** — always check first, redirect to setup
- The daemon runs as a background process (node or bun); its PID is stored at `~/.claude-code-in-slack/runtime/daemon.pid`
- Logs are at `~/.claude-code-in-slack/logs/daemon.log`
- Config persists at `~/.claude-code-in-slack/config.env` — survives across sessions
