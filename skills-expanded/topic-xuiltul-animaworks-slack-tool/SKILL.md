---
name: slack-tool
description: >-
  Slack integration tool. It handles message sending and receiving, search, checking unreplied messages, channel list, and emoji reactions.
  Use when: Use when: you need to post to Slack, view the channel list, reply in threads, check unreplied messages, or add reactions.
tags: [communication, slack, external]
---


# Slack Tool

An external tool for sending, receiving, searching, and reacting to Slack messages.

## How to Invoke

**Bash**: Run with `animaworks-tool slack <サブコマンド> [引数]`

## Action List

### send — Send a message
```bash
animaworks-tool slack send CHANNEL MESSAGE [--thread TS]
```

### messages — Retrieve messages
```bash
animaworks-tool slack messages CHANNEL [-n 20]
```

### search — Search messages
```bash
animaworks-tool slack search KEYWORD [-c CHANNEL] [-n 50]
```

### unreplied — Check unreplied messages
```bash
animaworks-tool slack unreplied [--json]
```

### channels — List channels
```bash
animaworks-tool slack channels
```

### react — Add an emoji reaction
- `emoji`: Slack emoji name (without colons. e.g., `thumbsup`, `eyes`, `white_check_mark`)
- `message_ts`: Timestamp of the message to react to (can be obtained from the `messages` action result)
- **Note**: The `react` action is not supported via CLI. Use it via MCP.

## CLI Usage

```bash
animaworks-tool slack send CHANNEL MESSAGE [--thread TS]
animaworks-tool slack messages CHANNEL [-n 20]
animaworks-tool slack search KEYWORD [-c CHANNEL] [-n 50]
animaworks-tool slack unreplied [--json]
animaworks-tool slack channels
```

## Notes

- The Slack Bot Token must be pre-configured in credentials
- Channels are specified by name with # or by channel ID
- The `reactions:write` scope is required for reactions
