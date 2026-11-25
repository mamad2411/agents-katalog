---
name: cosmosdb-analyze-full-text-hybrid-search
description: Analyze Azure Cosmos DB full-text and hybrid search design, including full-text policy/indexes, BM25-style lexical ranking where supported, vector retrieval, rank fusion, filters, and RAG search behavior. Use for keyword, full-text, or hybrid vector-plus-text retrieval workloads.
---

# Analyze Full-Text and Hybrid Search

1. Identify full-text fields, policy/index configuration, vector configuration, and target retrieval behavior.
2. Inspect lexical and vector query components separately before evaluating hybrid ranking.
3. Evaluate filters, top-k choices, ranking behavior, RU/latency, and relevance.
4. Determine whether poor results originate from text indexing, vector retrieval, ranking, or application query construction.
5. Preserve grounding/relevance requirements when recommending optimization.

## Output
- Search Configuration
- Lexical Findings
- Vector Findings
- Hybrid Ranking Assessment
- Recommended Action
