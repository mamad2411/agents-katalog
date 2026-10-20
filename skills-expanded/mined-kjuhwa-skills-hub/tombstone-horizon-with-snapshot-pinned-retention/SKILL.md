---

name: tombstone-horizon-with-snapshot-pinned-retention
description: Tombstones can only be GC'd once no snapshot or reader lease still needs them, tracked via a monotonic horizon watermark.
category: algorithms
triggers:
  - tombstone horizon with snapshot pinned retention
tags: [algorithms, tombstone, horizon, snapshot, pinned, retention]
version: 1.0.0
---

# tombstone-horizon-with-snapshot-pinned-retention

The naive tombstone GC bug: delete the tombstone as soon as compaction runs, and any in-flight snapshot or replay reader that started before compaction now sees the key *resurrect* because the original value is gone but the tombstone that hid it is also gone. The fix is a horizon watermark — each active snapshot/reader registers its start offset, and the tombstone-retention horizon is `min(registeredOffsets)`. Compaction may only physically drop a tombstone whose offset is strictly less than the horizon.

Implement as a small registry: `snapshots: Map<snapshotId, baseOffset>` with register/release, and a derived `horizon()` that returns the min (or `Long.MAX_VALUE` if empty). Compaction iterates keys and keeps the tombstone if `tombstoneOffset >= horizon()`. Two subtle bits: (1) the horizon must be computed *before* compaction begins and held for the duration — if it advances mid-compaction you're fine (more aggressive), but if it retreats you have a race, so forbid retreats by making release only remove, never replace; (2) long-lived snapshots create unbounded retention, so expose the horizon as a metric and alert when it lags current-tail by too much.

```
class TombstoneHorizon {
  register(id, offset) { snapshots.put(id, offset) }
  release(id) { snapshots.remove(id) }
  horizon() { return snapshots.values().min() ?? Long.MAX_VALUE }
}
compact(segment) {
  h = horizon.snapshot()
  for (entry in segment) {
    if (entry.isTombstone && entry.offset < h) drop()
    else keep()
  }
}
```
