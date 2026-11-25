---

name: watermark-aligned-window-emitter
description: Emit windowed aggregates only when the minimum watermark across all input partitions advances past the window close edge.
category: algorithms
triggers:
  - watermark aligned window emitter
tags: [algorithms, watermark, aligned, window, emitter]
version: 1.0.0
---

# watermark-aligned-window-emitter

When building multi-partition stream aggregations, a single global watermark causes either premature emission (drops late data from lagging partitions) or indefinite stalls (one idle partition freezes all output). The reusable pattern is a per-partition watermark table with a min-reducer gate: each partition advertises its highest observed event-time, the operator tracks `globalWatermark = min(perPartitionWatermark)`, and a window closes only when `globalWatermark >= windowEnd + allowedLateness`. Idle partitions must advertise a synthetic "idle watermark" derived from wall-clock minus a grace interval, otherwise the min collapses to the stale value.

```
onEvent(p, e):
  perPartition[p] = max(perPartition[p], e.time)
  global = min(perPartition.values())
  for w in openWindows where w.end + lateness <= global:
    emit(w); close(w)

onIdleTick():
  for p in idlePartitions:
    perPartition[p] = max(perPartition[p], now() - idleGrace)
```

The gotcha is the idle-grace value: too small and you emit before slow partitions catch up; too large and idle partitions permanently stall output. A good default is `max(expectedSourceLag) * 2`. Expose per-partition watermark as a gauge so operators can see which partition is the min-holder — 90% of "why isn't my window firing" debugging collapses to "partition X is holding the min."
