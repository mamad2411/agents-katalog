---
tags: [backend, second, aggregation, snapshot, merge]
name: second-aggregation-snapshot-merge
description: Per-second metric aggregation using in-memory counters + Flux.interval snapshot-and-reset + bounded parallel publish, to decouple request latency from downstream health.
trigger: Need 1-second-resolution metrics (TPS, error counts, response-time histograms) without hitting Kafka/DB per event; counter registries with periodic drain.
source_project: lucida-domain-apm
version: 1.0.0
category: backend
---

# Per-Second Aggregation — Snapshot & Merge

Producers increment in-memory counters on the hot path. A scheduler ticks once per second, atomically snapshots the counters, resets them, and publishes the batch downstream.

## Why

Aggregating per-event on the hot path (every request → Kafka) saturates the broker and couples request latency to downstream health. Moving to per-second aggregation decouples the two: the hot path only bumps a `LongAdder`; publish rate is fixed at 1 Hz per aggregator instance regardless of load.

`snapshotAndReset` (read-and-clear atomically) keeps buckets aligned with ticks and avoids double-counting across tick boundaries.

## Pattern

```java
Flux.interval(Duration.ofSeconds(1))
    .map(tick -> counterRegistry.snapshotAndReset()) // Map<Key, Counter>
    .flatMap(snapshot -> Flux.fromIterable(snapshot.entrySet())
                             .flatMap(this::publish, 50), // max 50 in-flight
             1)                                            // one snapshot at a time
    .subscribe();
```

## Steps

1. Hot path writes to `ConcurrentHashMap<Key, LongAdder>` — zero I/O per event.
2. Scheduler ticks once per second via `Flux.interval`.
3. On tick, atomically swap the map for a fresh one and return the old one (`snapshotAndReset`).
4. Publish entries with bounded concurrency (`flatMap(..., 50)`) so in-flight sends can't explode.
5. Log `drainedCount`, `elapsedMs`, and `inflight` at DEBUG — late ticks need to be diagnosable.
6. Capture the `Disposable` from `subscribe()` so you can dispose on shutdown.

## Counter / Caveats

- The bucket boundary is "when the tick fires", not a clean wall-clock second; in-flight events may land in either bucket. Fine for dashboards, wrong for billing.
- If a tick is delayed (GC pause), the next may cover >1s of events. Publish the snapshot's start/end timestamps; don't trust wall-clock alone.
- Back-pressure: if downstream can't keep up, `Flux.interval` buffers internally — either bound explicitly or drop old snapshots.
- Don't `subscribe()` and forget — without a captured `Disposable`, shutdown can't stop the loop cleanly.
