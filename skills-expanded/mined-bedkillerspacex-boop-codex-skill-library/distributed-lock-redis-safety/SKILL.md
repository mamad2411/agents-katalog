---
name: distributed-lock-redis-safety
description: >
  Implement safer distributed locks with Redis: token ownership, TTL/expiry, fencing tokens,
  extend/heartbeat, single-instance vs Redlock caveats, and when not to use Redis locks.
  Use when Redis distributed lock, SET NX EX, Redlock, fence token, lock renew, scheduler
  mutual exclusion, or multi-instance job safety on owned systems — not as a substitute for
  transactional DB integrity or consensus for strong correctness.
---

# Distributed Lock Redis Safety

## Scope And Authorization

- **In scope:** Applications and Redis deployments you own.
- **Out of scope:** Attacking shared Redis; using locks to bypass business authZ.
- Prefer staging tests of partition behavior before production reliance.
- Redact Redis passwords and production key names if sensitive in tickets.
- Pair with `retry-backoff-patterns`, `dependency-outage-degrade`, Redis security skills, and `code-quality-standards`.

## When To Use

- Only one instance should run a job, cron, or leader loop.
- Preventing double-charge / double-send with best-effort mutual exclusion **plus** idempotency.
- Reviewing `SET key NX EX` lock code for unlock races and deadlocks.
- Evaluating Redlock and understanding controversy / limitations.
- Choosing DB transaction / unique constraint instead of Redis lock.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Strong multi-key atomic business integrity | Database transactions / serializability design |
| Redis auth/network hardening | `redis-security-misconfig` |
| Outage degrade when Redis down | `dependency-outage-degrade` |
| Kafka exactly-once | messaging skills |
| Code quality baseline | `code-quality-standards` |

## Correctness model (read this)

Redis locks provide **mutual exclusion best-effort** under assumptions (single primary, synced clocks roughly for TTL mental model, process behavior). They are **not** a general substitute for:

- Consensus (etcd/ZooKeeper/Raft) for hard leadership in all network partitions
- DB unique constraints and transactional check-and-set for money/inventory

**Always** pair locks with **idempotent** work and **fencing** when stale holders can still write.

## Unsafe vs safer patterns

| Pattern | Problem |
| --- | --- |
| `SETNX` without TTL | Dead forever if process dies |
| Unlock by `DEL key` only | Deletes someone else’s lock after expiry |
| Ignore return of extend | Work continues without lock |
| Redlock without reading critiques | False confidence under partitions |
| Lock only, no fencing | Slow holder writes after losing lock |

| Safer element | Practice |
| --- | --- |
| `SET key token NX EX ttl` | Atomic acquire with expiry |
| Compare-and-delete | Lua/script: delete only if value == token |
| Fencing token | Monotonic token checked by resource (DB version) |
| Short critical section | Hold lock only for scheduling claim, not long IO |
| Idempotency keys | Business op safe if run twice |

## Workflow

### 1. Confirm scope and success criteria

1. What resource is protected? Cost of double-execution?
2. Success: no double-run under normal failover tests; crash releases via TTL; unlock cannot steal others’ locks; documented failure if Redis down (fail closed vs open).
3. Decide if a **DB unique job row** is the real source of truth.

### 2. Inventory current lock code

```bash
rg -n "SETNX|setnx|Redlock|acquire_lock|release_lock|redis\.lock|NX.*EX" .
```

1. Note TTL, renew, unlock, and error handling.
2. List all writers to the protected resource.

### 3. Implement single-primary safe lock

```python
# Illustrative — single Redis primary
import uuid
import redis

r = redis.Redis.from_url("redis://...")
LOCK_KEY = "locks:job:invoice-sync"
TTL_SEC = 30

def acquire() -> str | None:
    token = str(uuid.uuid4())
    ok = r.set(LOCK_KEY, token, nx=True, ex=TTL_SEC)
    return token if ok else None

RELEASE_LUA = """
if redis.call("get", KEYS[1]) == ARGV[1] then
  return redis.call("del", KEYS[1])
else
  return 0
end
"""

def release(token: str) -> bool:
    return bool(r.eval(RELEASE_LUA, 1, LOCK_KEY, token))
```

1. Never `DEL` without token check.
2. TTL must exceed max critical section **or** use renew carefully with same token.
3. On Redis errors: **fail closed** for financial ops (do not run unlocked).

### 4. Fencing tokens (strongly recommended)

```text
1. Acquire Redis lock (optional scheduler aid)
2. Increment monotonic fence in DB: UPDATE resource SET fence = fence+1 ...
3. All writes include WHERE fence = expected
4. Stale writer with old fence fails CAS
```

1. Resource rejects lower fence numbers.
2. Especially important if lock TTL can expire mid-work.

### 5. Renew / heartbeat caveats

1. Background renew must stop if work is done or process is unhealthy.
2. If renew fails, **abort** work; do not continue assuming lock.
3. Clock jumps: prefer TTL refresh from Redis server perspective; keep sections short.

### 6. Redlock and multi-node notes

1. Redlock tries multiple independent Redis nodes; correctness under delayed processes/clocks is **debated**.
2. For many apps: **one Redis primary + fencing + idempotency** is clearer than DIY Redlock.
3. If you need strong distributed consensus, use etcd/ZooKeeper/Consul leadership, not only Redis.
4. Redis Cluster: locks are per-key slot; understand failover and key loss windows.

### 7. Test, observe, hand off

```bash
# Staging chaos (owned)
# - kill holder mid-section → second instance acquires after TTL
# - concurrent acquisitors → only one token
# - unlock with wrong token → no-op
# - Redis down → app fails closed
```

1. Metrics: lock acquire failures, hold time, renew failures, fence reject count.
2. Document: key naming, TTL, owner service, and “do not hold across user requests.”
3. Apply `code-quality-standards` to lock helpers; centralize Lua scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Acquire | `SET NX EX` + token | `SETNX` without TTL |
| Unlock | Token-checked Lua | Blind `DEL` |
| Long work | Claim lease + fence + idempotent workers | Hold lock during 30m report |
| Redis down | Fail closed for money | Run without lock |
| Correctness | DB constraint + fence | “Redis lock guarantees exactly once” |
| Redlock | Know limits / prefer alternatives | Paste from blog as proven CP |

## Output Checklist

- [ ] Protected resource and double-run cost documented
- [ ] Acquire uses NX+EX+unique token
- [ ] Release is compare-and-delete
- [ ] TTL/renew policy safe; abort on renew fail
- [ ] Fencing or DB uniqueness for writers
- [ ] Idempotency for business operations
- [ ] Fail-closed behavior on Redis errors defined
- [ ] Chaos tests on staging recorded
- [ ] Metrics/alerts on lock failures
- [ ] `code-quality-standards` applied

## Rules

- Locks aid exclusion; they do not replace transactional integrity.
- Never delete a lock key without owning the token.
- Keep critical sections short; design for expiry.
- Document Redlock limitations if used.
- Owned systems only; evidence over folklore.
