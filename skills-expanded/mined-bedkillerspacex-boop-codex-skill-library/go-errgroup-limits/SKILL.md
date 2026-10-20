---
name: go-errgroup-limits
description: >
  golang.org/x/sync/errgroup with concurrency limits: SetLimit, error propagation,
  context cancel on first error, and patterns for bounded fan-out in owned Go
  services. Use when parallelizing work safely without goroutine storms.
---

# Go errgroup Limits

## Scope And Authorization

- **In scope:** Owned Go codebases parallelizing I/O or CPU tasks.
- **Out of scope:** Stress-testing third-party APIs without authorization.
- Unbounded `g.Go` can exhaust memory/FDs — always bound when N is large.
- Pair with `go-context-timeouts` and `code-quality-standards`.

## When To Use

- Fan-out HTTP/DB calls with a max concurrency.
- Wait for multiple tasks; return first error; cancel siblings.
- Replacing ad-hoc `sync.WaitGroup` + error mutex patterns.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Context deadlines only | `go-context-timeouts` |
| Singleflight dedupe | `go-singleflight-dedupe` |
| Race detector | `go-race-detector-workflow` |
| Worker pool frameworks | domain-specific queues |
| Implementation quality | `code-quality-standards` |

## Concepts

| API | Role |
| --- | --- |
| `errgroup.WithContext` | Shared cancel on first error |
| `g.Go(func() error)` | Start task |
| `g.Wait()` | Wait all; return first error |
| `g.SetLimit(n)` | Max active goroutines (x/sync) |
| First error cancel | Sibling ctx done |

## Workflow

### 1. Choose limit

| Work | Limit heuristic |
| --- | --- |
| External API | Match provider rate + connection pool |
| DB | ≤ pool size |
| CPU-bound | ≈ `runtime.GOMAXPROCS(0)` |
| Mixed | Measure; start conservative (8–32) |

### 2. Basic bounded fan-out

```go
import "golang.org/x/sync/errgroup"

func FetchAll(ctx context.Context, ids []string, c Client) ([]Result, error) {
    out := make([]Result, len(ids))
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(8)

    for i, id := range ids {
        i, id := i, id
        g.Go(func() error {
            r, err := c.Fetch(ctx, id)
            if err != nil {
                return err
            }
            out[i] = r // each i unique — no mutex needed
            return nil
        })
    }
    if err := g.Wait(); err != nil {
        return nil, err
    }
    return out, nil
}
```

### 3. Without SetLimit (small fixed N)

```go
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return loadA(ctx) })
g.Go(func() error { return loadB(ctx) })
return g.Wait()
```

OK when N is tiny and known.

### 4. Collect errors vs fail-fast

`errgroup` is **fail-fast** (first error cancels). For best-effort all results:

- Use WaitGroup + mutex error list, or
- Swallow per-item errors into result objects and return nil from `Go`.

Document which semantics the API needs.

### 5. Avoid common bugs

| Bug | Fix |
| --- | --- |
| Loop variable capture pre-Go 1.22 habits | `i, id := i, id` if old toolchain |
| Shared map write | Mutex or shard by index |
| Ignoring parent ctx | Always `WithContext` |
| Limit 0 | Means unlimited in SetLimit — careful |
| Nested errgroups without budgets | Share timeout parent |

### 6. Combine with timeout

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel()
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10)
// ...
err := g.Wait()
```

### 7. Test

```go
func TestFetchAll_CancelsSiblings(t *testing.T) {
    // first call errors; ensure other calls see ctx.Done
}
func TestFetchAll_RespectsLimit(t *testing.T) {
    // atomic current/max concurrency probe
}
```

### 8. Metrics

- In-flight goroutines / queue wait time if wrapping limit.
- Error rate on `Wait`.
- Partial success not available with fail-fast — metric abandoned tasks.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Concurrency | `SetLimit` for large slices | One goroutine per 100k item unbounded |
| Errors | Return err from Go | Panic in Go |
| Storage | Index into preallocated slice | Race on append without lock |
| Cancel | WithContext | WaitGroup forget cancel peers |
| Limits | Match pool size | Limit &gt;&gt; DB max conns |

## Output Checklist

- [ ] Fan-out uses errgroup or justified alternative
- [ ] SetLimit set when N unbounded/large
- [ ] Context derived and passed
- [ ] Slot writes race-free
- [ ] Fail-fast vs best-effort chosen deliberately
- [ ] Tests for error cancel and limit
- [ ] Timeouts applied at parent
- [ ] `code-quality-standards` applied

## Rules

- Bound concurrency for large N.
- Prefer `errgroup.WithContext` for sibling cancel.
- Do not ignore `Wait` errors.
- Align limits with downstream capacity.
- Context skill for deadline details; this skill for parallel limits.
