---
name: redis-data-structures
description: Picks the right Redis structure, key naming and expiry for queues, counters, leaderboards, rate limits and sessions.
---

# Redis data structures

Choose by operation, set expiry by default, and make updates atomic.

## Steps

1. For each feature, state the operations needed (increment, pop oldest, top 10, check membership).
2. Match the structure:
   - Counter or rate limit: `INCR` with `EXPIRE` on first write, or a fixed window key like `rl:{user}:{minute}`.
   - Object with fields: `HASH` (`HSET`, `HINCRBY`), not a JSON string you rewrite whole.
   - Leaderboard: `ZSET` with `ZADD`, `ZREVRANGE` and `ZRANK`.
   - Unique items and membership: `SET`; counting huge uniques cheaply: `HyperLogLog`.
   - Work queue: `STREAM` with consumer groups and `XACK` rather than `LIST` when a lost job matters.
   - Session: `HASH` or string with a sliding `EXPIRE`.
3. Name keys as `app:entity:id:field`. Use hash tags (`{user42}`) when several keys must live on one cluster slot.
4. Give every cache and session key a TTL, with a little random jitter to avoid a stampede at expiry. Plan for eviction by choosing a `maxmemory-policy` (`allkeys-lru` for a cache, `noeviction` for a queue).
5. Make multi-step changes atomic with a Lua script or `MULTI`/`EXEC`. A lock uses `SET key value NX PX 30000` and releases only if the value matches.
6. Never use `KEYS *` in production; use `SCAN`. Watch for big keys with `MEMORY USAGE`.

## Rules

- Do not store data you cannot rebuild unless persistence is configured and tested.
- Bound the size of every list, set and stream (`XTRIM`, `LTRIM`).

## Report

A table of feature, structure, key pattern, TTL and the commands used.
