---
name: telegram-actions
description: Draft and perform user-approved Telegram actions without exposing bot credentials.
category: utilities
aliases:
- telegram
- bot
- message
- telegram-bot
triggers:
- Send a Telegram message
- Post to Telegram
- Telegram notification
- Message via Telegram
keywords:
- telegram
- bot
- message
- notify
- channel
- chat
dependencies:
- optional:TELEGRAM_BOT_TOKEN
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- telegram-actions
- utilities
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- actions
- bot
- message
- notify
- telegram
- utilities
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Telegram Actions

## Purpose
Draft and send messages through a Telegram bot without exposing bot tokens or
credentials. The skill ensures all Telegram actions are explicitly approved by
the user before execution.

## When to Use
- The user wants to send a message via Telegram
- Notification to a Telegram channel or group is needed
- Automated alerts should go to Telegram

## When NOT to Use
- Urgent emergency notifications (use multiple channels)
- Sensitive information without explicit user approval
- Automated bulk messaging without user review

## Capabilities
- Send text messages to chats
- Send photos, documents, and media
- Format messages with Markdown or HTML
- Reply to specific messages
- Get chat information
- List available chats

## Inputs
- `action` (required) — one of: send, list-chats, get-chat
- `chat_id` (required for send) — target chat ID or username
- `message` (required for send) — message text
- `parse_mode` (optional) — Markdown or HTML
- `reply_to` (optional) — message ID to reply to

## Workflow
1. **Draft** — Prepare message content for user review
2. **Confirm** — Wait for explicit approval
3. **Send** — Execute via Telegram Bot API
4. **Report** — Confirm delivery with message ID

## Tools
- Telegram Bot API (via secure HTTP calls)
- Bot token from environment (never exposed to user)

## Examples
**User:** "Send 'Deployment complete!' to #dev-alerts"
**Response:**
```
Draft:
Channel: #dev-alerts
Message: Deployment complete!

Say "confirm" to send, or edit the message.
```

## Safety
- NEVER expose bot tokens in responses
- Always show draft before sending
- Require explicit confirmation for every message
- Log all Telegram actions for audit trail
- Never send sensitive data without explicit approval

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical utilities category.
