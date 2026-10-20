---
name: cosmosdb-analyze-indexing
description: Analyze Azure Cosmos DB indexing policies, included/excluded paths, composite indexes, spatial/vector/full-text indexes, write overhead, and query coverage. Use when queries are expensive, indexing policy changes are proposed, or write RU cost may be index-related.
---

# Analyze Indexing

1. Read current container indexing policy and affected query patterns.
2. Determine which paths and index types each workload actually requires.
3. Inspect included/excluded paths, composite indexes, and specialized indexes when applicable.
4. Evaluate both read benefit and write RU/storage overhead.
5. Correlate missing-index symptoms with query diagnostics.
6. Do not remove indexes without checking all known query consumers.

## Output
- Current Index Policy
- Query Coverage
- Missing/Excess Index Findings
- RU Tradeoffs
- Recommended Policy Changes
