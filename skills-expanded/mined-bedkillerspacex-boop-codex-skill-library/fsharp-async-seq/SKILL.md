---
name: fsharp-async-seq
description: >
  Use F# AsyncSeq (and related async sequences) for streaming pipelines: generation,
  map/filter/scan, backpressure-aware consumption, cancellation, and error handling.
  Use when building owned F# services or scripts that process async streams of events,
  pages, or IO results more naturally than raw Async or Task sequences alone.
---

# F# AsyncSeq

## Scope And Authorization

- **In scope:** F# codebases you own or are authorized to modify.
- **Out of scope:** unlicensed redistribution of proprietary libraries beyond project rights.
- Handle cancellation and secret redaction in streamed logs.
- Pair with `code-quality-standards` and relevant .NET security practices.

## When To Use

- Processing **asynchronous sequences** (paged APIs, log tails, message batches) in F#.
- Composing `AsyncSeq.mapAsync`, `filter`, `choose`, `scan` pipelines.
- Bridging `IAsyncEnumerable` / `task { }` ecosystems carefully.
- Avoiding unbounded buffering when consuming producers.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| C# style conventions only | `csharp-style-conventions` |
| Observability patterns | `observability-metrics-tracing` |
| Retry/backoff policy design | `retry-backoff-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| `AsyncSeq<'T>` | Async-pull sequence abstraction (FSharpx / related libraries—confirm package in repo) |
| Generation | `asyncSeq { yield! ...; let! x = ... }` patterns |
| Transformation | map/filter parallel options with care |
| Consumption | `AsyncSeq.iterAsync`, `toListAsync` (memory!), `firstOrDefault` |
| Cancellation | Thread `CancellationToken` through async work |
| Errors | Decide fail-fast vs skip-with-log per item |

## Workflow

### 1. Confirm scope and success criteria

1. Package versions (`FSharp.Control.AsyncSeq` or repo equivalent), runtime, throughput needs.
2. Success: correct streaming semantics; cancellation works; memory stable under long streams.
3. Identify whether order must be preserved.

### 2. Inventory existing async patterns

```fsharp
// Search for AsyncSeq, IAsyncEnumerable, seq of Async
```

```bash
rg -n "AsyncSeq|asyncSeq|IAsyncEnumerable" -g '*.fs'
```

### 3. Model the producer

```fsharp
open FSharp.Control

let pagedApi (ct: System.Threading.CancellationToken) : AsyncSeq<Item> =
    asyncSeq {
        let mutable page = 0
        let mutable done' = false
        while not done' do
            ct.ThrowIfCancellationRequested()
            let! batch = fetchPage page ct |> Async.AwaitTask
            if batch.Length = 0 then
                done' <- true
            else
                for item in batch do
                    yield item
                page <- page + 1
    }
```

1. Prefer pull-driven pages over prefetching unbounded lists.
2. Bound page size; handle 429 with `retry-backoff-patterns`.

### 4. Build pipeline

```fsharp
let pipeline ct =
    pagedApi ct
    |> AsyncSeq.filter (fun x -> x.IsActive)
    |> AsyncSeq.mapAsync (fun x -> enrich x ct)
    |> AsyncSeq.bufferByCountAndTime 50 500
    // choose operators available in your version carefully
```

1. Avoid `toListAsync` on infinite streams.
2. For side effects use `iterAsync` with explicit error policy.
3. Parallel map only when order/side effects allow; cap concurrency.

### 5. Cancellation and resources

```fsharp
use cts = new System.Threading.CancellationTokenSource()
// link to host shutdown token
Async.RunSynchronously(pipeline cts.Token |> AsyncSeq.iterAsync processItem, cancellationToken = cts.Token)
```

1. Dispose HTTP clients/handlers appropriately (shared factory).
2. Ensure finally blocks run on cancel where needed.

### 6. Verify with evidence

| Test | Expect |
| --- | --- |
| Finite fixture stream | All items processed once |
| Cancel mid-way | Stops without hang |
| Empty pages | Completes cleanly |
| Error in map | Policy applied (fail or skip) |
| Long run | Stable memory |

### 7. Hand off

1. Document operator versions and concurrency caps.
2. Metrics: items/sec, lag, error rate.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Memory | Streaming iter | `toListAsync` on huge source |
| Cancel | Token threaded | Ignore cancel, hang on exit |
| Parallelism | Bounded | Unbounded `mapAsyncParallel` storms |
| Errors | Explicit policy | Silent empty on failures |
| APIs | Paged pull | Load all pages then seq |
| Secrets | Redacted logs | Log full records |

## Output Checklist

- [ ] Package/version confirmed
- [ ] Producer is pull/paged
- [ ] Pipeline operators justified
- [ ] Cancellation tested
- [ ] Error policy documented
- [ ] Memory/throughput checked
- [ ] Metrics considered
- [ ] `code-quality-standards` applied

## Rules

- Owned code only.
- Streaming does not remove need for authZ on each item when multi-tenant.
- Prefer bounded operators; measure before parallelizing.
- Confirm exact API names against the library version in the repo.
