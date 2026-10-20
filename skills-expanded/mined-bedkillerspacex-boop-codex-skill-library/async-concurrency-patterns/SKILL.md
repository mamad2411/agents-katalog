---
name: async-concurrency-patterns
description: >
  Design and implement safe async/await and concurrency in application code: cancellation,
  timeouts, structured task lifetimes, shared-state races, and shutdown. Use when async,
  await, concurrency, race condition in code, CancellationToken/Context, Promise.all,
  goroutines, tokio tasks, or concurrent workers. Not for HTTP TOCTOU / business
  limit-overrun testing (see race-condition skill if present).
---

# Async Concurrency Patterns

## Scope And Authorization

- **In scope:** Application code you own (services, CLIs, workers) across languages.
- **Out of scope:** Exploiting race conditions on third-party systems for unauthorized gain; pure network TOCTOU abuse testing belongs to authorized race/business-logic skills.
- Prefer correctness under cancellation and shutdown over raw throughput hacks.
- Document concurrency invariants (who owns shared state; what locks protect).
- Pair implementations with `code-quality-standards` and language style skills.

## When To Use

- Introducing async I/O, worker pools, or fan-out/fan-in pipelines.
- Fixing flaky tests, lost cancellations, deadlocks, or “zombie” tasks.
- Choosing between mutexes, channels, actors, and immutable snapshots.
- Implementing graceful shutdown with in-flight work bounds.
- Reviewing `Promise.all` / `Task.WhenAll` / errgroup / JoinSet usage.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| HTTP limit-overrun / TOCTOU abuse testing | `race-condition` or business-logic race skill (authorized) |
| Retry/backoff policies | `retry-backoff-patterns` |
| Observability of concurrent systems | `observability-metrics-tracing` |
| Language-only style | python/ts/go/rust style skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concern | Guidance |
| --- | --- |
| Structured concurrency | Parent owns child tasks; cancel children on failure/shutdown |
| Cancellation | Cooperative; check tokens/contexts at await points |
| Timeouts | Bound every external wait; distinguish timeout vs cancel |
| Shared state | Prefer message passing; else mutex/RWLock with clear order |
| Backpressure | Bound queues; reject or block rather than unbounded memory |
| Shutdown | Drain or cancel with deadline; no fire-and-forget in servers |

## Cross-Language Patterns

| Pattern | Examples |
| --- | --- |
| Context propagation | Go `context.Context`; .NET `CancellationToken`; Python `asyncio.timeout` |
| Fan-out limited | semaphores, worker pools, `errgroup` + limit |
| All succeed | `Promise.all`, `Task.WhenAll`, `JoinSet` — handle partial failure |
| First success | `Promise.any` / `select` — cancel losers |
| Single-flight | coalesce identical in-flight loads |
| Actor / channel | one owner of mutable state |

## Workflow

### 1. Confirm scope and success criteria

1. Record language/runtime, service type, latency SLO, failure modes.
2. Success: no unbounded task leaks; cancellation stops work; no data races under TSAN/loom/stress; shutdown within deadline.
3. Identify shared mutable structures and external I/O.

### 2. Inventory concurrency sites

```bash
# Heuristic searches (adjust)
rg -n "async |await |Promise\.|Task\.|goroutine|tokio::spawn|asyncio|CancellationToken|context\.With" src
rg -n "Mutex|RWLock|Semaphore|Channel|Queue|lock\(" src
```

1. List background tasks started at process boot.
2. Note places catching-and-swallowing cancel exceptions.
3. Find unbounded `create_task` / `spawn` without join.

### 3. Baseline

1. Reproduce race under stress (`go test -race`, `pytest-asyncio` stress, `cargo +nightly` loom if used).
2. Measure queue depths and task counts under load.
3. Capture hang dumps if deadlocks suspected.

### 4. Apply safe patterns

**Propagate cancellation (Go):**

```go
func fetchAll(ctx context.Context, urls []string) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(8)
    for _, u := range urls {
        u := u
        g.Go(func() error {
            req, err := http.NewRequestWithContext(ctx, http.MethodGet, u, nil)
            if err != nil { return err }
            res, err := http.DefaultClient.Do(req)
            if err != nil { return err }
            defer res.Body.Close()
            return nil
        })
    }
    return g.Wait()
}
```

**Timeouts (TypeScript):**

```ts
async function withTimeout<T>(p: Promise<T>, ms: number, signal?: AbortSignal): Promise<T> {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), ms);
  const onAbort = () => ac.abort();
  signal?.addEventListener("abort", onAbort, { once: true });
  try {
    return await Promise.race([
      p,
      new Promise<T>((_, rej) => ac.signal.addEventListener("abort", () => rej(new Error("timeout")), { once: true })),
    ]);
  } finally {
    clearTimeout(t);
    signal?.removeEventListener("abort", onAbort);
  }
}
```

**Shared state**

1. Prefer immutable snapshots published under a lock, then process lock-free.
2. Define global lock order if multiple mutexes; document it.
3. Never hold locks across slow network awaits unless designed for it.

**Bounded workers**

```text
queue capacity N → worker pool size M → reject/backpressure when full
```

**Shutdown**

1. Stop accepting new work; cancel context; await in-flight with max drain time; then force.
2. Register SIGTERM handlers that trigger the same path as health “not ready.”

### 5. Verify with evidence

```bash
go test ./... -race -count=20
cargo test
# Node
npm test
# Force cancel paths in unit tests (token canceled mid-flight)
```

1. Unit-test cancellation: after cancel, no further side effects (no extra DB writes).
2. Load test: memory stable (no task leak).
3. Shutdown test: process exits within SLA under in-flight load.

### 6. Observe and harden

1. Metrics: in-flight tasks, queue depth, cancel counts, timeout counts.
2. Trace context must propagate across async boundaries.
3. Alert on sustained queue saturation.

### 7. Hand off

1. Document concurrency model (threads/event loop/workers).
2. List invariants and lock orders.
3. Link retry/observability companions.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Spawn | structured parent/child | fire-and-forget in request path |
| Cancel | cooperative + tests | ignore OperationCanceled |
| Timeout | every external I/O | hang forever on socket |
| Shared state | channels or clear mutex | ad-hoc globals |
| Fan-out | bounded concurrency | unbounded Promise.all on user input size |
| Shutdown | drain with deadline | kill -9 as only strategy |

## Output Checklist

- [ ] Language/runtime and success criteria recorded
- [ ] Concurrency sites inventoried
- [ ] Cancellation and timeouts on external waits
- [ ] Structured task lifetimes / no leaks
- [ ] Shared-state strategy documented
- [ ] Backpressure bounds applied
- [ ] Race/stress tests green with evidence
- [ ] Graceful shutdown path tested
- [ ] Metrics for queues/in-flight considered
- [ ] `code-quality-standards` applied

## Rules

- Prefer structured concurrency and bounded work.
- Cancellation and timeouts are correctness, not polish.
- Do not use this skill as a playbook for unauthorized TOCTOU attacks on others’ systems.
- Evidence from race detectors and stress tests over “looks fine.”
- Focus on in-process concurrency; route distributed races and HTTP limit races to their skills.
