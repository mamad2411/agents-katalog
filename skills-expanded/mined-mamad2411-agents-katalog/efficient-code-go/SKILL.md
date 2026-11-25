---
name: efficient-code-go
description: Applies when writing or reviewing Go code. Extends the core efficient-code principles with Go-specific rules around slice growth and leaks, strings.Builder, interface boxing, escape analysis, defer cost, range-copies, sync.Pool for transient buffers, and pprof discipline.
---

# Efficient Code — Go

This skill assumes you also have the core `efficient-code` skill active.

## Stdlib primitives

- **`slice` (`[]T`)** — pointer + len + cap. `make([]T, 0, n)` preallocates. `append` is amortized O(1) with a growth factor around 2× below 1024 and ~1.25× above.
- **`map[K]V`** — hash map, average O(1). `make(map[K]V, n)` preallocates buckets.
- **`strings.Builder`** — zero-copy string assembly. **`s += t` in a loop is O(n²)** because strings are immutable. Use `Builder`.
- **`bytes.Buffer`** — mutable byte buffer for building `[]byte`.
- **`strings.Join(parts, sep)`** — O(n) when the count is known.
- **`sync.Pool`** — per-P free list for reusable objects; great for transient buffers. Pooled items may be reclaimed between GC cycles — never assume one specific object comes back.
- **`container/list`** — linked list; almost never the right choice (cache-hostile).
- **`sort.Slice`** uses reflection. For hot paths prefer **`slices.Sort`** (Go 1.21+ generics) or a typed `sort.Interface`.
- **`sync.Map`** — optimized for caches with stable key sets and many readers. For write-heavy workloads, a plain `map` + `sync.Mutex` is faster.
- **`context.Context`** — cancel/timeout propagation; passing it is cheap.

## Go-specific gotchas

1. **Slice growth & leaks:** re-slicing does NOT copy — it shares the backing array. Holding a small sub-slice of a huge array keeps the whole array alive. Copy to a fresh slice when subslicing a large buffer long-term.
2. **`copy(dst, src)` copies `min(len(dst), len(src))`** — you must pre-size `dst`, not pre-cap.
3. **`for i, v := range slice` COPIES each element into `v`.** For large structs use `for i := range slice; use slice[i]`. Same for `range map`.
4. **`range` on a channel blocks until the channel is closed.**
5. **Strings are immutable `[]byte` views.** `[]byte(s)` copies; `string(b)` copies. Avoid round-tripping.
6. **Interface boxing:** assigning a value type to an `interface{}` / `any` allocates a heap box (except tiny addressable cases). `any` parameters in hot paths cost allocations.
7. **Escape analysis:** a local escapes to the heap when its address is taken and it outlives the function — returning `&x`, capturing in an escaping closure, storing in an interface, etc. Use `go build -gcflags="-m"` to see the compiler's decisions.
8. **Goroutines are cheap (~2 KB stack) but leak if the receiver blocks forever.** Always have a cancellation or timeout path.
9. **Channels are not free.** Unbuffered channels force a rendezvous; buffered channels add a mutex + ring buffer. For fan-in/fan-out with tight timing, measure vs mutex-guarded slices.
10. **`defer` has a small cost** (~35-50 ns historically, much cheaper in 1.14+ with open-coded defers). Avoid in the tightest loops.
11. **Maps with pointer-free key/value types have a fast path.** Mixing pointers adds GC barriers per write.
12. **Map iteration order is randomized intentionally.** Do not rely on it.
13. **Method receivers:** pointer receivers avoid copying the struct; value receivers copy each call.
14. **Zero values are always valid.** No need to initialize fields to their zero value explicitly.
15. **`_, ok := m[k]` is one lookup.** `if _, ok := m[k]; ok { v := m[k] }` is two — use `if v, ok := m[k]; ok` instead.
16. **Benchmark flakiness:** `go test -bench` results vary with `GOMAXPROCS` and GC pressure. Set `GOGC` and pin CPUs for stable runs.
17. **Inlining is limited by function budget.** Runtime/reflect/interface calls often block inlining.
18. **Go has no generics-specialized containers in stdlib pre-1.21.** Since Go 1.21 the `slices` and `maps` packages are generic and faster than reflective alternatives.

## Profiling

`go tool pprof` is built in. `go test -cpuprofile=cpu.prof`, then `go tool pprof -http=:8080 cpu.prof` opens a flame graph in the browser.

## Sources

- https://go.dev/blog/slices-intro
- https://go.dev/doc/effective_go
- https://go.dev/blog/pprof
- https://go.dev/ref/spec
- https://github.com/golang/go/wiki/Performance
