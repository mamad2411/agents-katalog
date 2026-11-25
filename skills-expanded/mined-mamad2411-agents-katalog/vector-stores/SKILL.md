---
name: vector-stores
description: >
  Vector search for retrieval — choosing a store, indexing it, and getting relevant results back.
  Carries: pgvector vs Qdrant/Weaviate/Milvus/Chroma and when each earns itself, HNSW vs IVF and the
  recall/latency/build-time trade, why chunking dominates retrieval quality more than the embedding
  model does, hybrid search (BM25 + dense) with reciprocal rank fusion, reranking as the cheapest
  quality win, **metadata filtering as the tenancy control — enforced in the query, never in the
  prompt**, embedding-model versioning and the reindex it forces, and measuring retrieval separately
  from generation. Load when building or debugging RAG retrieval, choosing a vector store, tuning an
  index, or fixing "it returns the wrong documents". Triggers: vector database, vector store,
  embedding store, pgvector, Qdrant, Weaviate, Milvus, Chroma, FAISS, similarity search, ANN, HNSW,
  IVF, cosine similarity, chunking, chunk size, hybrid search, BM25, reranking, top-k, recall,
  metadata filter, namespace, reindex, RAG retrieval. Corpus governance is `data-governance.md`
  D7/D8; poisoning defence is `agent-security`; retrieval metrics are `agent-evaluation`.
---

# vector-stores — retrieval that returns the right documents, to the right tenant

**Pinned:** pgvector, qdrant, weaviate, milvus, chroma — unpinned · authored 2026-07 · run
`/skill-update vector-stores` once a store is chosen. Index-tuning defaults move between releases;
verify parameter names against the installed version.

> On-demand: load this when retrieval is the problem. The *governance* of what may be in a corpus is
> canon (`data-governance.md` `D7`, `D8`); the *design* question of poisoning and untrusted retrieved
> content is `agent-security` (`AI1`, `AI4`); scoring retrieval quality is `agent-evaluation`. This
> skill is the store and the query.

## When this applies

Choosing a vector store. Building or tuning an index. Debugging "it returns the wrong documents."
Adding a tenant boundary to retrieval. Changing embedding models.

## Choosing a store

**Start with pgvector if you already run Postgres.** One fewer system to operate, back up, secure,
and pay for; transactional consistency with the rows the vectors describe; and joins to your
metadata for free. It carries tens of millions of vectors comfortably. Teams routinely add a
dedicated vector database before they have the scale that justifies one.

| Store | Earns itself when |
|---|---|
| **pgvector** | You have Postgres. Metadata lives in the same query. Default answer |
| **Qdrant** | You need rich payload filtering at scale, and want a simple single-purpose service |
| **Weaviate** | You want built-in hybrid search and module-based embedding generation |
| **Milvus** | Genuinely large scale (10⁸+ vectors), and you can operate a distributed system |
| **Chroma** | Prototyping and local dev. Not the production answer |
| **FAISS** | A library, not a store — no persistence, no filtering, no multi-tenancy. Use inside a service that provides those |

The operational question matters more than the benchmark: who backs it up, who patches it, who
notices when it's down, and does it satisfy `platform-security.md` `P11` (not internet-reachable, not
default-credentialed — several vector stores ship with auth **off**).

## Index types — the trade you're actually making

Exact search (a flat scan) is perfect recall and linear cost. Approximate indexes buy latency with
recall, and the parameter names differ per store but the concepts don't:

| | HNSW | IVF (+PQ) |
|---|---|---|
| Structure | Navigable small-world graph | Inverted file over centroids |
| Build | Slow, memory-hungry | Fast, needs a training set |
| Query | Fast, excellent recall | Fast; recall depends on probes |
| Memory | High — the graph lives in RAM | Lower, especially with product quantization |
| Updates | Handles incremental inserts well | Degrades as data drifts from the centroids; retrain |
| Use when | Default. Most workloads | Very large collections, memory-constrained |

The knobs, and what they cost:

- **`m` / `ef_construction`** (HNSW build) — higher means better recall and a slower, larger index.
- **`ef_search`** (HNSW query) — the one to tune first. Raise it until recall is acceptable, then
  stop; it is a pure latency-for-recall dial, at query time, with no reindex.
- **`nlist` / `nprobe`** (IVF) — more probes, better recall, more latency.

**Measure recall against exact search on your own data before shipping.** Build a small ground-truth
set with a flat index and compare — a published benchmark on a different distribution tells you very
little, and an ANN index silently returning 70% recall looks exactly like a retrieval quality
problem you'll misattribute to the embedding model.

