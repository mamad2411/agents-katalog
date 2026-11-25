---
name: memory-leak-hunt
description: Hunt a memory leak by heap-diffing over time and attributing the growing allocation. Use when a process's heap/RSS grows monotonically under steady load — never bump the memory limit to hide it.
kind: skill
pack: performance
allowed-tools: [Read, Grep, Glob, Bash]
---

# memory-leak-hunt

Diff the heap over time, attribute the growing retained set, fix the source, confirm the heap goes flat. Never guess, never bump the limit to make the alert stop.

## Premise

A process whose heap/retained-set grows monotonically under steady load has a leak. Hunt it by heap-diffing over time and attributing the growing allocation — not by reading code and guessing, not by raising the memory limit. Every finding cites the growing object type / allocation site from a captured snapshot diff (dominator or retained-size delta between two snapshots taken under the same steady load), and the retaining path that keeps it alive. "Unbounded cache" requires the snapshot showing that collection's retained size climbing across snapshots, plus the code site that inserts without eviction. No "this looks like it might leak" without two snapshots and a growing delta.

## Halt conditions

- Refuse to declare a leak without at least two heap snapshots under steady load showing a monotonic growth in a specific retained set — a single snapshot only shows a moment, not a trend.
- Refuse to name a source without the retaining path (dominator chain / GC roots → the object) that proves what holds it.
- Halt if the "steady load" wasn't actually steady — growth under rising traffic is expected working-set, not a leak. Hold load flat.
- Don't accept "raise the limit" / "add a periodic restart" as a fix — those hide the leak, they don't close it.
- Don't propose the fix as done until a soak run shows the heap flat (see confirming the fix).

## When to use

- RSS/heap climbs monotonically and never recovers after GC under flat traffic.
- Eventual OOM-kill, restart-loop, or container-memory alert firing on a long-running process.
- GC thrash — CPU rising and pauses lengthening as the live set grows.
- After a feature ship correlated with a slow upward memory trend on the dashboard.
- `memory-growth-scan` (this pack) hands over a candidate its deterministic test cannot isolate: take its `<file:line>`, class and suspected key as the starting hypothesis, and confirm or refute it with the snapshot diff.

## Prerequisites

- A way to hold load steady (constant RPS / constant job rate) — the same generator used for `profile-endpoint` works.
- Two or more heap snapshots taken at spaced intervals under that steady load.
- Enough runtime (or accelerated allocation) that the leak accumulates visibly between snapshots.

## Symptom signature

- **Monotonic RSS/heap growth** under flat load — the giveaway. Working set plateaus; a leak does not.
- **Sawtooth that trends up** — GC reclaims some, but the floor rises each cycle.
- **Eventual OOM / restart-loop** — the process dies, restarts, climbs again on the same schedule.
- **GC thrash** — collector runs more often and longer as it fails to reclaim the growing live set.

## Adapt to the runtime

| Runtime | Snapshot / diff tooling |
|---|---|
| Node | `node --heapsnapshot-signal=SIGUSR2` or `v8.writeHeapSnapshot()` for three snapshots of the same workload, then `memlab analyze unbound-object --snapshot-dir <dir>` (memlab 2.0.5, MIT) or Chrome DevTools "Comparison" view; `--inspect` for an interactive session. `clinic heapprofiler` is optional — clinic 13.0.0 (2023-06) is not actively maintained and may misreport on current Node |
| Python | `tracemalloc` (`take_snapshot()` + `compare_to()`), `memray` (flamegraph + `--leaks`), `objgraph.show_growth()` / `show_backrefs()` |
| JVM | Heap dump (`jmap -dump` / `jcmd GC.heap_dump`) into Eclipse MAT (dominator tree + leak-suspects report), `async-profiler` alloc mode for allocation sites |
| Go | `pprof` heap profile (`go tool pprof -inuse_space`) + `-alloc_space`; diff two profiles with `-base`; watch `runtime.MemStats.HeapInuse` |
| Ruby | `ObjectSpace.dump_all` + heap diff, `derailed exec perf:mem` / `perf:objects`, `memory_profiler` |

## Technique — heap-diff over time

