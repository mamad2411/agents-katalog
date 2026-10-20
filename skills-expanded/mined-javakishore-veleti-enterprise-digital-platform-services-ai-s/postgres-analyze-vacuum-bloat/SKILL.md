---
name: postgres-analyze-vacuum-bloat
description: Analyze PostgreSQL autovacuum, dead tuples, table/index bloat, transaction ID age, freeze behavior, statistics maintenance, and workload impact on Azure Flexible Server. Use for bloat, vacuum, or table-maintenance incidents.
---

# Analyze Vacuum and Bloat

1. Identify affected tables/indexes, churn rate, dead tuples, relation size, and transaction age.
2. Inspect autovacuum/analyze activity and relevant server parameters.
3. Correlate vacuum pressure with long transactions, storage I/O, and query latency.
4. Distinguish table bloat from index bloat and stale statistics.
5. Recommend per-table tuning only when workload evidence supports it.
6. Do not run disruptive maintenance in production without explicit authorization.

## Output
- Vacuum State
- Bloat/Statistics Findings
- Root Contributors
- Performance Impact
- Recommended Action
