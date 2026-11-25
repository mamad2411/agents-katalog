---
name: optimizing-query-by-id
description: |
  Optimizes Snowflake query performance using query ID from history. Use when optimizing Snowflake queries for:
  (1) User provides a Snowflake query_id (UUID format) to analyze or optimize
  (2) Task mentions "slow query", "optimize", "query history", or "query profile" with a query ID
  (3) Analyzing query performance metrics - bytes scanned, spillage, partition pruning
  (4) User references a previously run query that needs optimization
  Fetches query profile, identifies bottlenecks, returns optimized SQL with expected improvements.
---

# Optimize Query from Query ID

**Fetch query → Get profile → Apply best practices → Verify improvement → Return optimized query**

## Workflow

### 1. Fetch Query Details from Query ID
```sql
SELECT
    query_id, query_text,
    total_elapsed_time/1000 as seconds,
    bytes_scanned/1e9 as gb_scanned,
    bytes_spilled_to_local_storage/1e9 as gb_spilled_local,
    bytes_spilled_to_remote_storage/1e9 as gb_spilled_remote,
    partitions_scanned, partitions_total, rows_produced
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE query_id = '<query_id>';
```

Key metrics:
- `seconds`: Total execution time
- `gb_scanned`: Data read (lower is better)
- `gb_spilled`: Spillage indicates memory pressure
- `partitions_scanned/total`: Partition pruning effectiveness

### 2. Get Query Profile Details
```sql
SELECT * FROM TABLE(GET_QUERY_OPERATOR_STATS('<query_id>'));
```
Look for:
- Operators with high `output_rows` vs `input_rows` (explosions)
- TableScan operators with high bytes
- Sort/Aggregate operators with spillage

### 3. Identify Optimization Opportunities
| Metric | Issue | Fix |
|--------|-------|-----|
| partitions_scanned = partitions_total | No pruning | Add filter on cluster key |
| gb_spilled > 0 | Memory pressure | Simplify query, increase warehouse |
| High bytes_scanned | Full scan | Add selective filters, reduce columns |
| Join explosion | Cartesian or bad key | Fix join condition, filter before join |

### 4. Apply Optimizations
Rewrite the query:
- Select only needed columns
- Filter early (before joins)
- Use CTEs to avoid repeated scans
- Ensure filters align with clustering keys
- Add LIMIT if full result not needed

### 5. Get Explain Plan for Optimized Query
```sql
EXPLAIN USING JSON <optimized_query>;
```

### 6. Compare Plans
Compare original vs optimized:
- Fewer partitions scanned?
- Fewer intermediate rows?
- Better join order?

### 7. Return Results
Provide:
1. Original query metrics (time, data scanned, spillage)
2. Identified issues
3. The optimized query
4. Summary of changes made
5. Expected improvement

## Performance Thresholds
Use these to assess the query before and after optimization:

| Metric | Healthy | Needs Attention | Critical |
|--------|---------|-----------------|----------|
| Execution time | < 60s | 60–300s | > 300s |
| Data scanned | < 1 GB | 1–10 GB | > 10 GB |
| Partition pruning | < 25% scanned | 25–75% | > 75% |
| Spillage | 0 GB | < 5 GB local | > 5 GB or any remote |
| Row explosion (output/input) | < 2x | 2–10x | > 10x |

## Validation Checklist
- [ ] Original query metrics captured (time, GB scanned, spillage, partitions)
- [ ] GET_QUERY_OPERATOR_STATS analyzed for bottlenecks
- [ ] Optimization opportunities identified with severity
- [ ] Optimized query preserves identical results (same columns, rows, order)
- [ ] EXPLAIN plan compared: fewer partitions or intermediate rows
- [ ] Before/after metrics summarized for user
- [ ] Expected improvement estimated with specific numbers
