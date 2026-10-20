---
name: discord-webhook-send
description: Send messages to Discord channels via webhook with embed support
---

# Discord Webhook Sender

Send messages to Discord channels via webhook with embed support

## When to Use

- User wants to discord send
- User wants to send discord
- Keywords: discord, webhook, message, chat

## Required Parameters

- **webhook_url** (string): Discord webhook URL
- **content** (string): Message content

## Output

- **sent** (boolean): Message sent successfully
- **message_id** (string): Discord message ID

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: discord.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `build` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
