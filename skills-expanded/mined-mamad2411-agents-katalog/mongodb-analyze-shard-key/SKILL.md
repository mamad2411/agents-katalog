---
name: mongodb-analyze-shard-key
description: Analyze MongoDB shard key selection and runtime behavior, including ranged, hashed, and compound keys, cardinality, frequency, monotonicity, targeting, hot shards, jumbo-range risk, and resharding considerations. Use for distribution or scalability problems.
---

# Analyze Shard Key

1. Identify collection workload, current shard key, query patterns, write patterns, and distribution requirements.
2. Evaluate cardinality, frequency, monotonicity, and query targeting.
3. Inspect data and traffic distribution across shards.
4. Detect hot-key/hot-shard patterns and poorly targeted scatter-gather queries.
5. Evaluate refinement or resharding only with supporting evidence and version compatibility.
6. Preserve application ordering and uniqueness requirements.

## Output
- Current Shard Key
- Workload Fit
- Distribution/Targeting Findings
- Scaling Risk
- Recommended Action
