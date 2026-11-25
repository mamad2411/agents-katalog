---
name: build-vector-search
description: Builds semantic/vector search — pick an embedding model + dimensionality (and whether to truncate Matryoshka dims) and the matching distance metric (cosine/dot/L2, normalize to unit length so cosine == dot and IP is correct), an ANN index with the recall/latency/memory tradeoff understood (HNSW M/efConstruction/efSearch for low-latency RAM-resident; IVF-PQ nlist/nprobe/PQ for billion-scale compressed; flat/exact for <100k) in pgvector/Qdrant/Milvus/FAISS/Pinecone, chunking + overlap + per-chunk metadata for filtering, HYBRID retrieval fusing BM25 + dense by Reciprocal Rank Fusion (RRF, k≈60) not score addition, a cross-encoder/Cohere reranker over the top-50→k, correct pre-filter-vs-ANN interaction (filterable HNSW, not post-filter that starves k), and offline eval with recall@k / nDCG@10 / MRR against a labeled qrels set. Quantize (scalar/PQ) only after measuring recall loss; tune efSearch/nprobe to a recall target, not a guess.
when_to_use: Building or tuning the embedding + vector-index + retrieval-quality core — choosing an embedding model/dim/metric, sizing/tuning an HNSW or IVF-PQ index for a recall@k target, adding hybrid (BM25+vector via RRF) or a reranker, fixing pre-filtering that tanks recall, or running a recall@k/nDCG eval. Distinct from rag-pipeline (the full retrieve-augment-generate app — prompt assembly, grounding, citations, hallucination control; this skill is the retrieval engine it embeds) and design-search-index-infra (the lexical/inverted-index + cluster topology + zero-downtime reindex infra; this skill owns the embedding model, distance metric, ANN params, and relevance eval rather than shard/analyzer/capacity design).
---

## When to Use

Reach for this skill when the task is the **quality and mechanics of vector retrieval itself** — embeddings, the ANN index, hybrid/rerank, and measuring relevance:

- "Pick an embedding model + dimensionality + distance metric for semantic search"
- "Our ANN search misses obvious matches" / "tune HNSW/IVF for recall@10 without blowing latency"
- "pgvector / Qdrant / Milvus / FAISS / Pinecone — which index and what parameters?"
- "Add hybrid search (BM25 + vector) and a reranker" / "results are semantically close but wrong-ranked"
- "Filtering by metadata returns too few results / wrong ones" (pre-filter vs ANN)
- "How do I know retrieval got better?" → recall@k / nDCG / MRR eval
- "Quantize to fit in RAM" / "embeddings cost/latency too high"

NOT this skill:
- The end-to-end **retrieve→augment→generate** app — prompt assembly, context packing, grounding, citations, hallucination control → rag-pipeline (this skill is the retrieval core it calls; tune retrieval here, wire the LLM there)
- **Lexical/inverted-index** search infra — Elasticsearch/OpenSearch analyzers & mappings, shard/replica topology, capacity sizing, alias-based zero-downtime reindex → design-search-index-infra (it owns BM25 analyzer config + cluster ops; this skill owns the embedding model, metric, ANN params, and relevance eval)
- Measuring **LLM answer** quality (faithfulness, answer correctness, LLM-as-judge) → llm-eval-harness (this skill evals *retrieval* — recall@k/nDCG — not generation)
- Cutting **embedding/inference** cost & latency at the model/serving layer (batching, caching, model size) → optimize-llm-cost-latency
- The BM25/keyword half as a standalone full-text feature with no vectors → design-search-index-infra
- Picking a document/KV store schema unrelated to vectors → model-nosql-data; relational schema for the metadata table → design-relational-schema
- Profiling the corpus before indexing (length distribution, dupes, language mix) → profile-dataset

## Steps

