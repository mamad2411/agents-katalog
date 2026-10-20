---
name: go-singleflight-dedupe
description: >
  Use golang.org/x/sync/singleflight to coalesce concurrent identical in-flight
  calls (cache stampede control): Group.Do/DoChan, key design, error sharing,
  Forget, and when not to use it. For owned Go services under parallel load.
---

# Go singleflight Deduplication

## Scope And Authorization

- **In scope:** Your services reducing duplicate concurrent work (DB/API fan-in).
- **Out of scope:** Using coalescing to hide authorization differences between callers
  (never share privileged results across users).
- Keys must not mix tenants/users with different authz.
- Pair with `caching-strategies`, `go-context-timeouts`, `code-quality-standards`.

## When To Use

- Cache miss stampede on hot keys.
- Expensive compute/RPC where concurrent identical requests should share one call.
- Thundering herd after deploy/cache flush.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General caching TTL/LRU | `caching-strategies` |
| errgroup fan-out | `go-errgroup-limits` |
| Timeouts | `go-context-timeouts` |
| Distributed locks across nodes | Redis/etcd lock skills |
| Implementation quality | `code-quality-standards` |

## Concepts

| API | Role |
| --- | --- |
| `singleflight.Group` | Per-process coalescer |
| `Do(key, fn)` | Runs fn once for concurrent waiters on key |
| `DoChan` | Async variant |
| shared result | All waiters get same v, err |
| `Forget(key)` | Drop in-flight bookkeeping for key |
| Not distributed | Each process has own Group |

## Workflow

### 1. Confirm fit

Use singleflight when:

- Many goroutines request the **same** key simultaneously
- Work is read-mostly idempotent
- Sharing the result is **safe** for all waiters (same authz)

Do **not** use when results depend on caller identity/permissions.

### 2. Basic pattern with cache

```go
import "golang.org/x/sync/singleflight"

type Loader struct {
    g     singleflight.Group
    cache *lru.Cache // conceptual
    db    DB
}

func (l *Loader) Get(ctx context.Context, id string) (Item, error) {
    if v, ok := l.cache.Get(id); ok {
        return v.(Item), nil
    }
    v, err, _ := l.g.Do(id, func() (interface{}, error) {
        item, err := l.db.Load(ctx, id)
        if err != nil {
            return nil, err
        }
        l.cache.Set(id, item)
        return item, nil
    })
    if err != nil {
        return Item{}, err
    }
    return v.(Item), nil
}
```

### 3. Context caveat

`Do` does not cancel `fn` when one waiter’s ctx dies if others still wait — design `fn`
to use a context that still makes sense (often a detached timeout or the first caller’s
ctx with care). Prefer documenting behavior; optionally select on ctx outside and accept
orphan work.

```go
// Pattern: respect caller ctx on wait side
ch := l.g.DoChan(id, func() (interface{}, error) { return l.db.Load(context.Background(), id) })
select {
case <-ctx.Done():
    return Item{}, ctx.Err()
case res := <-ch:
    return res.Val.(Item), res.Err
}
```

Note: work may continue after caller leaves — ensure that’s acceptable.

### 4. Error sharing

If `fn` errors, all waiters receive the error — good for outages, bad if error is
caller-specific. Keep `fn` key-scoped only.

### 5. Forget

```go
// After invalidation needing immediate reload
l.cache.Delete(id)
l.g.Forget(id)
```

Usually unnecessary for completed calls; useful for stuck or force-refresh designs.

### 6. Key design

| Good keys | Bad keys |
| --- | --- |
| `item:{id}` | `item:{id}:user:{uid}` coalesced across uids with different ACL |
| `url:sha256` for public fetch | Empty string key for everything |
| Normalized IDs | Unbounded free-form keys causing Group growth |

### 7. Metrics

- singleflight shared count (if instrumented wrapper)
- cache hit vs coalesced miss
- fn latency

### 8. Test

```go
func TestCoalesce(t *testing.T) {
    // launch N parallel Get same id; db.Load called once (atomic counter)
}
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authz | Public or same-privilege data only | Coalesce per-user private data together |
| Scope | Process-local stampede | Expect multi-replica dedupe |
| Keys | Explicit normalized | Giant structs stringified poorly |
| Errors | Shared infra errors | Caller-validation errors inside fn |
| Context | Document orphan work | Leak goroutines unbounded without timeout |

## Output Checklist

- [ ] Use case is stampede/coalesce safe
- [ ] Keys authz-safe
- [ ] Group lifetime matches process
- [ ] Cache + singleflight order correct (check cache first)
- [ ] Context behavior documented/tested
- [ ] Load call count tested under parallel
- [ ] Metrics optional
- [ ] `code-quality-standards` applied

## Rules

- Never share privileged responses across different principals.
- singleflight is in-process only.
- Combine with cache TTL strategies from caching skill.
- Bound work with timeouts.
- Forget carefully; don’t paper over bugs.
