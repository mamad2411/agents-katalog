---
name: go-context-timeouts
description: >
  Go context timeouts and deadlines: context.WithTimeout/WithDeadline/WithCancel,
  propagation across API/DB/RPC boundaries, cleanup with cancel, error handling
  (DeadlineExceeded vs Canceled), and testing. Use when hardening owned Go services
  against hung dependencies.
---

# Go Context Timeouts

## Scope And Authorization

- **In scope:** Application code you maintain.
- **Out of scope:** Intentionally timing out third-party clients as an attack.
- Every `WithTimeout`/`WithCancel` must call `cancel` to release resources.
- Pair with `retry-backoff-patterns`, `go-errgroup-limits`, and `code-quality-standards`.

## When To Use

- HTTP handlers bounding outbound calls.
- Worker loops with per-task deadlines.
- Preventing connection pool exhaustion from stuck RPCs.
- Aligning client timeouts with server-side deadlines.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Bounded parallel work | `go-errgroup-limits` |
| Retries/backoff | `retry-backoff-patterns` |
| Singleflight coalescing | `go-singleflight-dedupe` |
| Go style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| API | Role |
| --- | --- |
| `context.Background` | Root of trees (main, init-free) |
| `context.TODO` | Temporary when unclear — replace soon |
| `WithCancel` | Manual cancel |
| `WithTimeout` | Auto cancel after duration |
| `WithDeadline` | Absolute time |
| `WithValue` | Request-scoped values (use sparingly; not for optional params everywhere) |
| `ctx.Err()` | `Canceled` or `DeadlineExceeded` |
| Propagation | Pass `ctx` as first param |

## Workflow

### 1. Set timeout policy

| Layer | Example bound |
| --- | --- |
| Inbound HTTP server | `ReadHeaderTimeout`, handler ctx from request |
| Outbound HTTP | 3–10s for UX path; longer for batch |
| DB query | Slightly under handler budget |
| Total handler | Sum of children &lt; client timeout |

Document budgets so nested timeouts don’t immediately fire.

### 2. Handler pattern

```go
func (h *Handler) Get(w http.ResponseWriter, r *http.Request) {
    ctx, cancel := context.WithTimeout(r.Context(), 3*time.Second)
    defer cancel()

    out, err := h.svc.Fetch(ctx, idFrom(r))
    if err != nil {
        if errors.Is(err, context.DeadlineExceeded) {
            http.Error(w, "timeout", http.StatusGatewayTimeout)
            return
        }
        // ...
    }
    // write out
}
```

Prefer deriving from `r.Context()` so client disconnect cancels work.

### 3. Outbound call

```go
func (c *Client) Fetch(ctx context.Context, id string) (Result, error) {
    req, err := http.NewRequestWithContext(ctx, http.MethodGet, c.url+id, nil)
    if err != nil {
        return Result{}, err
    }
    res, err := c.http.Do(req)
    // ...
}
```

Always `NewRequestWithContext` — bare `NewRequest` ignores cancel.

### 4. Cancel hygiene

```go
ctx, cancel := context.WithTimeout(parent, 5*time.Second)
defer cancel() // ALWAYS, even on success
```

Leaking cancel functions retains parent resources and timers.

### 5. Select loops

```go
select {
case <-ctx.Done():
    return ctx.Err()
case job := <-jobs:
    // process with ctx
}
```

### 6. Error classification

```go
switch {
case errors.Is(err, context.Canceled):
    // client gone or parent cancel — often not server bug
case errors.Is(err, context.DeadlineExceeded):
    // budget exhausted — metric + 504/timeout
default:
    // other errors
}
```

Wrap with `%w` so `errors.Is` works.

### 7. Testing timeouts

```go
func TestFetchTimeout(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 20*time.Millisecond)
    defer cancel()
    // server that sleeps 200ms
    _, err := client.Fetch(ctx, "1")
    if !errors.Is(err, context.DeadlineExceeded) {
        t.Fatalf("got %v", err)
    }
}
```

Avoid extreme short timeouts that flake on slow CI — use fake clocks or controllable stubs when needed.

### 8. Anti-patterns

| Bad | Why |
| --- | --- |
| `context.Background()` in every handler ignoring request | Disconnect ignored |
| Storing ctx in struct long-lived | Lifecycle bugs |
| Timeout longer than parent always | Pointless child budget |
| Swallowing `ctx.Err()` | Hung UX without metrics |
| Using WithValue for optional DI everywhere | Hidden coupling |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Derive | From `r.Context()` | New Background per request ignoring parent |
| Cancel | `defer cancel()` | Forget cancel |
| HTTP | `NewRequestWithContext` | Ignore ctx on Do |
| Errors | `errors.Is` deadline | String match `"context deadline"` |
| Metrics | timeout counters | Silent 500s |

## Output Checklist

- [ ] Timeout budgets documented per layer
- [ ] ctx passed first to blocking calls
- [ ] All WithTimeout/Cancel deferred cancel
- [ ] HTTP/gRPC/DB use ctx
- [ ] Deadline vs cancel handled for responses/metrics
- [ ] Tests cover timeout path
- [ ] No ctx in long-lived structs
- [ ] `code-quality-standards` applied

## Rules

- First argument `ctx context.Context`.
- Always cancel.
- Propagate parent; tighten child budgets carefully.
- Measure timeouts as first-class SLIs.
- Retries must respect remaining deadline (`retry-backoff-patterns`).
