---
name: valkey-cache
description: "Cache data and manage state using Valkey (Redis-compatible) at {{VALKEY_HOST}}:{{VALKEY_PORT}}."
metadata:
  openclaw:
    emoji: "💎"
---

# Valkey Cache

Valkey is available at `{{VALKEY_HOST}}:{{VALKEY_PORT}}` within the Docker network. It is fully Redis-compatible.

## Basic Operations

```bash
# Set and get a value
valkey-cli -h {{VALKEY_HOST}} -p {{VALKEY_PORT}} SET mykey "myvalue"
valkey-cli -h {{VALKEY_HOST}} -p {{VALKEY_PORT}} GET mykey

# Set with expiration (60 seconds)
valkey-cli -h {{VALKEY_HOST}} -p {{VALKEY_PORT}} SET session:123 "data" EX 60
```

## Tips for AI Agents

- Drop-in replacement for Redis — use the same commands and client libraries.
- Ideal for caching, session storage, and pub/sub messaging.
