---
name: postgres-analyze-query
description: Analyze PostgreSQL query performance on Azure Flexible Server using EXPLAIN/EXPLAIN ANALYZE, pg_stat_statements where enabled, logs, query plans, statistics, indexes, sorts, joins, and resource evidence. Use for slow-query investigations.
---

# Analyze Query Performance

1. Identify exact query shape, parameters, database/schema, workload context, and latency.
2. Inspect query statistics and `EXPLAIN`; use `EXPLAIN ANALYZE` only when production impact is acceptable.
3. Evaluate scans, joins, row estimates, sorts, spills, parallelism, and returned versus processed rows.
4. Correlate plan behavior with indexes, table statistics, compute, memory, and storage.
5. Distinguish query inefficiency from server saturation or lock waits.
6. Do not apply query/index changes without validation.

## Output
- Query Shape
- Plan Evidence
- Cardinality/Resource Findings
- Bottleneck
- Recommended Action
