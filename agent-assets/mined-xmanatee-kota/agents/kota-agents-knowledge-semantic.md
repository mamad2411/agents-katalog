# Knowledge-Semantic Module

Embedding-backed semantic search over the file-based knowledge store.

- Wraps the default `KnowledgeStore` with `SemanticKnowledgeStore`.
- Keeps the sidecar index next to knowledge entries.
- Registers itself as the knowledge provider selected by config.
- `SemanticIndexManager` owns index load, reconciliation, ranking, background
  update failure handling, persistence, and reindex lifecycle. This module
  retains only knowledge document/filter/result mapping.

## Boundaries

- Does not change canonical markdown-plus-frontmatter entries.
- Adapter fingerprint is each entry's `updated` timestamp.
- Reindex on demand via `kota knowledge reindex`.
- Without module config, keyword search remains available through the default
  provider.
