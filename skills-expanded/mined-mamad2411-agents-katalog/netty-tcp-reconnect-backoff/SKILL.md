---
tags: [backend, netty, tcp, reconnect, backoff]
name: netty-tcp-reconnect-backoff
description: On Netty `channelInactive`/EOF/read-timeout, reconnect with exponential backoff (100ms → 30s cap), reset on success, keep SO_KEEPALIVE + TCP_NODELAY
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - long-lived TCP client to a device or broker that drops silently
  - need to survive peer restarts without crashing the collector
---

# Netty TCP Reconnect with Backoff

See `content.md`.
