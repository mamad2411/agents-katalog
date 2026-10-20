---
name: samber-lo
description: "transform — functional, type-safe collection transforms in Go with samber/lo: Map, Filter, Reduce, GroupBy, Chunk, and the lo/lop/lom/loi package ladder. Use when writing declarative transforms, reviewing hand-rolled loops, or choosing between core, parallel, mutable, and iterator variants. Not for streaming pipelines (→ See samber-ro)."
license: MIT
---

# samber/lo

**Leading word: transform.** Collection work is a declarative pipeline, not a loop. The discipline: reach for the stdlib first, compose `lo` transforms as immutable chains, use the `Err` variants where a step can fail, and escalate to `lop`/`lom`/`loi` only when profiling demands it.

## Steps — write transforms

1. **Prefer the stdlib where it already covers the operation.** `slices.Contains`, `slices.Sort`, `maps.Keys` carry no dependency. Reach for `lo` for the transforms the stdlib lacks — Map, Filter, Reduce, GroupBy, Chunk, Flatten, Zip.
   *Done when: no `lo` call duplicates a stdlib helper available since Go 1.21+.*
2. **Compose `lo` functions instead of nesting loops.** Chain `lo.Filter` → `lo.Map` → `lo.GroupBy`; each call returns a new collection, since `lo` is immutable by default.
   *Done when: every collection transform is a composed chain, not a hand-rolled loop.*
3. **Use the `Err` variants when a step can fail.** `MapErr`, `FilterErr`, `ReduceErr` stop on the first error and propagate it.
   *Done when: any fallible transform uses the Err variant and handles the returned error.*
4. **Reserve `lo.Must` for tests and init.** In production paths, use the non-Must variant and handle the error.
   *Done when: no `lo.Must` sits in a production call path.*

## Steps — choose the package

1. **Default to `lo`; escalate only on profiling evidence.** `lop`/`lom`/`loi`/`simd` trade safety or simplicity for throughput — switch after pprof identifies the bottleneck.
   *Done when: any non-core package choice cites a profiled bottleneck.*
2. **Use `lop` for CPU-bound parallel transforms on large slices** (1000+ items). It is not an I/O concurrency tool — for I/O fan-out use `errgroup`.
   *Done when: `lop` runs on big CPU-bound slices, and no `lop` Map wraps I/O.*
3. **Use `lom` only when allocation pressure is measured** (`go tool pprof -alloc_objects`). It mutates the input — callers must accept the side effect.
   *Done when: `lom` usage cites an allocation profile and the mutation is intentional.*
4. **Use `loi` for large chained transforms (Go 1.23+).** Lazy iterators eliminate intermediate allocations in chains like `Map → Filter → Take`.
   *Done when: long eager chains over big data switched to `loi`, or stayed eager with a reason.*

## Steps — review or audit

1. Scan for hand-rolled transform loops that `lo` replaces. *Done when: no manual loop reimplements a lo helper.*
2. Check every `lo` usage for a stdlib equivalent. *Done when: no unnecessary dependency for stdlib-covered ops.*
3. Check the hot list: `Must` in production, `lop` on tiny slices, eager chains on large data, mutation without intent. *Done when: the hot list is clean.*

## Reference

### Package ladder

| Package | Import | Alias | Go version | Use when |
| --- | --- | --- | --- | --- |
| Core (immutable) | `github.com/samber/lo` | `lo` | 1.18+ | Default for all transforms |
| Parallel | `github.com/samber/lo/parallel` | `lop` | 1.18+ | CPU-bound work on 1000+ items |
| Mutable | `github.com/samber/lo/mutable` | `lom` | 1.18+ | Hot path confirmed by `pprof -alloc_objects` |
| Iterator | `github.com/samber/lo/it` | `loi` | 1.23+ | Large datasets with chained transforms |
| SIMD (experimental) | `github.com/samber/lo/exp/simd` | — | 1.25+ (amd64) | Numeric bulk ops after benchmarking |

### Core patterns

```go
names := lo.Map(users, func(u User, _ int) string { return u.Name })

total := lo.Reduce(
    lo.Filter(orders, func(o Order, _ int) bool { return o.Status == "paid" }),
    func(sum float64, o Order, _ int) float64 { return sum + o.Amount },
    0,
)

byStatus := lo.GroupBy(tasks, func(t Task, _ int) string { return t.Status })

results, err := lo.MapErr(urls, func(url string, _ int) (Response, error) {
    return http.Get(url)
})
```

### Quick reference

| Function | What it does |
| --- | --- |
| `lo.Map` | Transform each element |
| `lo.Filter` / `lo.Reject` | Keep / remove elements matching predicate |
| `lo.Reduce` | Fold elements into a single value |
| `lo.ForEach` | Side-effect iteration |
| `lo.GroupBy` | Group elements by key |
| `lo.Chunk` | Split into fixed-size batches |
| `lo.Flatten` | Flatten nested slices one level |
| `lo.Uniq` / `lo.UniqBy` | Remove duplicates |
| `lo.Find` / `lo.FindOrElse` | First match or default |
| `lo.Contains` / `lo.Every` / `lo.Some` | Membership tests |
| `lo.Keys` / `lo.Values` | Extract map keys or values |
| `lo.PickBy` / `lo.OmitBy` | Filter map entries |
| `lo.Zip2` / `lo.Unzip2` | Pair/unpair two slices |
| `lo.Range` / `lo.RangeFrom` | Generate number sequences |
| `lo.Ternary` / `lo.If` | Inline conditionals |
| `lo.ToPtr` / `lo.FromPtr` | Pointer helpers |
| `lo.Must` / `lo.Try` | Panic-on-error / recover-as-bool |
| `lo.Async` / `lo.Attempt` | Async execution / retry with backoff |
| `lo.Debounce` / `lo.Throttle` | Rate limiting |
| `lo.ChannelDispatcher` | Fan-out to multiple channels |

- **[Package Guide](./references/package-guide.md)** — detailed package comparison and decision flowchart
- **[API Reference](./references/api-reference.md)** — complete function catalog
- **[Advanced Patterns](./references/advanced-patterns.md)** — composition, stdlib interop, iterator pipelines

## Watch for

| Mistake | Fix |
| --- | --- |
| `lo.Contains` when `slices.Contains` exists | Use stdlib `slices` / `maps` helpers since Go 1.21+ |
| `lop.Map` on 10 items | Use `lo.Map` — `lop` pays off at ~1000+ CPU-bound items |
| Assuming `lo.Filter` mutates input | `lo` is immutable — use `lom.Filter` for in-place |
| `lo.Must` in request handlers | Use the error variant and handle it |
| Eager chains on large data | Use `loi` lazy iterators to cut allocations |
| Dropping errors from transforms | Use `MapErr` / `FilterErr` / `ReduceErr` to stop on first error |

## Cross-references

- → See `samber-ro` for reactive/streaming pipelines over infinite event streams
- → See `samber-mo` for monadic types (Option, Result, Either) that compose with transforms
- → See `go-data-structures` for choosing the underlying data structure
- → See `go-performance` for profiling methodology before switching to `lom`/`lop`
- → See `go-concurrency` for `errgroup` I/O fan-out (not `lop`)
