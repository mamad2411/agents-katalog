---
name: eventhub-analyze-geo-replication
description: Analyze Azure Event Hubs geo-replication, primary/secondary regions, synchronous or asynchronous replication where applicable, replication lag, promotion readiness, checkpoint implications, and disaster-recovery behavior. Use for regional resilience, DR, replication lag, or promotion planning.
---

# Analyze Geo Replication

1. Resolve namespace tier, primary region, secondary regions, and replication mode.
2. Inspect replication health and lag when available.
3. Evaluate producer and consumer behavior during planned or forced promotion.
4. Verify checkpoint strategy and client SDK compatibility with failover design.
5. Assess potential duplicate or lost processing risks for asynchronous or forced transitions.
6. Do not promote/fail over a production namespace unless explicitly authorized.

## Output
- Region Topology
- Replication Mode/Health
- Lag and RPO Implications
- Consumer Checkpoint Readiness
- Recommended DR Action
