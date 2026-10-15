---
name: telegram-ask
description: Ask a question via Telegram with inline buttons and wait for the user's response — either a button press or a free-text reply to the message. Use when you need user confirmation, input, or a decision before proceeding (e.g. "deploy to prod?", "which option?").
metadata:
  author: roziscoding
  version: "1.0.0"
---

# Telegram Ask

Ask questions via Telegram with inline keyboard buttons. The script blocks until the user answers — either by pressing a button **or** by replying directly to the question message — and prints the answer to stdout.

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

The binary is at `<skill-dir>/../telegram-skills-bin/bin/telegram`. It reads the question from stdin. Use `--choice` to define the buttons.

> **Requires the `telegram-skills-bin` skill.** The binary lives in that sibling skill. If `<skill-dir>/../telegram-skills-bin/bin/telegram` does not exist, tell the user to install it (`bunx skills add roziscoding/telegram-skills`) instead of failing with a raw error.

```bash
# Yes/No question
ANSWER=$(echo "Deploy to production?" | <skill-dir>/../telegram-skills-bin/bin/telegram --choice "Yes" --choice "No")
echo "User chose: $ANSWER"

# Multiple options
ANSWER=$(echo "Which environment?" | <skill-dir>/../telegram-skills-bin/bin/telegram --choice "staging" --choice "production" --choice "cancel")

# Ask a specific person by chat ID
ANSWER=$(echo "Approve release?" | <skill-dir>/../telegram-skills-bin/bin/telegram -c 123456 --choice "Approve" --choice "Reject")

# Ask a named contact
ANSWER=$(echo "Approve release?" | <skill-dir>/../telegram-skills-bin/bin/telegram --to alice --choice "Approve" --choice "Reject")
```

Usage: `<bin> [-c chat_id ...] [--to name ...] --choice "Option" [--choice "Option" ...]` — reads question from stdin. The script blocks until the user answers, then prints the answer to stdout. The user can either press a button (the chosen option's text is printed) or send a Telegram reply to the question message (the reply text is printed). Either way the original message is edited to show the answer and the buttons are removed.

## Notes

- Always provide at least two `--choice` options
- The script blocks — use it when you need the answer before continuing
- The user can answer by pressing a button **or** by replying to the question message; a text reply is printed to stdout verbatim, so the answer is not limited to the predefined options
- The message is updated after the answer to show what was chosen (button) or "answered by reply" with the reply text; the buttons are removed
- Text replies must be sent as a Telegram **reply** to the question message; non-text replies (stickers, photos with no caption) are ignored and the script keeps waiting
- Supports Markdown formatting in the question text
