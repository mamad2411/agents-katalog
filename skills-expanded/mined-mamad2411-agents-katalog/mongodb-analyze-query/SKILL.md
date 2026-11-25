---
name: mongodb-analyze-query
description: Analyze MongoDB query performance using query shape, explain plans, execution statistics, profiler/current operations, targeting, sort behavior, document examination, and latency evidence. Use for slow queries or inefficient access paths.
---

# Analyze Query

1. Identify the exact query shape, collection, filters, projection, sort, limit, and workload context.
2. Inspect `explain()` execution evidence and compare returned vs examined documents/keys.
3. Identify collection scans, inefficient index scans, blocking sorts, excessive fetches, or shard scatter.
4. Correlate query behavior with concurrency, cache, storage, and application latency.
5. Recommend query or index changes only when evidence supports them.
6. Do not run expensive production explains without considering impact.

## Output
- Query Shape
- Execution Plan
- Examined/Returned Evidence
- Bottleneck
- Recommended Action
