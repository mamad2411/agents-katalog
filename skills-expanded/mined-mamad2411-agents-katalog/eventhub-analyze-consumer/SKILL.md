---
name: eventhub-analyze-consumer
description: Analyze Azure Event Hubs consumer behavior including consumer groups, EventProcessorClient-style processing, partition ownership, load balancing, checkpointing, retries, lag, duplicate processing, and scaling. Use for stalled consumers, reprocessing, lag, checkpoint, or load-balancing incidents.
---

# Analyze Consumer

1. Identify consumer application, consumer group, checkpoint store, instance count, and processing model.
2. Inspect partition ownership, load balancing, checkpoints, processing failures, retries, and lag.
3. Compare active processor instances with partition count and ownership distribution.
4. Check checkpoint cadence and failure behavior.
5. Evaluate duplicate-processing and idempotency handling.
6. Distinguish consumer slowness from Event Hubs capacity or downstream dependency failures.
7. Do not reset checkpoints unless explicitly authorized.

## Output
- Consumer Topology
- Partition Ownership
- Checkpoint/Lag Findings
- Duplicate/Retry Risks
- Recommended Action
