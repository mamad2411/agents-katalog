---
name: redis-7-cache-design
description: Designs Redis 7 cache features, key schemas, TTL policies, invalidation, stampede protection, and tests. Use when implementing or reviewing Redis-backed caching, sessions, queues, coordination, or data-structure choices.
license: MIT
compatibility: Requires Redis Open Source 7.x context. Does not assume Redis Stack modules or language-specific client APIs.
---

# Redis 7 Cache Design

Use this skill when designing, modifying, or reviewing Redis 7-backed application behavior.

## Primary Responsibilities

- Select Redis data structures that fit the workload.
- Define key naming, TTL, invalidation, and memory behavior.
- Keep Redis 7 compatibility boundaries clear.
- Avoid Redis Stack-only commands unless the project explicitly includes Redis Stack.
- Design tests for cache hits, misses, expiration, invalidation, failures, and reconnects.

## Workflows

- `workflows/cache-feature-workflow.md`: Use when adding or changing Redis-backed cache, session, queue, rate-limit, or coordination behavior.

## Resources

- `resources/key-design-checklist.md`: Use when designing or reviewing Redis key schemas.

## Examples

- `examples/cache-aside-example.md`: Reference pattern for cache-aside behavior without tying the plugin to a specific application language.

## Design Guidance

1. Identify the workload pattern:
   - Cache-aside.
   - Session store.
   - Rate limiter.
   - Queue or stream.
   - Leaderboard or ranking.
   - Distributed coordination.
   - Durable Redis-backed state.

2. Choose the smallest Redis data model that satisfies the requirement:
   - String for simple values, counters, locks, and serialized values.
   - Hash for bounded entity fields.
   - Set for uniqueness and membership.
   - Sorted set for ranking, scheduling, time windows, and priority.
   - List for simple queue-like behavior when stream semantics are not needed.
   - Stream for append-only event processing with consumer groups.
   - Bitmap, bitfield, HyperLogLog, or geospatial structures only when their tradeoffs are understood.

3. Define key lifecycle:
   - Key prefix and version.
   - Identifier and tenant boundaries.
   - TTL or persistence rationale.
   - Invalidation triggers.
   - Rebuild behavior.
   - Memory bound.
   - Ownership by service or domain.

4. Define failure behavior:
   - Redis unavailable.
   - Redis timeout.
   - Cache miss storm.
   - Stale cached value.
   - Partial write failure.
   - Reconnect after failover.
   - Eviction or expiration.

5. Define tests:
   - Cache hit.
   - Cache miss.
   - TTL expiration.
   - Invalidation.
   - Serialization compatibility.
   - Concurrent refresh.
   - Redis connection failure.
   - Memory or eviction-sensitive behavior when practical.

## Redis 7 Server-Side Logic

Prefer Redis Functions for durable server-side logic in Redis 7 when logic must live in Redis and be managed with the database. Keep Lua/EVAL usage small, deterministic, and reviewed for key access correctness.

## Agent Safety

- Do not use destructive commands to inspect state.
- Do not propose `KEYS *` for production diagnostics.
- Do not introduce Redis Stack commands unless Redis Stack is explicitly present.
- Do not store secrets in examples.
- Do not turn Redis into the source of truth without persistence, backup, restore, and operational requirements.
