---
name: mark-read
description: user wants to mark Telegram chats as read, clear unread badges and mentions, dismiss notifications, or acknowledge messages to remove the unread.
allowed-tools: Bash, Read, Grep, Glob
---

# Mark Telegram Chat as Read

Mark all messages in a chat as read, clearing unread badges and mentions.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Mark a chat as read
bun "$SCRIPT" mark-read <chat_id_or_username>

# Examples
bun "$SCRIPT" mark-read 2124832490
bun "$SCRIPT" mark-read @username
EOF
```

## Parameters

| Parameter | Type       | Description          |
| --------- | ---------- | -------------------- |
| chat      | string/int | Chat to mark as read |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