## Chunking dominates, and it's the thing people tune last

Retrieval quality is decided more by how documents are split than by which embedding model ranks
highest on a leaderboard. The failure modes:

- **Too large** — the chunk's embedding is an average of several topics and matches nothing
  precisely.
- **Too small** — the chunk loses the context that made it meaningful ("it supports this" — what
  does?).
- **Split mid-structure** — a table cut in half, a code block severed, a heading orphaned from its
  section.

What works: split on **document structure** (headings, sections, paragraphs) rather than a fixed
character count; overlap adjacent chunks modestly; **prepend the document title and section path to
each chunk** before embedding, so a chunk carries its own context; and keep the chunk's source,
offset, and heading in metadata so a citation can point at something real.

Store the raw text alongside the vector. You will need to re-embed, and re-fetching the source is
the expensive part.

## Hybrid search and reranking — the two cheapest quality wins

**Dense retrieval alone misses exact matches.** Product codes, error identifiers, function names,
and rare proper nouns are exactly what users search for and exactly what embeddings blur. Run BM25
(or the store's keyword index) alongside vector search and fuse the results — **reciprocal rank
fusion** is a few lines, needs no tuning, and works:

```python
def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:                       # e.g. [dense_ids, bm25_ids]
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)
```

**Then rerank.** Retrieve generously (k=50–100) with the cheap methods, and rerank with a
cross-encoder to get the final 5–10. A cross-encoder sees the query and document *together* and is
substantially more accurate than any bi-encoder similarity; it is too slow to run over the whole
corpus, which is exactly why the two-stage shape works. This is usually a bigger quality jump than
changing embedding models.

## Tenancy — the security-critical part

Canon `D8`: **enforced in the query, never in the prompt.** The retriever must be structurally
incapable of returning another tenant's chunk.

```python
# WRONG — the model is asked to be a security control, and the breach already happened
results = store.search(query_vec, top_k=10)
prompt = f"Only use documents belonging to {tenant}. Context: {results}"

# RIGHT — the filter is part of the query; the tenant comes from the authenticated context
results = store.search(
    query_vec, top_k=10,
    filter={"tenant_id": ctx.tenant_id},        # never a client-supplied parameter (I4)
)
```

Stronger still where the store supports it: **a collection, namespace, or partition per tenant**, so
a missing filter returns nothing rather than everything. Physical separation beats a predicate that
one code path can forget.

Two things to verify rather than assume:
- **Does filtering happen before or after the ANN search?** Post-filtering can return fewer than
  `top_k` results, or — depending on implementation — leak the existence of filtered documents
  through counts and timing. Pre-filtering is what you want; check your store's behaviour.
- **Test cross-tenant retrieval as a negative test in CI.** Testing only as a privileged user finds
  nothing (`agent-evaluation`, `testing`).

## Embedding versions and reindexing

**The embedding model is part of the index's schema.** Vectors from two models are not comparable,
and mixing them silently degrades results rather than erroring.

- Record the model id and version in the collection's metadata (`model-governance.md` `M14`).
- **Changing the model means a full reindex**, not an incremental update. Budget for it: a
  dual-write or blue/green collection, a recall comparison against the old one on a fixed query set,
  then a cutover (`reliability.md` `R3`).
- A provider silently updating a hosted embedding model is the same event without the warning —
  another reason to pin.

## Gotchas

- **Normalise, and match the metric.** Cosine similarity on unnormalised vectors is not cosine
  similarity. Confirm whether your store normalises for you; the symptom of getting it wrong is
  mediocre-but-plausible results, which is the hardest kind to notice.
- **`top_k` chosen by feel.** Too few starves the generator of context; too many bury the relevant
  chunk and burn tokens. Tune it against a retrieval metric (`agent-evaluation`), not by reading a
  few outputs.
- **No metric for "retrieval failed".** If the right document isn't in the corpus at all, that is
  *context insufficiency*, not a model failure — and only measuring retrieval separately tells them
  apart.
- **The store shipped with authentication off.** Several do (`P11`). Check before it's reachable
  from anywhere.
- **Deletion that stops at the source.** Removing a document does not remove its embeddings — canon
  `D10`, and the one that turns a deletion request into a compliance failure.
- **Chunks with no provenance.** Without source, offset, and heading in metadata, you cannot cite,
  audit, or selectively delete (`D7`).
