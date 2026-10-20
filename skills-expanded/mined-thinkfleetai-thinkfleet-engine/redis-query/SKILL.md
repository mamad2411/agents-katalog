---
name: redis-query
description: "Execute Redis commands using redis-cli."
metadata: {"thinkfleetbot":{"emoji":"🔴","requires":{"bins":["redis-cli"]}}}
---

# Redis Query

Execute Redis commands via `redis-cli`.

## Environment Variables

- `REDIS_URL` - Redis connection URL (e.g. `redis://user:pass@host:6379/0`)

## Basic commands

```bash
redis-cli -u "$REDIS_URL" PING
```

```bash
redis-cli -u "$REDIS_URL" GET mykey
```

```bash
redis-cli -u "$REDIS_URL" SET mykey "hello" EX 3600
```

## Scan keys (safe for production)

```bash
redis-cli -u "$REDIS_URL" --scan --pattern "session:*" | head -20
```

## Hash operations

```bash
redis-cli -u "$REDIS_URL" HGETALL user:123
```

## Server info

```bash
redis-cli -u "$REDIS_URL" INFO server | head -20
```

## Notes

- Avoid `KEYS *` on large databases; use `SCAN` instead.
- Confirm before running `FLUSHDB`, `FLUSHALL`, or `DEL` on multiple keys.
