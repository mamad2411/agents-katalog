---
name: eventhub-analyze-checkpointing
description: Analyze Azure Event Hubs checkpointing, checkpoint stores, offsets, partition ownership records, replay behavior, duplicate delivery risk, and failover implications. Use for lost progress, duplicate processing, replay, checkpoint-store, or geo-replication consumer issues.
---

# Analyze Checkpointing

1. Identify consumer group, checkpoint store, partition ownership strategy, and checkpoint cadence.
2. Inspect checkpoint freshness and partition ownership records.
3. Determine behavior after restart, scale-out, failover, or processor crash.
4. Evaluate duplicate processing and idempotency protection.
5. For geo-replicated scenarios, verify checkpoint strategy aligns with failover requirements.
6. Never delete or reset checkpoints without explicit authorization.

## Output
- Checkpoint Topology
- Offset/Ownership State
- Restart/Failover Behavior
- Duplicate/Loss Risk
- Recommended Action