1. **Pick the embedding model, dimensionality, and distance metric together — they're coupled.** Don't default to `text-embedding-ada-002` (legacy). 2025-2026 strong choices:

   | Model | Dim | Notes |
   |---|---|---|
   | OpenAI `text-embedding-3-large` | 3072 (truncatable to 256/1024) | Matryoshka — truncate then **re-normalize**; strong general |
   | OpenAI `text-embedding-3-small` | 1536 (truncatable) | cheap, good baseline |
   | Cohere `embed-v3` / `embed-v4` | 1024 | has `input_type` (query vs document) — use it |
   | `BAAI/bge-large-en-v1.5`, `intfloat/e5-large-v2` | 1024 | open, self-host; **require a prefix** (`query:` / `passage:`) — omitting it craters recall |
   | `BAAI/bge-m3` | 1024 | multilingual + multi-vector |
   | Voyage `voyage-3` | 1024 | strong retrieval, code/domain variants |

   Rules: **embed the query and the document with the SAME model** (and the right `input_type`/prefix). Higher dim ≈ better recall but more RAM/latency — Matryoshka models let you truncate (e.g. 3072→1024) and trade recall for cost; **re-normalize after truncating**. Metric choice:

   | Metric | Use when | pgvector op | Note |
   |---|---|---|---|
   | **Cosine** | text embeddings (default) | `<=>` (`vector_cosine_ops`) | direction only |
   | **Dot / inner product** | already unit-normalized vectors | `<#>` (negative IP) | == cosine when normalized; faster |
   | **L2 / Euclidean** | rarely for text; some image models | `<->` (`vector_l2_ops`) | magnitude matters |

   **Normalize embeddings to unit length once at write time**, then cosine == dot and you can use the faster IP path. Pick the index opclass to match the metric — a cosine index on un-normalized vectors silently mis-ranks.

2. **Chunk with structure, sized to the model, with overlap and metadata — bad chunks cap recall before any tuning.** Defaults: ~**256–512 tokens** per chunk, **10–15% overlap** (~50–80 tokens) so a fact split across a boundary survives. Split on **semantic boundaries** (headings, paragraphs, code blocks, `RecursiveCharacterTextSplitter` by separator hierarchy) — never a blind fixed char window mid-sentence. Stamp every chunk with metadata for filtering and citation: `{doc_id, chunk_id, source, title, section, page, created_at, tenant_id, lang}`. Consider **late chunking** (embed the long context, then pool per-chunk) or a parent-document retriever (embed small, return the larger parent) when chunks lose context. One vector per chunk; keep the raw text + metadata in a payload column/store.

3. **Choose the ANN index by corpus size and the recall/latency/memory tradeoff — there is no free lunch.**

   | Index | Recall | Latency | Memory | Build | Use when |
   |---|---|---|---|---|---|
   | **Flat / exact (brute force)** | 100% | O(N) | full | none | < ~50–100k vectors, or as the recall ground-truth |
   | **HNSW** | high | very low | **high (graph in RAM)** | slow | low-latency, RAM-resident, ≤ tens of millions |
   | **IVF / IVF-Flat** | tunable | low | medium | fast | large, want simple recall/latency knob (`nprobe`) |
   | **IVF-PQ / PQ** | lower (lossy) | low | **very low (compressed)** | medium | 100M–1B+, must fit RAM/budget; accept recall hit |
   | **DiskANN / Vamana** | high | low | on-disk | slow | billion-scale, can't fit graph in RAM |

   **HNSW knobs:** `M` (neighbors/node, 16–64; higher = better recall + more RAM), `efConstruction` (build quality, 100–400), `efSearch`/`ef` (**query-time** recall↔latency dial — raise until recall target met). **IVF knobs:** `nlist` (clusters ≈ `√N` to `4√N`), `nprobe` (clusters scanned at query — the recall↔latency dial). **PQ knobs:** `m` sub-quantizers (dim must be divisible), `nbits` (usually 8). Default to **HNSW** unless memory or scale forces IVF-PQ.

4. **Per-store specifics — same concepts, different syntax.**
   - **pgvector** (Postgres): `CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64);` then per-session `SET hnsw.ef_search = 100;`. IVFFlat: `WITH (lists = N)` + `SET ivfflat.probes = 10;` — **build IVFFlat AFTER loading data** (it clusters existing rows); HNSW can be built on empty. `pgvector` ≥0.7 supports `halfvec` (16-bit) to halve size. Pre-filter with a plain `WHERE` + a btree index — Postgres can combine.
   - **Qdrant:** HNSW by default; set `hnsw_config` (`m`, `ef_construct`) per collection, `ef` per search via `params.hnsw_ef`. **Payload indexes** on filtered fields enable *filterable HNSW* (filter applied during graph traversal, not after). Use scalar/product quantization via `quantization_config`.
   - **Milvus:** explicit `index_type` (`HNSW`, `IVF_FLAT`, `IVF_PQ`, `DISKANN`, `SCANN`) + `metric_type` (`COSINE`/`IP`/`L2`); search `params` = `{ef}` or `{nprobe}`. Must `load()` collection into memory before search.
   - **FAISS** (library, no server): `IndexHNSWFlat`, `IndexIVFFlat`, `IndexIVFPQ`; **train IVF/PQ on a representative sample** before `add`; `index.nprobe = N`. Wrap with `IndexIDMap` to keep external ids. You manage persistence + metadata yourself.
   - **Pinecone:** managed; pick `metric` at index creation (immutable), use **namespaces** for tenant isolation, `filter` in query for metadata. Serverless handles the index internals — you tune `top_k` and filters, not `M`/`nprobe`.

