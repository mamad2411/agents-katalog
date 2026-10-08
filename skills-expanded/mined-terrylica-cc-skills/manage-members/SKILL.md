---
name: manage-members
description: user wants to manage Telegram group or channel members, including inviting users, kicking or banning someone, listing members, or filtering.
allowed-tools: Bash, Read, Grep, Glob
---

# Manage Telegram Members

Invite, kick, and list members in groups and channels.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Invite users
bun "$SCRIPT" invite <group> @user1 @user2

# Kick a user
bun "$SCRIPT" kick <group> @username

# List all members
bun "$SCRIPT" members <group>

# List admins only
bun "$SCRIPT" members <group> --admins

# Search members by name
bun "$SCRIPT" members <group> --search "Terry"
EOF
```

## Subcommands

### invite

| Parameter | Type       | Description                |
| --------- | ---------- | -------------------------- |
| group     | string/int | Group/channel              |
| users     | list       | Usernames or IDs to invite |

### kick

| Parameter | Type       | Description            |
| --------- | ---------- | ---------------------- |
| group     | string/int | Group/channel          |
| user      | string     | Username or ID to kick |

### members

| Parameter    | Type       | Description                |
| ------------ | ---------- | -------------------------- |
| group        | string/int | Group/channel              |
| `--search`   | string     | Filter by name/username    |
| `--admins`   | flag       | Show admins only           |
| `-n/--limit` | int        | Max members (default: 200) |

## Output Format

```
First Last @username (id: 12345) [admin]
```

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
