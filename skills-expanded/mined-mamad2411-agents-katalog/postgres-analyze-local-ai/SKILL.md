---
name: postgres-analyze-local-ai
description: Analyze Azure local AI/embedding capabilities exposed through Azure Database for PostgreSQL Flexible Server when supported, including model availability, embedding generation, resource behavior, vector integration, and workload fit. Use for in-database/local embedding scenarios.
---

# Analyze Local AI

1. Verify the capability/extension exists and is supported for the exact Azure PostgreSQL region/version.
2. Identify model, embedding dimensions, SQL workflow, expected volume, and latency requirement.
3. Inspect resource and concurrency impact on database workloads.
4. Compare local embedding generation with external Azure AI services when architecture requires a tradeoff analysis.
5. Validate generated embeddings against the target vector index and retrieval pipeline.
6. Do not assume preview capabilities are production-ready without lifecycle verification.

## Output
- Capability/Lifecycle Status
- Model/Embedding Flow
- Resource Impact
- Retrieval Compatibility
- Recommended Action