5. **Pre-filter correctly — naïve post-filtering starves your k and silently drops good hits.** Three interaction modes:

   | Mode | What happens | Risk |
   |---|---|---|
   | **Post-filter** (ANN then drop non-matches) | fetch top-k, remove rows failing the filter | a selective filter can leave **0–few** results; raise `k` won't reliably fix it |
   | **Pre-filter** (filter then exact search) | filter to a subset, brute-force within it | exact but slow on large subsets |
   | **Filterable ANN** (filter *during* graph/list traversal) | engine prunes by metadata inside HNSW/IVF | best — Qdrant payload index, Milvus filtered search, pgvector `WHERE` + index |

   For a highly selective filter (e.g. `tenant_id = X` with few rows), **pre-filter or partition** (separate collection/namespace/partition per tenant) instead of filtering a global index. **Always index the metadata fields you filter on**; an unindexed filter forces a slow scan or weak post-filter. Test recall *with the filter applied* — unfiltered recall lies.

6. **Add hybrid (BM25 + dense) and fuse with RRF — not score addition.** Dense embeddings miss exact terms (IDs, codes, rare names, acronyms); BM25/keyword catches them. Run both retrievers, take each result's **rank**, and fuse with **Reciprocal Rank Fusion**:

   ```
   RRF_score(d) = Σ_retrievers 1 / (k + rank_r(d))      # k ≈ 60
   ```

   RRF is rank-based, so you **don't have to normalize** the wildly different BM25 vs cosine score scales (raw weighted score-sum is the classic bug — one scale dominates). Native support: Qdrant `Query` API with `Fusion.RRF`, Elasticsearch/OpenSearch `rrf` retriever, Milvus `RRFRanker`, Weaviate hybrid `fusionType`. In pgvector, run a BM25/`tsvector` (or ParadeDB `pg_search`) query and a vector query, then fuse in SQL. Hybrid typically beats either alone on heterogeneous corpora.

7. **Rerank the shortlist with a cross-encoder — it fixes the ordering bi-encoders get wrong.** Retrieve a wide net (top **50–100** by RRF), then rerank to the final **k (5–10)** with a cross-encoder that scores (query, doc) jointly: **Cohere `rerank-v3.5`**, `BAAI/bge-reranker-v2-m3`, or a `cross-encoder/ms-marco-MiniLM` model. Cross-encoders are far more accurate but **O(candidates)** per query — only ever run them over the shortlist, never the whole index. Reranking usually buys more nDCG than squeezing the ANN, and it's where "semantically close but mis-ranked" gets fixed. Budget the extra ~50–300ms.

8. **Eval with a labeled set — tune to a recall TARGET, never by eyeballing.** Build qrels: a set of queries each with known-relevant `doc_id`s (mine from clicks/logs, or hand-label 50–200). Metrics:

   | Metric | Measures | When |
   |---|---|---|
   | **recall@k** | did the relevant doc make the top-k at all | the **ANN/retrieval** gate — most important for RAG (can't rerank what you didn't retrieve) |
   | **MRR** | rank of the *first* relevant hit | single-answer / "find the doc" |
   | **nDCG@10** | graded relevance + position | multi-relevant, ranking quality (post-rerank) |
   | **precision@k** | fraction of top-k relevant | when noise in context hurts |

   Compute **exact (flat) search as the recall=100% ground truth**, then measure your ANN's recall@k against it — that's how you set `efSearch`/`nprobe`: raise it until recall@k hits target (e.g. 0.95), then stop (latency grows past it). Re-run the suite on every model/chunk/param change. Tools: `ranx`, BEIR, `pytrec_eval`, or a small custom harness.

