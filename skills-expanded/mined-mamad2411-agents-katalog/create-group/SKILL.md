---
name: create-group
description: "Use when user wants to create a new Telegram group, supergroup, or channel, optionally inviting members on creation."
allowed-tools: Bash, Read, Grep, Glob
---

# Create Telegram Group/Channel

Create groups, supergroups, or channels and optionally invite users.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Create supergroup (default)
bun "$SCRIPT" create-group "My Group" --about "Group description"

# Create with initial members
bun "$SCRIPT" create-group "Project Chat" --users @user1 @user2

# Create broadcast channel
bun "$SCRIPT" create-group "Announcements" --type channel --about "Updates"

# Create legacy group (limited to ~200 members)
bun "$SCRIPT" create-group "Small Team" --type group --users @teammate
EOF
```

## Parameters

| Parameter | Type   | Description                                |
| --------- | ------ | ------------------------------------------ |
| title     | string | Group/channel name                         |
| `--type`  | choice | `supergroup` (default), `channel`, `group` |
| `--about` | string | Description text                           |
| `--users` | list   | Users to invite (usernames or IDs)         |

## Group Types

| Type         | Members   | Messaging             | Use Case          |
| ------------ | --------- | --------------------- | ----------------- |
| `group`      | ~200 max  | Two-way               | Small teams       |
| `supergroup` | 200K max  | Two-way + admin tools | Large communities |
| `channel`    | Unlimited | One-way (admins only) | Broadcasts        |

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
