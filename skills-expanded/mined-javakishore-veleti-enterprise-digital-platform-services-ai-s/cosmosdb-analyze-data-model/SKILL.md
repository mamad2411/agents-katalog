---
name: cosmosdb-analyze-data-model
description: Analyze Azure Cosmos DB document modeling, denormalization, item boundaries, relationship patterns, transactional scope, duplication tradeoffs, and access-pattern alignment. Use when designing or reviewing Cosmos DB data models for application workloads.
---

# Analyze Data Model

1. Read service and Cosmos DB metadata plus representative item shapes and access patterns.
2. Identify dominant reads, writes, transaction boundaries, and query paths.
3. Evaluate document boundaries, denormalization, duplication, embedded vs referenced data, item size, and transactional batch requirements.
4. Check whether the model aligns with the partition key and expected scale.
5. Avoid relational normalization assumptions that create cross-item or cross-partition joins.
6. Recommend model changes only when tied to concrete access patterns.

## Output
- Workload Model
- Data Modeling Findings
- Tradeoffs
- Partitioning Implications
- Recommended Design
