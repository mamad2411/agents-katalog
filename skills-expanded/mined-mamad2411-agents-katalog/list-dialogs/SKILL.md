---
name: list-dialogs
description: user wants to list all Telegram chats, groups, and channels, see their contacts, find a chat ID, browse conversations, or check account info via.
allowed-tools: Bash, Read, Grep, Glob
---

# List Telegram Dialogs

List all chats, groups, and channels visible to your personal Telegram account.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Preflight

1. Session must exist: `~/.local/share/gramjs/<profile>.session`
   - If missing, run `/tlg:setup` first

## Usage

```bash
/usr/bin/env bash << 'DIALOGS_EOF'
ROOT="$(cc-plugin-root tlg)"
SCRIPT="$ROOT/scripts/tg-cli.ts"

# Default profile
bun "$SCRIPT" dialogs

# Specific profile
bun "$SCRIPT" -p missterryli dialogs

# Filter results
bun "$SCRIPT" dialogs | grep -i "search term"
DIALOGS_EOF
```

## Additional Commands

### Read Messages

`read` returns the **full text** of every message by default. Multi-line
bodies are indented under the header so the message stays visually
grouped. No truncation.

```bash
# Full text (default — recommended)
bun "$SCRIPT" read <chat_id> -n 10

# Short scan listing — truncate each body to N chars (\n flattened to "⏎")
bun "$SCRIPT" read <chat_id> -n 50 --preview 200
```

Use `--preview N` only when you're scanning many messages and want a
single-line summary per row. For routine reading, omit it — long messages
deserve to be read in full, not silently cut at 200 chars (the prior default,
which forced repeated manual workarounds when content mattered).

### Account Info

```bash
bun "$SCRIPT" whoami
```

## Output Format

```
Chat Name                                  (id: 1234567890)
```

Use the `id` value with `send-message` skill to send to that chat.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If tg-cli.ts's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
