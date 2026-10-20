---
name: postgres-analyze-indexes
description: Analyze PostgreSQL indexes on Azure Flexible Server including B-tree, GIN, GiST, BRIN, partial, expression, covering, unique, and vector indexes, usage, bloat, selectivity, redundancy, and write cost. Use for index design or performance investigations.
---

# Analyze Indexes

1. Inventory relevant indexes and query patterns.
2. Evaluate index type, column order, selectivity, predicates, INCLUDE columns, and operator support.
3. Inspect usage, size, duplication, and bloat evidence.
4. Consider write amplification and maintenance cost.
5. Route vector indexes to `postgres-analyze-pgvector`.
6. Do not drop or build production indexes without explicit authorization.

## Output
- Index Inventory
- Query Coverage
- Redundancy/Bloat
- Write/Storage Impact
- Recommended Action
