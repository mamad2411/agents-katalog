# History-Semantic Module

Embedding-backed semantic search over the file-based conversation history store.

- Wraps scope-scoped `ConversationHistory` with `SemanticHistoryStore`.
- Keeps the sidecar index next to `index.json` in the history directory.
- Registers itself as the history provider selected by config.
- `SemanticIndexManager` owns index load, reconciliation, ranking, background
  update failure handling, persistence, and reindex lifecycle. This module
  retains only conversation document/filter/result mapping.

## Boundaries

- Does not change canonical `index.json` or per-conversation `<id>.json` files.
- Adapter fingerprint is each conversation's `updatedAt` timestamp.
- Reindex on demand via `kota history reindex`.
- Without module config, keyword search remains available through the default
  provider.
