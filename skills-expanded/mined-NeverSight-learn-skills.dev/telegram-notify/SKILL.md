---
name: telegram-notify
description: Send a one-way Telegram message to configured contacts. Use when the user asks to send a message, notify, ping, or alert via Telegram. Also use when you need to proactively notify the user about something (e.g. a long task completing). This skill is send-only and does NOT wait for or receive a reply — if you need an answer or decision back from the user, use the telegram-ask skill instead.
metadata:
  author: roziscoding
  version: "1.0.0"
---

# Telegram Notify

Send messages via a Telegram bot. This skill is fire-and-forget and **one-way only** — it sends and moves on. It does not wait for, read, or return any response from the user.

> **Need an answer back?** This skill cannot receive replies. If you need the user to confirm, decide, or provide input before continuing, use the **`telegram-ask`** skill instead — it blocks until the user answers (via a button or a reply) and prints the answer to stdout.

## Setup

Create `~/.config/telegram-skills/credentials.json`:

```json
{
  "bot_token": "your-bot-token-from-botfather",
  "default_chat_id": "your-chat-id",
  "contacts": {
    "alice": "123456",
    "bob": "789012"
  }
}
```

## Usage

The binary is at `<skill-dir>/../telegram-skills-bin/bin/telegram`. It reads message text from stdin.

> **Requires the `telegram-skills-bin` skill.** The binary lives in that sibling skill. If `<skill-dir>/../telegram-skills-bin/bin/telegram` does not exist, tell the user to install it (`bunx skills add roziscoding/telegram-skills`) instead of failing with a raw error.

```bash
# Send to default recipient
echo "Deploy complete" | <skill-dir>/../telegram-skills-bin/bin/telegram

# Send to a specific chat ID
echo "Hello" | <skill-dir>/../telegram-skills-bin/bin/telegram -c 123456

# Send to multiple recipients
echo "Hello" | <skill-dir>/../telegram-skills-bin/bin/telegram -c 111 -c 222

# Send to a named contact
echo "Hello" | <skill-dir>/../telegram-skills-bin/bin/telegram --to alice

# Send to multiple named contacts
echo "Hello" | <skill-dir>/../telegram-skills-bin/bin/telegram --to alice --to bob

# Multiline with heredoc
<skill-dir>/../telegram-skills-bin/bin/telegram <<'EOF'
*Build complete*
- 42 tests passed
- Deployed to staging
EOF
```

Usage: `<bin> [-c chat_id ...] [--to name ...]` — reads message from stdin. Use `-c` for raw chat IDs or `--to` for named contacts from credentials. Both are repeatable. Defaults to `default_chat_id` from credentials if neither is given.

## Formatting

- Messages support Markdown parse mode
- Keep messages concise and useful
- When notifying about task completion, include a brief summary of what was done
- Use backticks for code snippets
