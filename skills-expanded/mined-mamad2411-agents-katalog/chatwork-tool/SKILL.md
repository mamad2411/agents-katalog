---
name: chatwork-tool
description: >-
  Chatwork integration tool. Handles message send/receive, search, unreplied check, and room listing.
  Use when: Use when: sending messages in Chatwork, retrieving room lists, checking unreplied messages, searching chats, or handling mentions.
tags: [communication, chatwork, external]
---


# Chatwork Tool

An external tool for sending, receiving, searching, and managing Chatwork messages.

## How to Invoke

**Bash**: Run with `animaworks-tool chatwork <サブコマンド> [引数]`. See the syntax below.

## Action List

### send — Send a message
```bash
animaworks-tool chatwork send ROOM MESSAGE
```

### messages — Retrieve messages
```bash
animaworks-tool chatwork messages ROOM [-n 20]
```

### search — Search messages
```bash
animaworks-tool chatwork search KEYWORD [-r ROOM] [-n 50]
```

### unreplied — Check unreplied messages
```bash
animaworks-tool chatwork unreplied [--json]
```
- `include_toall` (optional, default: false): Whether to include messages addressed to everyone

### rooms — List rooms
```bash
animaworks-tool chatwork rooms
```

### mentions — Retrieve mentions
```bash
animaworks-tool chatwork mentions [--json]
```
- `include_toall` (optional, default: false): Whether to include messages addressed to everyone

### delete — Delete a message (own messages only)
```bash
animaworks-tool chatwork delete ROOM MESSAGE_ID
```

### sync — Synchronize messages (cache update)
```bash
animaworks-tool chatwork sync [ROOM]
```

## CLI Usage

```bash
animaworks-tool chatwork send ROOM MESSAGE
animaworks-tool chatwork messages ROOM [-n 20]
animaworks-tool chatwork search KEYWORD [-r ROOM] [-n 50]
animaworks-tool chatwork unreplied [--json]
animaworks-tool chatwork rooms
animaworks-tool chatwork mentions [--json]
animaworks-tool chatwork delete ROOM MESSAGE_ID
animaworks-tool chatwork sync [ROOM]
animaworks-tool chatwork <サブコマンド> ... --as <identity>
```

## Notes

- Operates with a personal token `CHATWORK_API_TOKEN__<自分の名前>`. Not available if unregistered
- `--as <identity>` is available only when delegated via `chatwork_tool.grants`. With read delegation, write operations (such as send/delete) are not allowed
- Rooms can be specified by room name or room ID
