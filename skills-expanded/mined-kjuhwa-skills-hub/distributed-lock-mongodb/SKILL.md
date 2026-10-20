---
tags: [backend, distributed, lock, mongodb]
name: distributed-lock-mongodb
description: MongoDB findAndModify-based distributed lock with TTL expiry, owner tagging, and retry loop for multi-instance Spring Boot services.
trigger: Need mutual exclusion across JVM instances without Redis/Zookeeper; using MongoDB already.
source_project: lucida-meta
version: 1.0.0
category: backend
---

# Distributed Lock over MongoDB

## Shape

A `DistributedLockService` exposes `tryLock(key, ttl)` / `release(key, owner)`.

Implementation uses atomic `findAndModify` on a single `locks` collection:

- Document: `{ _id: key, owner: "<node>:<thread>", expiresAt: Date }`
- Acquire: `findAndModify(query = { _id: key, $or: [{expiresAt: {$lt: now}}, {_id: {$exists: false}}] }, update = { owner, expiresAt: now + ttl }, upsert: true)`
- Release: `deleteOne({ _id: key, owner: self })` (never blind delete)
- Retry: loop with 100 ms sleep up to configured timeout before giving up

## Steps

1. Create collection `locks` with TTL index on `expiresAt` as a safety net (not authoritative — acquire query checks expiry).
2. Implement `tryLock` using Mongo atomic upsert; return `false` when a different non-expired owner holds the key.
3. Always stamp `owner = "<hostname>:<threadName>"` so release is idempotent and crash-safe.
4. Wrap critical section in `try { if (tryLock) ... } finally { release }`.
5. For retry-until-timeout semantics, add a thin loop around `tryLock` rather than blocking inside the lock method.

## Counter / Caveats

- NTP drift across nodes skews TTL comparison — keep TTLs generous (seconds, not ms).
- Do not use a TTL index as the *only* expiry mechanism; the background deleter runs every 60 s.
- Prefer Redis/Redisson if you need fair queuing or pub-sub release notifications.
