---
name: postgres-analyze-pgvector
description: Analyze pgvector on Azure Database for PostgreSQL Flexible Server, including vector schema, dimensions, distance operators, HNSW and IVFFlat indexes, filtering, recall/latency, ingestion, and RAG retrieval. Use for PostgreSQL vector-search design or incidents.
---

# Analyze pgvector

1. Identify embedding model/version, dimensions, vector column type, similarity metric, filters, and retrieval objective.
2. Inspect vector index type and parameters supported by the deployed pgvector/Azure PostgreSQL versions.
3. Evaluate exact versus approximate search and representative recall/latency.
4. Correlate metadata filtering with index/query behavior.
5. Separate embedding quality, retrieval configuration, reranking, and generation problems.
6. Verify Azure-specific vector/index capabilities before recommending features beyond standard pgvector.

## Output
- Vector Schema
- Index/Search Configuration
- Recall/Latency Evidence
- Filtering/RAG Findings
- Recommended Action