1. Reach steady state: warm the process, then hold load flat.
2. Snapshot A once the working set has plateaued (baseline live set).
3. Keep the SAME steady load running for a fixed interval (minutes, or long enough for the leak to accumulate).
4. Snapshot B (and optionally C at a further interval).
5. Diff B against A: sort by retained-size / dominator-size delta. The leak is the type/collection whose retained set grew the most and keeps growing into C.
6. Attribute: from the top growing object, walk the retaining path (dominator chain / back-references / GC roots) to the code that holds it — the allocation site plus the reference that never releases.

## Common leak sources

- **Unbounded cache / map** — inserts with no eviction, no TTL, no max-size. The classic. Retained size of the map climbs snapshot over snapshot.
- **Event listener / subscription / closure capture not released** — `addListener` / `subscribe` / `on(...)` with no matching `remove` / `unsubscribe` / `off`; the closure pins everything it captured.
- **Module-level / global collection appended-to forever** — a package-level slice/list/dict that only ever grows (metrics buffer, "recent items", dedupe set).
- **Connection / timer / interval not cleaned up** — sockets, DB connections, `setInterval`/timers, goroutines/threads that never exit; each pins its own retained graph.
- **Detached object graph** — a subtree logically discarded but kept alive by one stray reference from a live root (a cache entry, a closure, an event registry). In a browser this is the classic detached-DOM leak; server-side it is the same shape without the nodes.

## Detectors

The static detectors are `memory-growth-scan`'s (this pack): unbounded process-lifetime containers (§1), listeners and subscriptions never removed (§2), timers, intervals and goroutines that outlive their owner (§3), and the rest of its §4–§9. This skill adds the runtime one: a soak showing a non-flat heap — the retained set still climbing after the working set should have plateaued — and the retaining path that names the source.

## Confirming the fix

The leak is closed only when a soak run proves it — same steady load, run long, and the heap goes flat: the retained set plateaus and stays there across the whole soak, GC reclaims back to a stable floor, and no OOM/restart. Take a final snapshot at the end of the soak and confirm the previously-growing collection is now bounded. A shorter run or a lower limit is not confirmation.

## Output (illustrative)

```
Leak hunt — worker service, steady 200 jobs/min

Symptom: RSS 180MB → 640MB over 40min, flat load, no plateau; OOM-kill at ~1GB.

Snapshots (heap comparison A@5min vs B@25min vs C@40min):
  Map<string, Session>  retained  62MB → 210MB → 340MB   ← growing, unbounded
  Buffer (job payloads) retained  18MB →  22MB →  23MB   (working set, stable)

Retaining path (dominator chain):
  GC root → sessionCache (module-level Map) → Session → socket → payload buffers
  Insert site: session-cache.ts:41  cache.set(id, session)   — no delete, no TTL, no max size

Root cause: sessionCache grows one entry per job, never evicted.

Fix: bound the cache — LRU with max 10k entries + TTL on idle sessions.

Confirmation (soak, same load, 60min after fix):
  RSS 180MB → 205MB → 205MB   flat.  sessionCache retained plateaus at 41MB. No OOM.
```

## False positives / gotchas
- Growth under RISING traffic is working-set expansion, not a leak — hold load flat before judging.
- A lazy cache warming to its steady size looks like a leak for the first few minutes — wait for the intended plateau before snapshot A.
- One snapshot can't prove a leak; you need the trend across two+ under the same load.
- Raising the memory limit or adding a nightly restart moves the OOM out further — it is not a fix and will mask the next regression.
- Fragmentation (RSS high, heap live-set flat) is an allocator issue, not a leak — check live-set, not just RSS.

## Boundary

`profile-perf`'s Memory + GC axis diagnoses a single snapshot — allocation rate and GC pressure at one moment. THIS skill is the over-TIME leak-hunt discipline: two-or-more snapshots under steady load, the growing-retained-set diff, and the flat-heap soak that confirms the fix. When the Memory + GC axis flags climbing memory, hand the subject here for the time-series hunt.

## Related

- `memory-growth-scan` — the static front end: it finds the candidates and proves what a deterministic count can; this skill attributes what it cannot isolate.
- `profile-endpoint` — the steady-load generator it uses to baseline an endpoint is the same one that holds load flat here.
- `@performance-optimizer` — invoked to design the bounded replacement (LRU, TTL, ring buffer) once the source is attributed.
- `@caching-architect` — owns the eviction/TTL policy for the cache that was leaking.
- Cross-pack `backend` — bounded caches are a backend contract; a cache added there must ship with an eviction bound so it never becomes this skill's finding.
