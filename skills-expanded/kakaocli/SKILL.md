---
name: kakaocli
description: Send and receive KakaoTalk messages via CLI
version: 0.5.0
requires:
  binaries:
    - kakaocli
  platform: darwin
tags:
  - messaging
  - kakaotalk
  - korea
---

# KakaoTalk CLI Skill

Read and send KakaoTalk messages from the command line. Requires macOS with KakaoTalk desktop app installed. Auto-launches and auto-logs in when credentials are stored.

## Setup (Required First Time)

```bash
# Store credentials for auto-login
kakaocli login --email user@example.com --password yourpassword
```

## Available Commands

### Check Status
```bash
kakaocli login --status
```

### List Chats
```bash
kakaocli chats --json
```

### Read Messages
```bash
kakaocli messages --chat "Name" --since 1h --json
```

### Send Message
```bash
kakaocli send "Name" "Your message here"
```

### Send to Self-Chat (Testing)
```bash
kakaocli send x --me "Test message"
```

### Watch for New Messages
```bash
kakaocli sync --follow
```

### Search Messages
```bash
kakaocli search "keyword" --json
```

### Harvest Chat Names & History
```bash
# Capture display names for all chats
kakaocli harvest

# Full harvest with scroll + history loading
kakaocli harvest --scroll --top 20
```

## Usage Guidelines

- Always confirm before sending messages to others
- Use `--me` flag and `--dry-run` for testing
- Rate limit: max 1 message per 2 seconds
- Don't send messages between 11 PM and 7 AM unless urgent
- KakaoTalk is auto-launched and auto-logged-in when credentials are stored
- First-time setup requires `kakaocli login --email ... --password ...`