9. **Quantize only after measuring the recall loss — it's a memory/latency win that costs accuracy.** Options: **scalar quantization** (float32→int8, ~4× smaller, small recall loss — good default), **binary quantization** (1-bit, ~32× smaller, big loss — only with a rescoring/oversampling pass), **PQ** (product quantization, tunable, needs training). Pattern: quantize for the fast first pass, then **rescore the top candidates with full-precision vectors** (Qdrant `rescore`, Milvus refine) to recover recall. Measure recall@k before/after on the eval set — never ship a silent quality drop. Also: store the original embedding model + dim in metadata so a model upgrade triggers a full re-embed (you can't mix embedding spaces).

## Common Errors

- **Embedding query and documents with different models (or wrong `input_type`/prefix).** Vectors live in different spaces → garbage similarity. Fix: same model both sides; set Cohere `input_type`, E5/BGE `query:`/`passage:` prefixes.
- **Metric/opclass mismatch or un-normalized vectors with cosine/IP.** A cosine index on un-normalized vectors mis-ranks; IP on un-normalized ≠ cosine. Fix: normalize to unit length at write time, pick the matching opclass (`vector_cosine_ops` etc.).
- **Tuning by feel instead of to a recall target.** Picking `efSearch`/`nprobe` "that seems fine" hides recall cliffs. Fix: exact search as ground truth, raise the knob until recall@k ≥ target, then stop.
- **Post-filtering a selective metadata filter.** ANN returns k, the filter drops most → too few/empty results. Fix: filterable ANN (payload/`WHERE` index) or pre-filter/partition per tenant.
- **Weighted score-sum hybrid instead of RRF.** BM25 and cosine scales differ wildly; one dominates. Fix: fuse by rank with RRF (k≈60) — no score normalization needed.
- **Building an IVFFlat index before loading data.** It clusters on existing rows; empty → degenerate. Fix: load data, then build IVFFlat (HNSW is fine on empty).
- **No overlap / mid-sentence chunking.** Facts split across boundaries become unretrievable. Fix: 10–15% overlap, split on semantic boundaries.
- **Reranking the whole index.** Cross-encoders are O(N) per query → unusable latency. Fix: rerank only the top-50–100 shortlist.
- **Quantizing without measuring.** Silent recall drop in prod. Fix: measure recall@k before/after; add a full-precision rescore pass.
- **Mixing embedding spaces after a model upgrade.** New and old vectors are incomparable. Fix: store model+dim in metadata; re-embed the whole corpus on upgrade.
- **HNSW out-of-memory at scale.** The graph is RAM-resident; tens of millions × high `M` × float32 blows the budget. Fix: lower `M`, scalar-quantize, or switch to IVF-PQ / DiskANN.

## Verify

1. **Metric/normalization correct:** vectors are unit-normalized; the index opclass matches the metric; a known query returns its known-relevant doc as a top hit.
2. **Same-model invariant:** grep the pipeline — query and document embeddings use the identical model + correct `input_type`/prefix.
3. **Recall measured against exact search:** flat/brute-force gives the ground truth; ANN recall@k is computed and meets target (e.g. ≥0.95) at the chosen `efSearch`/`nprobe`, with latency recorded.
4. **Filter recall holds:** run the eval **with the production metadata filter applied**; recall doesn't collapse (no post-filter starvation), and selective filters use pre-filter/partition.
5. **Hybrid fuses by RRF:** BM25 and dense both contribute; fusion is rank-based (RRF k≈60), and hybrid recall@k ≥ either retriever alone on the eval set.
6. **Rerank improves nDCG, not latency-killing:** cross-encoder runs over the top-50–100 only; nDCG@10 improves vs pre-rerank; added latency is within budget.
7. **Chunking sound:** chunks are 256–512 tokens with 10–15% overlap on semantic boundaries, each carrying filter/citation metadata; a boundary-straddling fact is retrievable.
8. **Quantization is net-positive:** recall@k before/after quantization is measured; any drop is recovered by a full-precision rescore pass and is within tolerance.
9. **Index choice fits scale/memory:** the index type (flat/HNSW/IVF-PQ/DiskANN) matches corpus size and the RAM budget; HNSW graph fits in memory or a compressed index was chosen.

Done = query and documents share one normalized embedding model with a matching distance metric/opclass, the ANN index is chosen for the corpus's scale/latency/memory budget and tuned to a measured recall@k target against exact search, hybrid retrieval fuses BM25 + dense by RRF, a cross-encoder reranks the shortlist, metadata filtering uses filterable/pre-filter (not post-filter starvation), and every change is validated by the recall@k / nDCG / MRR eval in checks 3–8.
