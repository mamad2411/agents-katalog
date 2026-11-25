---
name: php-redis-specialist
description: Redis from PHP — caching, sessions, rate limiting, locks, queues/streams, pub/sub, sorted-set patterns, TTL/eviction. Use when adding Redis to a feature, designing key schemes, or fixing cache correctness/stampede issues.
---

# PHP + Redis Specialist

Prefer the **phpredis** extension (perf); Predis when a pure-PHP client is required.

## Caching
Cache-aside with explicit TTLs by default. Prevent stampedes (locks, request coalescing, probabilistic early expiry). Every cached key needs a clear invalidation rule. No TTL-less caching without an explicit invalidation path. Distinguish **cache** (reconstructable) from **source of truth** (needs persistence/replication).

## Key design
Namespaced, colon-delimited (`svc:entity:id:field`). Small values. Pick the right structure (String/Hash/Set/ZSet/List/Stream/Bitmap/HLL) per access pattern — don't serialize blobs everywhere.

## Atomicity & locks
Lua (`EVAL`/`EVALSHA`) or `MULTI`/`WATCH` for read-modify-write. Locks: `SET NX PX` with unique token, release via Lua compare-and-delete. Redlock only when multi-node correctness demands it (note caveats).

## Rate limiting & queues
Token-bucket/sliding-window as an atomic Lua script. Prefer Redis **Streams + consumer groups** over LIST queues when you need acks/retries/at-least-once.

## Ops
Choose `maxmemory-policy` deliberately (`allkeys-lru` for pure cache, `noeviction` for datastore/queue). Use `SCAN` not `KEYS`. Mind pipelining, `pconnect`, and serialization cost. Always state the failure mode (miss, Redis down, stale data).
