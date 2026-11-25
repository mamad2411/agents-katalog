---
name: crabchat-send
version: 0.0.1
description: |
  Send a message via WeChat. Use when the user asks to send, message, notify,
  or communicate with someone on WeChat.
allowed-tools:
  - Bash
---

# crabchat send

Send a text message to the configured WeChat user.

```bash
crabchat "your message here"
```

Requires `to_user_id` to be set in `~/.config/crabtalk/gateway.toml` under
the `[wechat]` section. The gateway does NOT need to be running — this command
hits the ilink API directly.
