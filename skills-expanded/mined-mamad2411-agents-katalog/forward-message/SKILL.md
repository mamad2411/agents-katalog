---
name: forward-message
description: "Use when user wants to forward, relay, or copy Telegram messages from one chat to another, supporting both single and batch forwarding."
allowed-tools: Bash, Read, Grep, Glob
---

# Forward Telegram Messages

Forward one or multiple messages between chats.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Forward single message
bun "$SCRIPT" forward <from_chat> <message_id> <to_chat>

# Forward multiple messages (comma-separated IDs)
bun "$SCRIPT" forward 2124832490 471920,471921 90417581

# Get message IDs first with read command
bun "$SCRIPT" read <chat> -n 5
EOF
```

## Workflow

1. Use `read` to find message IDs: `read <chat> -n 10`
2. Forward by ID: `forward <from> <id> <to>`

## Parameters

| Parameter   | Type       | Description                    |
| ----------- | ---------- | ------------------------------ |
| from_chat   | string/int | Source chat                    |
| message_ids | string     | Message ID(s), comma-separated |
| to_chat     | string/int | Destination chat               |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
