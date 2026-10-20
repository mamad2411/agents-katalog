---
name: eventhub-analyze-partitioning
description: Analyze Azure Event Hubs partition count, partition key strategy, event distribution, ordering requirements, hot partitions, scale constraints, and producer routing. Use for new stream design, uneven partition traffic, ordering requirements, or partition-related performance problems.
---

# Analyze Partitioning

1. Identify event hub, partition count, producer behavior, partition key, and ordering requirements.
2. Inspect partition-level ingress, egress, lag, and skew when available.
3. Evaluate:
   - key cardinality
   - distribution balance
   - ordering guarantees
   - hot partition risk
   - future scale requirements
4. Distinguish broker capacity limits from producer-created skew.
5. Treat partition-count changes as architectural decisions because partition topology has lifecycle constraints.
6. Preserve business ordering semantics when recommending changes.

## Output
- Partition Topology
- Distribution Evidence
- Ordering Assessment
- Hot Partition Risk
- Recommended Strategy
