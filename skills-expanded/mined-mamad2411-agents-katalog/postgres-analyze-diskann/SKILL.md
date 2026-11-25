---
name: postgres-analyze-diskann
description: Analyze DiskANN-based vector indexing/search on Azure Database for PostgreSQL Flexible Server when supported by the deployed Azure extension/version, including index configuration, memory/storage tradeoffs, recall, latency, and workload fit. Use for Azure-specific high-scale vector search.
---

# Analyze DiskANN

1. Verify DiskANN support for the exact Azure PostgreSQL version, region, and extension configuration before proceeding.
2. Identify vector dimensions, distance metric, data volume, filters, latency target, and recall target.
3. Inspect index build/runtime configuration and resource requirements.
4. Compare with supported pgvector alternatives such as HNSW when appropriate.
5. Measure retrieval quality and latency using representative queries.
6. Do not assume upstream pgvector and Azure-specific DiskANN capabilities are identical.

## Output
- Support/Version Check
- Vector Workload
- Index Configuration
- Recall/Latency Tradeoffs
- Recommended Action
