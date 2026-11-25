---
name: cosmosdb-analyze-partitioning
description: Analyze Azure Cosmos DB partition key design, logical partition distribution, hot partitions, cardinality, storage growth, query routing, hierarchical partition keys, and scale risks. Use for new container design, hot partition diagnosis, uneven RU consumption, or partition-key review.
---

# Analyze Partitioning

1. Identify container, current partition key, expected data volume, write/read distribution, and top query patterns.
2. Inspect partition-level metrics when available.
3. Evaluate:
   - cardinality
   - write distribution
   - read locality
   - hot-key risk
   - storage concentration
   - cross-partition query frequency
   - hierarchical partition key applicability
4. Distinguish a poor partition key from a temporary traffic hotspot.
5. Treat partition-key changes as schema/migration decisions; do not propose them casually.

## Output
- Partition Key Assessment
- Distribution Evidence
- Hot Partition Risk
- Query Impact
- Recommended Partition Strategy
