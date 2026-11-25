---
tags: [backend, kafka, debounce, event, coalescing]
name: kafka-debounce-event-coalescing
description: Coalesce bursts of change events into one Kafka event per tenant per debounce window using Redis state (first/last change time + changed-tenant SET), with a MAX_WAIT fallback so a never-quiet stream still fires.
trigger: Bursts of upstream change events (MongoDB change stream, bulk API mutations) would otherwise fan out into N downstream Kafka events per tenant.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# Kafka Debounce Event Coalescing (Redis-backed)

## Shape

- Debouncer service keeps per-tenant timing state in Redis: `first_change_time`, `last_change_time`, SET `changed_tenants`.
- Publisher fires one Kafka event per tenant when either (a) the debounce window elapses with no new event, or (b) the MAX_WAIT ceiling since the first change is reached.
- Consumer acquires a per-tenant Redis lock; concurrent events set a `recheck` flag, forcing a second pass rather than being dropped.

## Steps

1. On each upstream change, capture `tenantId`. `SET NX first_change_time=now`; always update `last_change_time=now`.
2. `SADD changed_tenants tenantId`.
3. If `now - first_change_time >= MAX_WAIT` (e.g. 5 min) → fire immediately. Else schedule debounce timer (e.g. 1 min idle).
4. On timer, `SMEMBERS changed_tenants` and publish one Kafka event **per tenant** (not a bulk event — keeps downstream sharding simple).
5. Clear `first_change_time`, `last_change_time`, `changed_tenants`.
6. Consumer: per-tenant Redis lock with TTL; if lock fails, `SET recheck:<tenant> 1` and return.
7. Lock holder loop: `DEL recheck:<tenant>` → run logic → if `recheck` re-set during logic, loop again.

## Counter / Caveats

- TTLs must exceed worst-case processing time or lock is stolen mid-run.
- `MAX_WAIT` guards a continuously-noisy stream from starving downstream updates forever.
- One-event-per-tenant shape only helps when downstream is tenant-keyed.
- Re-check flag must be cleared **before** running logic, not after, or you'll miss events arriving during logic.
