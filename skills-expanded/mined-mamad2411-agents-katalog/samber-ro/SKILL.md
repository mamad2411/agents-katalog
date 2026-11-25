---
name: samber-ro
description: "stream — reactive streams with samber/ro: declarative, type-safe pipelines over asynchronous or infinite data with 150+ operators, 5 subject types, and 40+ plugins. Use when building event-driven pipelines, choosing between cold/hot observables and subjects, composing typed Pipe chains with backpressure and retry, or deciding whether ro, lo, or errgroup fits the data. Not for finite slice transforms — use samber-lo."
license: MIT
---

# samber/ro

**Stream.** Reach for reactive streams only when data arrives over time, from multiple sources, or needs retry/timeout/backpressure — a finite slice is samber/lo's job. The discipline is to **compose**: build declarative pipelines with typed operators, make every subscription observe all three events, and bound every infinite stream so it can always stop.

## Steps — choose the tool

1. **Match the tool to the data.** Finite slice → `samber/lo`. Bounded goroutine fan-out with error handling → `errgroup`. Async, infinite, time-aware, or multi-source data → `samber/ro`.
   *Done when: ro handles only streams that are infinite, time-aware, or multi-source; finite transforms stay in lo.*
2. **Pick cold by default.** Each cold `.Subscribe()` starts an independent execution — use it unless the source is expensive (WebSocket, DB poll) or subscribers must see identical events. Go hot via `Share`, `ShareReplay(n)`, `Connectable`, or Subjects.
   *Done when: every hot observable has a stated reason (shared source or shared events); everything else is cold.*

## Steps — build the pipeline

3. **Use typed Pipe chains.** `Pipe2`...`Pipe25` keep compile-time type safety across operators; untyped `Pipe` uses `any` and moves type errors to runtime.
   *Done when: no operator chain uses untyped Pipe where a typed PipeN fits.*
4. **Pick operators by job.** Creation (Just, FromChannel, Range, Interval, Defer), Transform (Map, FlatMap, Scan, GroupBy), Filter (Take, Distinct, Skip), Combine (Merge, Zip, CombineLatest, Race), Error (Catch, Retry, OnErrorReturn), Timing (Delay, Timeout, ThrottleTime), Side effect (Tap), Terminal (Collect, ToSlice, ToChannel).
   *Done when: each pipeline step maps to one operator category, and side effects route through Tap, not Map.*
5. **Observe all three events.** `ro.NewObserver(onNext, onError, onComplete)` — an unhandled error is silent data loss. `ro.Collect(observable)` blocks a finite stream and returns `([]T, error)`.
   *Done when: no subscription drops onError.*
6. **Bound every stream.** Infinite streams get `Take(n)`, `TakeUntil(signal)`, `Timeout(d)`, or context cancellation (`ContextWithTimeout`, `ThrowOnContextCancel`); call `.Unsubscribe()` or `.Wait()` deliberately.
   *Done when: every stream can terminate, and nothing leaks on shutdown.*

## Steps — review or audit

1. **Scan for `OnNext`-only observers.** *Done when: every observer handles all three callbacks.*
2. **Check for untyped `Pipe`.** *Done when: the hot path uses typed PipeN.*
3. **Verify every stream is bounded.** *Done when: each infinite stream has a terminal condition.*
4. **Check for ro on finite slices.** *Done when: no ro pipeline replaces a lo one-liner.*

## Reference

### Core concepts

1. **Observable** — a data source that emits values over time. Cold by default: each subscriber triggers independent execution from scratch
2. **Observer** — a consumer with three callbacks: `onNext(T)`, `onError(error)`, `onComplete()`
3. **Operator** — a function that transforms an observable into another observable, chained via `Pipe`
4. **Subscription** — the connection between observable and observer. Call `.Wait()` to block or `.Unsubscribe()` to cancel

```go
observable := ro.Pipe2(
    ro.RangeWithInterval(0, 5, 1*time.Second),
    ro.Filter(func(x int) bool { return x%2 == 0 }),
    ro.Map(func(x int) string { return fmt.Sprintf("even-%d", x) }),
)

observable.Subscribe(ro.NewObserver(
    func(s string) { fmt.Println(s) },      // onNext
    func(err error) { log.Println(err) },    // onError
    func() { fmt.Println("Done!") },         // onComplete
))
// Output: "even-0", "even-2", "even-4", "Done!"

// Or collect synchronously:
values, err := ro.Collect(observable)
```

### Cold vs hot

**Cold** (default): each `.Subscribe()` starts a new independent execution — safe and predictable, use by default.
**Hot**: multiple subscribers share a single execution — use when the source is expensive or subscribers must see the same events.

