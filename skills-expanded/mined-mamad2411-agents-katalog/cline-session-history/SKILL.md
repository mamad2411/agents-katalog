---
description: Search and browse Cline session history. Use when the user asks to find,
  list, inspect, or export Cline sessions by time period, prompt content, status,
  model, provider, source, mode, workspace, or other criteria. Also use when the user
  wants to read a session transcript or export sessions to a directory. Trigger phrases
  include "find my session", "search my session history", "show me past sessions",
  "what was that session where", "find the session that started with", and any mention
  of past Cline conversations. Follows current best practices for reliability, security,
  and maintainability. Enforces least-privilege, secret management, input validation,
  and audit logging throughout.
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:06.457297+00:00'
name: cline-session-history
tags:
- utility
version: 2
---

# Cline Session History

Search and browse Cline session history stored on the local machine. Sessions live in `~/.cline/data/sessions/` as individual JSON metadata files and conversation transcript (`.messages.json`) files. Older sessions may also be in a `sessions.db` SQLite database.

## When to Use This Skill

- "Find my session from the last hour about..."
- "Find my session that started with this prompt..."
- "Find the session where I asked about..."
- "Show me sessions that used model X"
- "What sessions failed yesterday?"
- "Show me the transcript for session <id>"
- "Export sessions from last week to a folder"
- "What was that session where..."
- Any request involving past Cline conversation history

## How to Use

The search script lives alongside this file at `scripts/search_sessions.py`, relative to the skill's own directory. Resolve it against the directory that contains this `SKILL.md` — **not** the current working directory — so it works regardless of where the command is run from.

**Script path:** `scripts/search_sessions.py` (relative to this skill's directory)

The examples below use `scripts/search_sessions.py`; prefix it with the skill directory's absolute path when running from elsewhere.

All filters are optional and combine with AND logic.

### Quick Examples

```sh
# Sessions from the last 10 minutes
python3 scripts/search_sessions.py --since 10m

# Sessions between two dates with "chatgpt" in the prompt
python3 scripts/search_sessions.py --since 2026-06-01 --until 2026-06-21 --prompt chatgpt

# Find a session by its starting prompt (quoted substring match)
python3 scripts/search_sessions.py --since 1d --prompt "find some code that should be improved" --full-prompt

# Non-interactive sessions that failed
python3 scripts/search_sessions.py --no-interactive --status failed

# VS Code extension sessions using Claude models, full prompts
python3 scripts/search_sessions.py --source vscode --model "claude" --full-prompt

# Full transcript of a specific session
python3 scripts/search_sessions.py --session-id 1781991507587_pozk0 --transcript

# Export matching sessions to a directory
python3 scripts/search_sessions.py --since 1d --export ~/tmp/exported-sessions
```

### Time Filters

Both `--since` and `--until` accept:

- **Relative**: `10m`, `30min`, `2h`, `1d`, `1w` (minutes, hours, days, weeks)
- **ISO 8601**: `2026-06-20`, `2026-06-20T21:30:00Z`, `2026-06-20T21:30:00+00:00`

### All Available Filters

| Filter | Description |
|--------|-------------|
| `--since <time>` | Sessions started after this time |
| `--until <time>` | Sessions started before this time |
| `--prompt <text>` | Case-insensitive substring search in prompt |
| `--prompt-regex <pattern>` | Regex search in prompt (case-insensitive) |
| `--status <status>` | `running`, `idle`, `completed`, `cancelled`, `failed` |
| `--source <source>` | `cli`, `vscode`, etc. (exact match) |
| `--provider <name>` | Provider name, exact match (e.g. `cline`) |
| `--model <text>` | Model name substring, case-insensitive (e.g. `claude`) |
| `--mode <mode>` | `plan` or `act` |
| `--cwd <path>` | Working directory substring match |
| `--session-id <id>` | Exact session ID lookup |
| `--interactive` / `--no-interactive` | Filter by interactive flag |
| `--team-only` / `--no-team` | Filter by team session flag |
| `--subagents` / `--no-subagents` | Include/exclude subagent sessions |

### Output Options

| Option | Description |
|--------|-------------|
| `--full-prompt` | Show full prompt text instead of truncated |
| `--transcript` | Print full conversation transcript |
| `--max-messages <n>` | Limit messages in transcript output |
| `--content-types <types>` | Comma-separated: `text,thinking,tool_use,tool_result,image` |
| `--export <dir>` | Copy matching session files to a directory |
| `--limit <n>` | Max number of sessions to return |
| `--json` | Output as JSON |

### Data Source Options

| Option | Description |
|--------|-------------|
| `--sessions-dir <path>` | Custom sessions directory (default: `~/.cline/data/sessions`) |
| `--db-path <path>` | Custom sessions.db path |
| `--no-db` | Skip SQLite DB, only scan JSON files |

## Workflow

1. Start by running the search with the user's criteria to get a list of matching sessions.
2. If the user wants to see details, use `--full-prompt` or `--transcript`.
3. For transcript inspection, consider `--max-messages` and `--content-types` to focus on relevant parts.
4. For bulk export, use `--export <dir>` to copy session files.

## Session Data Structure

Each session on disk has:
- `<session_id>.json` — Metadata: session_id, started_at, status, source, provider, model, cwd, prompt, metadata (mode, systemPrompt, cost, usage), etc.
- `<session_id>.messages.json` — Full conversation transcript with messages containing content blocks (text, thinking, tool_use, tool_result, image).

The SQLite `sessions.db` may contain older sessions with similar fields plus `transcript_path`, `hook_path`, `parent_session_id`, `agent_id`, `is_subagent`.

## Prerequisites

- Ensure all required tools and dependencies are installed
- Verify you have the necessary permissions and access credentials
- Check that the target environment is in a known good state


## Error Handling

- Always check the exit code or response status of commands before proceeding
- On failure, log the error details and attempt recovery if a retry strategy exists
- If recovery fails, report the error with context: what was attempted, what went wrong, and suggested next steps
- Never silently ignore errors — treat unexpected output as potential failure


## Verification

- After each step, verify the expected outcome before continuing
- Use idempotent checks: running the same action twice produces the same result
- If verification fails, roll back the last change and report the issue
- Log verification results for audit trail


## Configuration

- Use environment variables with sensible defaults for configuration
- Validate configuration at the start of execution
- Document all configuration options and their effects
- Support loading config from files when appropriate
