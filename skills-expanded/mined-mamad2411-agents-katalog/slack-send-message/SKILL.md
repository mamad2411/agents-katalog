---
name: slack-send-message
description: Send messages to Slack channels via webhook or API with formatting support
---

# Slack Message Sender

Send messages to Slack channels via webhook or API with formatting support

## When to Use

- User wants to slack send
- User wants to send slack
- Keywords: slack, message, chat, notification

## Required Parameters

- **webhook_url** (string): Slack webhook URL
- **text** (string): Message text

## Output

- **sent** (boolean): Whether message was sent
- **status_code** (number): HTTP response code

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: hooks.slack.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `build_payload` -> 5 steps -> Exit: `ret_ok`, `ret_fail`
