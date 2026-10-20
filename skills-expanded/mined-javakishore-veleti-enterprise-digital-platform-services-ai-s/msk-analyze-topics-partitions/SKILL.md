---
name: msk-analyze-topics-partitions
description: Analyze Amazon MSK topic and partition architecture, replication, partition distribution, retention, ordering, hot partitions, and managed topic operations. Use for topic design, partition skew, replication, or scaling investigations.
---

# Analyze Topics and Partitions

1. Identify topics, partition counts, replication factors, partition keys, and retention requirements.
2. Inspect distribution and leader/replica placement where available.
3. Detect hot partitions, uneven storage, and ordering constraints.
4. Evaluate partition growth against broker/capacity design.
5. Use AWS-native topic management APIs where supported by the target MSK capability; otherwise use appropriate Kafka administration tooling.
6. Preserve business ordering and durability requirements.

## Output
- Topic Topology
- Partition Distribution
- Replication/Retention Findings
- Hotspot Risk
- Recommended Action
