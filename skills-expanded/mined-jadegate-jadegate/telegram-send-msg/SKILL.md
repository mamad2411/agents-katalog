---
name: telegram-send-msg
description: Send a message via Telegram Bot API
---

# Telegram Send Message

Send a message via Telegram Bot API

## When to Use

- User wants to telegram send
- User wants to send telegram
- Keywords: telegram, message, bot, chat

## Required Parameters

- **bot_token** (string): Telegram bot token
- **chat_id** (string): Target chat ID
- **text** (string): Message text

## Output

- **message_id** (number): Sent message ID
- **success** (boolean): Send success

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: api.telegram.org
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `encode` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
