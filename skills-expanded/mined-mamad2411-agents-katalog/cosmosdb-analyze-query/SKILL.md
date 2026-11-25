---
name: cosmosdb-analyze-query
description: Analyze Azure Cosmos DB for NoSQL queries for RU cost, cross-partition execution, scans, filters, ORDER BY, pagination, functions, continuation behavior, and query diagnostics. Use for slow or expensive queries, throttling, high RU consumption, or query-review tasks.
---

# Analyze Query

1. Identify the query, container, partition key, expected result size, and calling code path.
2. Capture query diagnostics and RU charge when available.
3. Check:
   - partition-key filtering
   - cross-partition execution
   - index utilization
   - expensive functions
   - ORDER BY and composite-index requirements
   - pagination/continuation behavior
   - result cardinality
4. Correlate query cost with workload frequency.
5. Do not optimize only for latency; include RU and scalability impact.

## Output
- Query Findings
- RU/Diagnostics Evidence
- Partition/Index Impact
- Recommended Query Changes
- Remaining Unknowns
