---
name: delete-messages
description: "Use when user wants to delete, remove, or unsend Telegram messages from a chat, either for everyone or just for themselves."
allowed-tools: Bash, Read, Grep, Glob
---

# Delete Telegram Messages

Delete one or multiple messages from a chat. By default deletes for everyone.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Delete for everyone (default)
bun "$SCRIPT" delete <chat> <message_id>

# Delete multiple messages
bun "$SCRIPT" delete <chat> 12345,12346,12347

# Delete only for yourself
bun "$SCRIPT" delete <chat> <message_id> --self-only

# Find message IDs first
bun "$SCRIPT" read <chat> -n 10
EOF
```

## Parameters

| Parameter     | Type       | Description                                      |
| ------------- | ---------- | ------------------------------------------------ |
| chat          | string/int | Chat containing messages                         |
| message_ids   | string     | Message ID(s), comma-separated                   |
| `--self-only` | flag       | Delete only for yourself (default: for everyone) |

## Workflow

1. Use `read <chat> -n N` to find message IDs
2. Delete by ID: `delete <chat> <ids>`

## Anti-Patterns

- **Cannot delete others' messages** in private chats after 48 hours
- **Admin required** to delete others' messages in groups

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
