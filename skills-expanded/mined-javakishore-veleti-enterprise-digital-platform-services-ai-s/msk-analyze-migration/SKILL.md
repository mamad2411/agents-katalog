---
name: msk-analyze-migration
description: Analyze migrations to or between Amazon MSK clusters, including source Kafka/MSK topology, target cluster type, replication, topic/config compatibility, client cutover, offsets, validation, and rollback. Use for self-managed Kafka-to-MSK, MSK-to-MSK, or architecture migration planning.
---

# Analyze Migration

1. Inventory source and target cluster topology, Kafka versions, topics, partitions, replication, security, and clients.
2. Identify replication/copy strategy such as MSK Replicator or other supported migration tooling.
3. Plan producer and consumer cutover, offset handling, schema dependencies, and DNS/bootstrap changes.
4. Define validation for data completeness, ordering, lag, and application behavior.
5. Define rollback before cutover.
6. Do not execute production cutover unless explicitly authorized.

## Output
- Source/Target Topology
- Compatibility Gaps
- Replication/Cutover Plan
- Validation/Rollback
- Recommended Sequence
