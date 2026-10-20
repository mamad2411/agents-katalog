# Semantic Index Module

Shared embedding-index engine used by provider modules that add semantic
search to KOTA's file-based stores.

## Contract

- Embedding providers are OpenAI and Voyage through an OpenAI-compatible
  `/embeddings` API.
- The sidecar cache stores version, model, adapter fingerprint, and dense
  embedding per indexed item.
- The sidecar is explicitly rebuildable cache data: reads decode its version,
  model, entry fingerprints, and finite vectors; malformed or stale documents
  become cache misses. Writes are atomic. Canonical stores must not copy this
  recovery policy because their malformed data is operator-visible failure.
- `SemanticIndexManager` is the single production owner for lifecycle behavior:
  background embedding, cosine ranking, bulk reindex, deletion cleanup,
  staleness checks, lazy fill, in-memory cache lifecycle, and query error propagation.
- Store adapters own entry mapping (id, fingerprint, indexable text), canonical
  enumeration, persistence identity (storage directories), and mapping exceptions.
  Provider interfaces expose supported operations through their typed capability
  properties; the index manager does not maintain a second capability catalog.
- Semantic providers never mutate the canonical store and never embed
  synchronously in the write path.

Consumer modules provide a `SemanticStoreAdapter` and implement their owning
store's public provider interface around the manager. This module registers no
provider; it is only the shared capability pack.
