---
name: find-user
description: "Use when user wants to find, look up, or resolve a Telegram user by username, phone number, or ID, or get someone's Telegram profile info."
allowed-tools: Bash, Read, Grep, Glob
---

# Find Telegram User

Resolve usernames, phone numbers, or IDs to full user/chat profile information.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# By username
bun "$SCRIPT" find-user @username

# By user ID
bun "$SCRIPT" find-user 2124832490

# By phone (must be in contacts)
bun "$SCRIPT" find-user +15559876543

# Works for groups/channels too
bun "$SCRIPT" find-user @channelname
EOF
```

## Output

Returns JSON with profile information:

```json
{
  "type": "User",
  "id": 2124832490,
  "first_name": "Name",
  "last_name": null,
  "username": "username",
  "phone": "1234567890",
  "bot": false
}
```

For groups/channels:

```json
{
  "type": "Channel",
  "id": 1234567890,
  "title": "Group Name",
  "username": "groupname",
  "participants_count": 42
}
```

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
