---
name: cosmosdb-analyze-cost
description: Analyze Azure Cosmos DB cost drivers across RU consumption, autoscale/provisioned/serverless choices, regions, indexing, storage, backup, and workload patterns. Use when engineering teams need evidence-based Cosmos DB cost optimization without sacrificing required performance or resilience.
---

# Analyze Cost

1. Identify account regions, throughput mode, databases/containers, storage, and workload profile.
2. Inspect major cost drivers:
   - provisioned/autoscale RU
   - serverless consumption
   - multi-region footprint
   - index/write overhead
   - storage and backup
   - inefficient high-frequency queries
3. Separate architecture cost from avoidable workload inefficiency.
4. Preserve required SLO, consistency, and DR constraints.
5. Do not recommend cost reductions that weaken required resilience without explicitly stating the tradeoff.

## Output
- Primary Cost Drivers
- Supporting Evidence
- Optimization Opportunities
- Performance/Resilience Tradeoffs
- Recommended Priorities
