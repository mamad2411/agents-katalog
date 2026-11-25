---
name: memory-leak-diagnosis
description: Locates memory leaks by measuring growth, comparing heap snapshots and tracing the reference that keeps objects alive, then fixes that reference.
---

# Memory leak diagnosis

Prove the growth, find the growing type, find what holds it. Do not change code before the third step.

## Steps

1. Establish growth. Run the workload in a loop (a script, a load tool or repeated UI action) and sample memory at fixed intervals after forcing garbage collection where the runtime allows it. Growth that persists after collection is a leak; a sawtooth that returns to baseline is not.
2. Take at least two heap snapshots, one after warm-up and one after many iterations. Use the platform's tool: Chrome DevTools or `node --inspect` with `--heapsnapshot-signal`, `tracemalloc` or `objgraph` in Python, `jmap` or JFR in Java, `pprof -inuse_space` in Go.
3. Compare the snapshots. Sort by count and by retained size; look for types whose count grows in step with iterations (for example 10,000 more `Session` objects after 10,000 requests).
4. For the growing type, read the retaining path from the GC root. Typical culprits: a module-level map or cache with no eviction, event listeners and timers never removed, closures capturing large objects, unbounded queues, per-request data stored in a global, and unclosed connections or streams.
5. State the cause in one sentence, naming the variable and the line.
6. Fix by releasing at the right moment: bound the cache (LRU or TTL), remove listeners on teardown, clear timers, use weak references only when ownership is truly unclear, close resources in `finally`.
7. Repeat steps 1 and 3 to show the count is flat.

## Rules

- Never raise the memory limit or schedule restarts as the fix.
- Do not take snapshots on production without asking; they pause the process and contain data.

## Report

Growth rate before and after, the leaking type, the retaining path, the fix and the measurement that proves it.
