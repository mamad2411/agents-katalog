---
name: codecast
description: Stream coding agent sessions (Claude Code, Codex, Gemini CLI, etc.) to a Discord channel in real-time via webhook. Use when invoking coding agents and wanting transparent, observable dev sessions — no black box. Parses Claude Code's stream-json output into clean formatted Discord messages showing tool calls, file writes, bash commands, and results with zero AI token burn. Use when asked to "stream to Discord", "relay agent output", or "make dev sessions visible".
---

# Codecast

Live-stream coding agent sessions to Discord. No black box — see every tool call, file write, and bash command as it happens. Zero AI tokens burned.

## How It Works

```
┌──────────┐  stream-json  ┌──────────────┐  platform  ┌──────────┐
│ Claude   │ ────────────→ │ parse-stream │ ────────→ │ Discord  │
│ Code -p  │               │ .py          │           │ #channel │
└──────────┘               └──────────────┘           └──────────┘
```

- Claude Code runs in `-p` (print) mode with `--output-format stream-json --verbose`
- `parse-stream.py` reads JSON lines, posts formatted messages via a platform adapter
- Platform adapters (currently Discord) handle message delivery and threading
- `unbuffer` (from `expect`) provides PTY to prevent stdout buffering
- Non-Claude agents fall back to ANSI-stripped raw output relay
- Rate limiting (25 posts/60s) with automatic batching prevents webhook throttling

## First-Time Setup

Run these steps once after installing the skill:

### 1. Make scripts executable

```bash
chmod +x <skill-dir>/scripts/dev-relay.sh <skill-dir>/scripts/parse-stream.py
```

### 2. Create a Discord webhook

Create a webhook in the target Discord channel via the Discord API or Server Settings → Integrations → Webhooks.

To create via API (if the bot has MANAGE_WEBHOOKS):
```bash
curl -s -X POST "https://discord.com/api/v10/channels/<CHANNEL_ID>/webhooks" \
  -H "Authorization: Bot <BOT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Codecast"}'
```

Store the webhook URL:
```bash
echo "https://discord.com/api/webhooks/<ID>/<TOKEN>" > <skill-dir>/scripts/.webhook-url
chmod 600 <skill-dir>/scripts/.webhook-url
```

### 3. Skip the permissions prompt (Claude Code only)

Create `~/.claude/settings.json` if it doesn't exist:
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": ["*"]
  }
}
```

### 4. Install unbuffer (required)

```bash
brew install expect    # macOS
apt install expect     # Linux
```

## Invocation

After installing, run `chmod +x` on the scripts once:
```bash
chmod +x <skill-dir>/scripts/dev-relay.sh <skill-dir>/scripts/parse-stream.py
```

### From OpenClaw (recommended)

```bash
exec background:true command:"<skill-dir>/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build a REST API for todos'"
```

### Direct

```bash
bash <skill-dir>/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build auth module'
```

### Options

| Flag | Description | Default |
|------|------------|---------|
| `-w <dir>` | Working directory | Current dir |
| `-t <sec>` | Timeout | 1800 (30min) |
| `-h <sec>` | Hang threshold | 120 |
| `-i <sec>` | Post interval | 10 |
| `-n <name>` | Agent display name | Auto-detected |
| `-P <platform>` | Chat platform | discord |
| `--thread` | Post into a Discord thread | Off |
| `--skip-reads` | Hide Read tool events | Off |
| `--resume <dir>` | Replay session from relay dir | — |

### Thread Mode

Post all messages into a single Discord thread for cleaner channel history:
```bash
bash <skill-dir>/scripts/dev-relay.sh --thread -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Refactor auth'
```

### Session Resume

Replay a previous session's events (e.g., to a different channel or after a webhook change):
```bash
bash <skill-dir>/scripts/dev-relay.sh --resume /tmp/dev-relay.XXXXXX
```

The relay dir path is printed at session start (`📂 Relay: /tmp/dev-relay.XXXXXX`).

## What Discord Sees

For Claude Code (stream-json mode):
- ⚙️ Model info and permission mode
- 📝 File writes with line count and smart content preview
- ✏️ File edits
- 🖥️ Bash commands
- 📤 Bash command output (truncated to 800 chars)
- 👁️ File reads (hide with `--skip-reads`)
- 🔍 Web searches
- 💬 Assistant messages
- ✅/❌ Completion summary with turns, duration, cost, and session stats

For other agents (raw mode):
- Output in code blocks with ANSI stripping
- Hang detection warnings
- Completion/error status

### End Summary

Every session ends with a summary block showing:
- Files created and edited (with counts)
- Bash commands run
- Tool usage breakdown
- Total cost

## Architecture

```
scripts/
├── dev-relay.sh          # Shell entry point, flag parsing, process management
├── parse-stream.py       # JSON stream parser, rate limiter, event loop
├── .webhook-url          # Discord webhook URL (gitignored)
└── platforms/
    ├── __init__.py       # Platform adapter loader
    └── discord.py        # Discord webhook + thread support
```

## Agent Support

| Agent | Output Mode | Status |
|-------|------------|--------|
| Claude Code | stream-json (parsed) | Full support |
| Codex | Raw ANSI | Basic support |
| Gemini CLI | Raw ANSI | Basic support |
| Any CLI | Raw ANSI | Basic support |

## Interactive Input

During an active session, forward input to the agent:
- From OpenClaw: `process:submit sessionId:<id> data:"your message"`
- Session info stored at `/tmp/dev-relay-session.json`

## Completion Notification

On finish, the relay calls `openclaw gateway wake` to notify OpenClaw immediately.
