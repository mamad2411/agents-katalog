---
name: canary
description: Generate a curl-based canary watcher script for a deployed URL. Validates URL is http/https, status code is 100-599, interval is 5-86400 seconds. The generated script supports one-shot (default) and --watch (continuous loop) modes. Wire into cron or a CI scheduled job. Run as `node ~/.claude/skills/dragoon/skills/canary/scripts/canary.js <url>`.
version: 1.0.0
---

# /canary

Lightweight uptime watcher.

## When to use

- After deploying, to watch the new release
- Before a major event, as a heartbeat
- The user says "set up a watcher", "monitor X URL"

## What it produces

`scripts/canary.sh` that uses curl. zero install. supports:

```
bash scripts/canary.sh           # one-shot, exits 0/1
bash scripts/canary.sh --watch   # continuous loop
```

## Run it

```
dragoon canary https://example.com --apply
dragoon canary https://example.com --status 204 --interval 30 --apply
```
