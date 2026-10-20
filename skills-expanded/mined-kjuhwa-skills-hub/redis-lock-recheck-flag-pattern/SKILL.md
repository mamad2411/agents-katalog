---
tags: [backend, redis, lock, recheck, flag, pattern]
name: redis-lock-recheck-flag-pattern
description: Distributed Redis lock with a "recheck" flag so concurrent events arriving while the lock is held force the holder to run a second pass, instead of being silently dropped.
trigger: Multi-instance consumer must serialize work per-key (tenant/user/entity) but must not drop concurrent events arriving mid-processing.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# Redis Lock + Recheck Flag

## Shape

```
lockKey    = prefix:<key>
recheckKey = recheck:<key>
instanceId = <hostname>:<uuid>
```

Acquire via `SET lockKey instanceId NX EX ttl`. If acquired, loop: clear recheck → run work → if recheck was re-set during work, loop again. On exit, release with a Lua script that only deletes if the current value matches `instanceId` (prevents stealing).

## Steps

1. Compute `lockKey`, `recheckKey`, `instanceId`.
2. `SET lockKey instanceId NX EX ttl`.
3. Acquire failed → `SET recheckKey 1` and return. (Signals the holder: reprocess after done.)
4. Acquire succeeded → enter process loop:
   1. `DEL recheckKey` (clear **before** work).
   2. Run business logic.
   3. `EXISTS recheckKey`? If yes, loop. Else break. (Cap with `MAX_LOOPS` to prevent starvation.)
5. Release with Lua:
   ```
   if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) end
   return 0
   ```

## Counter / Caveats

- Choose TTL > worst-case processing time. If it expires mid-run, another instance grabs the lock — two workers.
- `DEL recheckKey` must happen **before** work, not after, or events arriving during work are lost.
- Cap the retry loop so a continuously-racing event stream can't pin one instance forever.
- Use a UUID-per-invocation for `instanceId`, not a static hostname — otherwise two worker threads on the same host can't tell their locks apart.
