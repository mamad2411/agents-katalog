---
name: bullybuddy
description: BullyBuddy - Control Claude Code sessions. Commands: status, list, spawn, send, output, kill, audit, transcript.
metadata: { "openclaw": { "emoji": "🦞", "always": true } }
---

# BullyBuddy

Control BullyBuddy Claude Code session manager via `/bullybuddy` or `/skill bullybuddy`.

## Usage

Run the script with the subcommand:

```bash
{baseDir}/scripts/bb.sh <command> [args...]
```

Environment variables `BB_URL` and `BB_TOKEN` must be set.

## Commands

| Command | Description |
|---------|-------------|
| `help` | Show help |
| `status` | Server status |
| `list` | List sessions |
| `spawn [cwd] [task]` | Create session |
| `send <id> <text>` | Send input |
| `output <id>` | Show output |
| `kill <id>` | Kill session |
| `audit [n]` | Audit log |
| `transcript <id>` | Transcript |

## Examples

```
/bullybuddy status
/bullybuddy list
/bullybuddy spawn ~/project "Fix bug"
/bullybuddy send abc123 yes
/bullybuddy kill abc123
```
