---
name: mongodb-analyze-indexes
description: Analyze MongoDB indexes including compound, partial, sparse, TTL, text, wildcard, multikey, unique, and hidden indexes, usage, selectivity, sort coverage, storage cost, and redundancy. Use for index design or performance investigations.
---

# Analyze Indexes

1. Inventory relevant indexes and query shapes.
2. Evaluate prefix ordering, selectivity, filter/sort coverage, multikey behavior, and uniqueness requirements.
3. Inspect index usage and identify redundant or unused candidates cautiously.
4. Evaluate partial, TTL, wildcard, text, or specialized indexes only when workload semantics require them.
5. Consider write amplification, memory, and disk cost.
6. Do not drop or build production indexes without explicit authorization.

## Output
- Index Inventory
- Query Coverage
- Redundancy/Gaps
- Write/Storage Impact
- Recommended Action
