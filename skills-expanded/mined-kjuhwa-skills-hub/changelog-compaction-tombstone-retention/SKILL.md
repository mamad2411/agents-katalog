---

name: changelog-compaction-tombstone-retention
description: State-backend changelog topics need tombstone retention longer than compaction interval to survive consumer rebalance gaps.
category: backend
triggers:
  - changelog compaction tombstone retention
tags: [backend, changelog, compaction, tombstone, retention]
version: 1.0.0
---

# changelog-compaction-tombstone-retention

When backing operator state with a compacted Kafka topic (changelog pattern), a delete is a `null`-value tombstone. Log compaction eventually removes tombstones after `delete.retention.ms`, but if a consumer/operator rebalances *after* the tombstone is compacted away, it will replay the old pre-delete value and never see the delete — resurrecting zombie state. The pattern: set `delete.retention.ms` to at least `max(sessionTimeout, checkpointInterval) * 3` and never rely on default (24h) if your checkpoint cycle is longer.

```
# topic config for state changelog
cleanup.policy=compact
min.cleanable.dirty.ratio=0.1
delete.retention.ms=604800000   # 7d, >> checkpoint interval
segment.ms=3600000
```

The corollary: when you *do* want to prune state (e.g., TTL'd keys), emit the tombstone and then force-roll a segment before the operator can be considered safe to rebalance. Also, never compact on a topic where you replay from `earliest` as part of bootstrap — compaction can remove intermediate values your bootstrap logic depends on for audit reconstruction. Use a separate non-compacted audit topic for that, and keep the compacted topic as materialized current-state only.
