---
name: cosmosdb-analyze-change-feed
description: Analyze Azure Cosmos DB change feed and Change Feed Processor behavior, including leases, continuation, lag, scaling, duplicate processing, retries, ordering expectations, and downstream event-driven workflows. Use for real-time processing or event-driven integration issues.
---

# Analyze Change Feed

1. Identify source container, processor/consumer, lease container, mode, and downstream system.
2. Inspect processor health, lease ownership, lag/backlog indicators, retries, and failures.
3. Evaluate idempotency and duplicate-processing handling.
4. Check partition scaling and processor-instance distribution.
5. Correlate change-feed timing with downstream Kafka/Event Hub/service behavior when applicable.
6. Do not reset leases or checkpoints unless explicitly authorized.

## Output
- Change Feed Topology
- Processor/Lease State
- Lag/Failure Evidence
- Delivery Semantics Findings
- Recommended Action
