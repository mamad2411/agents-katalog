---
name: crabchat
version: 0.0.1
description: |
  WeChat gateway for Crabtalk. Use when the user asks to interact with WeChat,
  send messages, start/stop the gateway, or check logs.
allowed-tools:
  - Bash
  - Read
  - Edit
---

# crabchat — WeChat Gateway CLI

Manage the Crabtalk WeChat gateway and send messages.

## Commands

| Command | Description |
|---------|-------------|
| `crabchat start` | Start the WeChat gateway service |
| `crabchat stop` | Stop the running gateway |
| `crabchat logs` | Show gateway logs |
| `crabchat send "message"` | Send a message to the configured WeChat user |

## Install

```bash
curl -sSf https://raw.githubusercontent.com/crabtalk/wechat-skill/main/setup | sh
```

## Configuration

Config file: `~/.config/crabtalk/gateway.toml`

```toml
[wechat]
token = "..."
base_url = "https://ilinkai.weixin.qq.com"
to_user_id = "user@im.wechat"
context_token = ""
```