| Convert with | Behavior |
| --- | --- |
| `Share()` | Cold → hot with reference counting. Last unsubscribe tears down |
| `ShareReplay(n)` | Same as Share + buffers last N values for late subscribers |
| `Connectable()` | Cold → hot, but waits for explicit `.Connect()` call |
| Subjects | Natively hot — call `.Send()`, `.Error()`, `.Complete()` directly |

| Subject | Constructor | Replay behavior |
| --- | --- | --- |
| `PublishSubject` | `NewPublishSubject[T]()` | None — late subscribers miss past events |
| `BehaviorSubject` | `NewBehaviorSubject[T](initial)` | Replays last value to new subscribers |
| `ReplaySubject` | `NewReplaySubject[T](bufferSize)` | Replays last N values |
| `AsyncSubject` | `NewAsyncSubject[T]()` | Emits only last value, only on complete |
| `UnicastSubject` | `NewUnicastSubject[T](bufferSize)` | Single subscriber only |

### Operator quick reference

| Category | Key operators | Purpose |
| --- | --- | --- |
| Creation | `Just`, `FromSlice`, `FromChannel`, `Range`, `Interval`, `Defer`, `Future` | Create observables from various sources |
| Transform | `Map`, `MapErr`, `FlatMap`, `Scan`, `Reduce`, `GroupBy` | Transform or accumulate stream values |
| Filter | `Filter`, `Take`, `TakeLast`, `Skip`, `Distinct`, `Find`, `First`, `Last` | Selectively emit values |
| Combine | `Merge`, `Concat`, `Zip2`–`Zip6`, `CombineLatest2`–`CombineLatest5`, `Race` | Merge multiple observables |
| Error | `Catch`, `OnErrorReturn`, `OnErrorResumeNextWith`, `Retry`, `RetryWithConfig` | Recover from errors |
| Timing | `Delay`, `DelayEach`, `Timeout`, `ThrottleTime`, `SampleTime`, `BufferWithTime` | Control emission timing |
| Side effect | `Tap`/`Do`, `TapOnNext`, `TapOnError`, `TapOnComplete` | Observe without altering stream |
| Terminal | `Collect`, `ToSlice`, `ToChannel`, `ToMap` | Consume stream into Go types |

Use typed `Pipe2`, `Pipe3` ... `Pipe25` for compile-time type safety across operator chains.

### Plugin ecosystem

40+ plugins extend ro with domain-specific operators:

| Category | Plugins | Import path prefix |
| --- | --- | --- |
| Encoding | JSON, CSV, Base64, Gob | `plugins/encoding/...` |
| Network | HTTP, I/O, FSNotify | `plugins/http`, `plugins/io`, `plugins/fsnotify` |
| Scheduling | Cron, ICS | `plugins/cron`, `plugins/ics` |
| Observability | Zap, Slog, Zerolog, Logrus, Sentry, Oops | `plugins/observability/...`, `plugins/samber/oops` |
| Rate limiting | Native, Ulule | `plugins/ratelimit/...` |
| Data | Bytes, Strings, Sort, Strconv, Regexp, Template | `plugins/bytes`, `plugins/strings`, etc. |
| System | Process, Signal | `plugins/proc`, `plugins/signal` |

### Deep references

- **[Subjects Guide](./references/subjects-guide.md)** — subject details and hot observable patterns
- **[Operators Guide](./references/operators-guide.md)** — complete operator catalog (150+ operators with signatures)
- **[Plugin Ecosystem](./references/plugin-ecosystem.md)** — full plugin catalog with import paths and usage examples
- **[Patterns](./references/patterns.md)** — retry+timeout, WebSocket fan-out, graceful shutdown, stream combination

### Official resources

- [github.com/samber/ro](https://github.com/samber/ro)
- [ro.samber.dev](https://ro.samber.dev)
- [pkg.go.dev/github.com/samber/ro](https://pkg.go.dev/github.com/samber/ro)

## Watch for

| Mistake | Fix |
| --- | --- |
| `ro.OnNext` without an error handler | `ro.NewObserver(onNext, onError, onComplete)` |
| Untyped `Pipe()` | `Pipe2`...`Pipe25` for type safety |
| Unbounded infinite stream | `TakeUntil`/`Timeout`/context cancellation |
| `Share()` when cold suffices | Cold by default; hot only for shared sources |
| ro for finite slice transforms | `samber/lo` |
| Ignoring cancellation on shutdown | `ContextWithTimeout`/`ThrowOnContextCancel` in the chain |

## Cross-references

- → See `samber-lo` for finite slice transforms (Map, Filter, Reduce, GroupBy)
- → See `samber-mo` for Option/Result monads that compose with ro pipelines
- → See `samber-hot` for in-memory caching (also available as an ro plugin)
- → See `samber-oops` for structured errors (oops plugin) in streams
- → See `go-concurrency` for goroutine/channel patterns when reactive streams are overkill
- → See `go-observability` for monitoring reactive pipelines in production
