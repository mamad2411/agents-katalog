---
name: crabchat-start
version: 0.0.1
description: |
  Start the WeChat gateway. Use when the user asks to start, launch, or run
  the WeChat bot or gateway.
allowed-tools:
  - Bash
---

# crabchat start

Start the WeChat gateway service.

```bash
crabtalk-wechat start
```

On first run, this displays a QR code in the terminal — the user must scan it
with WeChat on their phone to authenticate. After that the gateway bridges
WeChat messages to the Crabtalk daemon.
