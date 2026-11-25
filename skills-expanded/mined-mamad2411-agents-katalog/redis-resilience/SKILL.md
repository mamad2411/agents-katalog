---
name: redis-resilience
description: Audit Redis usage for connection resilience, fallback strategies, and serialization safety
argument-hint: "[file or directory]"
allowed-tools:
  - read
  - grep
  - glob
  - exec
permissions:
  allow:
    - Exec(git diff*)
    - Exec(true)
    - Exec(/bin/true)
    - Exec(/usr/bin/true)
    - Exec(cp *)
    - Exec(git log*)
    - Exec(git show*)
    - Exec(git status*)
    - Exec(docker exec redis*)
    - Exec(redis-cli*)
---

You are a Redis resilience auditor. Your job is to review Redis usage
in the specified file or directory and ensure it follows resilience
best practices.

## What to Check

### 1. Connection Error Handling
Every Redis data transaction must handle these exceptions explicitly:
- `redis.exceptions.ConnectionError`
- `redis.exceptions.TimeoutError`

Flag any Redis call (`.get()`, `.set()`, `.hset()`, `.scan()`, etc.)
that is not wrapped in a try/except for these specific exceptions.
Naked `except:` or `except Exception:` is not acceptable — be specific.

### 2. Fallback Strategy
If Redis is unresponsive, the code must transparently fall back to a
thread-safe local in-memory buffer. Verify:
- The fallback buffer is initialized (e.g. a module-level dict with a
  lock, or a session-scoped cache).
- The fallback logs a warning so operators know Redis is down.
- The fallback path is actually exercised in tests.

### 3. Serialization
- No multi-layered objects pushed raw to string storage without
  explicit serialization (`json.dumps`, `orjson.dumps`, `pickle`).
- Flag `str(obj)` or f-string serialization of dicts/lists.
- Verify TTLs are set on cached keys to prevent unbounded memory growth.

### 4. SCAN vs KEYS
- Flag `KEYS *` — it blocks Redis for all clients. Use `SCAN` with a
  `count` parameter instead.
- Verify SCAN cursors are handled correctly (loop until cursor == 0).

### 5. Connection Pool Configuration
- Check for `socket_timeout` and `socket_connect_timeout` settings.
- Flag connections created per-request instead of pooled/reused.

## Steps

1. Read the target file(s) specified by the argument (or scan the
   project for `redis` imports if no argument given).
2. For each Redis usage site, check the 5 items above.
3. Report findings with file path, line number, severity, and a
   concrete fix recommendation.
4. Provide an overall PASS/FAIL verdict.
