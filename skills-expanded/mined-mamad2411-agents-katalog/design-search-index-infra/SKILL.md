---
name: design-search-index-infra
description: Designs full-text and vector search infrastructure — Elasticsearch/OpenSearch mappings and analyzers, vector index parameters (HNSW M/efConstruction, IVF nlist/PQ), BM25+vector hybrid via RRF, offline relevance tuning, capacity/shard topology, and alias-based zero-downtime reindex.
when_to_use: Building or tuning a search backend — defining a text mapping (analyzers/tokenizers/multi-fields), sizing a vector index for recall-vs-latency-vs-memory, fusing lexical and vector into hybrid search, tuning relevance with offline eval, or planning a zero-downtime reindex. NOT for wiring an LLM retrieval/grounding flow (use rag-pipeline) or keeping the index synced from a DB log (use build-cdc-streaming-pipeline).
---

## When to Use

Reach for this when the request is about **the search index itself** — how documents are mapped, scored, and stored — not the application logic that calls it:

- "Set up a mapping/analyzer so partial-word and stemmed search works"
- "Add autocomplete / typeahead / search-as-you-type"
- "Pick HNSW vs IVF and size `M`/`efConstruction`/`nlist` for N million vectors"
- "Combine keyword (BM25) and semantic (embedding) search into one ranked list"
- "Search relevance is bad — boost titles, add synonyms, tune fuzziness"
- "Reindex 200M docs to a new mapping with no downtime"
- "How many shards/replicas, what refresh interval, how much heap for the HNSW graph?"

NOT this skill:
- Wiring an LLM to answer over the corpus (chunking → embed → retrieve → rerank → ground) → rag-pipeline (this skill builds the index that pipeline queries)
- Keeping the index in sync with a source DB as rows change → build-cdc-streaming-pipeline
- Tuning a relational `WHERE`/`JOIN`/`GIN` query plan in Postgres/MySQL → optimize-sql-query
- Putting a read cache in front of the search cluster → caching-strategy
- Measuring downstream *answer* quality of an LLM → llm-eval-harness

## Steps

1. **Classify the query workload first — it dictates index type. Do not vector-index everything.**

   | Workload | Example query | Index | Scoring |
   |---|---|---|---|
   | Exact / filter | `status=active`, `sku=ABC`, range, faceting | `keyword`/numeric, `doc_values` | none (constant) — wrap in `filter` (cached, no scoring) |
   | Full-text relevance | "wireless noise cancelling headphones" | `text` + analyzer | BM25 |
   | Autocomplete / prefix | "wir" → "wireless…" | `search_as_you_type` or edge-ngram | prefix match |
   | Semantic / fuzzy-intent | "thing to block out plane noise" | `dense_vector` (HNSW) | cosine/dot |
   | Filtered hybrid | semantic + `brand IN (...)` + `price<200` | text + vector + keyword | RRF fusion + filter |

   Most real search is the **last row**. Build all three field families in one index; choose per query, not per cluster.

2. **Full-text mapping — be explicit, never rely on dynamic mapping in prod.** Disable `dynamic` or set `"dynamic": "strict"` so a stray field can't silently become the wrong type. Per field decide: `text` (analyzed, for relevance) vs `keyword` (exact, for filter/sort/agg) — you almost always want **both** via multi-fields:

   ```json
   {
     "mappings": {
       "dynamic": "strict",
       "properties": {
         "title": {
           "type": "text",
           "analyzer": "english",                 // stemming + lowercase + stop
           "fields": {
             "raw":  { "type": "keyword" },        // exact match / sort / agg
             "ac":   { "type": "search_as_you_type" }, // typeahead
             "ngram":{ "type": "text", "analyzer": "edge_ngram_idx",
                       "search_analyzer": "standard" } // index edge-ngrams, query whole term
           }
         },
         "body":      { "type": "text", "analyzer": "english" },
         "brand":     { "type": "keyword" },
         "price":     { "type": "scaled_float", "scaling_factor": 100 },
         "embedding": { "type": "dense_vector", "dims": 768, "index": true,
                        "similarity": "cosine",
                        "index_options": { "type": "hnsw", "m": 16, "ef_construction": 128 } }
       }
     }
   }
   ```

   Rules: set `search_analyzer` ≠ index `analyzer` for edge-ngram (index n-grams, search the **whole** query term — otherwise the query is shredded too and precision collapses). Use `english`/language analyzers for stemming; keep a `.raw` keyword for anything you sort, aggregate, or exact-match. Set `"index": false` on fields you only display (saves space). Mapping is **immutable** — wrong type means reindex (step 7), so get it right now.

3. **Vector index — pick the algorithm by corpus size and recall target. Default HNSW; reach for IVF/PQ only when RAM-bound.**

   | Param | What it trades | Opinionated default |
   |---|---|---|
   | `m` (HNSW edges/node) | recall + memory ↑ vs build time | **16** (32 for high-recall >10M) |
   | `ef_construction` | build-time recall ↑ vs index speed | **128** (200 if recall short) |
   | `ef_search`/`num_candidates` | query recall ↑ vs latency | **100**, raise until recall@10 plateaus |
   | IVF `nlist` (partitions) | speed ↑ vs recall | **≈√N** vectors |
   | IVF `nprobe` (lists scanned) | recall ↑ vs latency | **nlist/20**, tune up for recall |
   | PQ (product quant.) | **memory ÷4–16** vs recall ↓ | only when graph won't fit RAM |

   - **HNSW** = best recall/latency, default for ≤ ~10M vectors per node. The graph lives in **RAM** — budget `~(dims*4 + m*8) bytes × N`; a 768-dim, 10M, m=16 index ≈ **31 GB** resident. If it won't fit, go IVF-PQ (FAISS/Milvus) or scalar-quantize (`int8_hnsw` in ES 8.x → ~4× smaller, recall ~unchanged).
   - **Distance must match how the model was trained.** Normalized embeddings (most sentence-transformers, OpenAI) → `cosine`, or `dot_product` if you pre-normalize vectors to unit length (skips the per-query magnitude divide → faster). Never `l2`/euclidean on cosine-trained vectors — silently wrong ranking, not an error.
   - `dims` must equal the model's output exactly. Truncating/padding to a "round" number breaks similarity.

4. **Hybrid — run BM25 and vector separately, then fuse with RRF. Do not just add raw scores.** BM25 (unbounded, ~0–30) and cosine (0–1) are different scales; summing lets one dominate. **Reciprocal Rank Fusion** uses rank position, not score:

   ```
   rrf_score(d) = Σ_q  1 / (k + rank_q(d))        // k=60 default, sum over each retriever
   ```

   Use ES `rank: { rrf: {...} }` / OpenSearch `hybrid` query, or compute RRF app-side over the two result sets. Weighted fusion (`α·norm(bm25) + (1-α)·cosine`) works **only if you min-max normalize each list first** and tune α offline (step 5); RRF needs no normalization and is the safer default.

   **Filtering is where hybrid breaks.** A post-filter (retrieve top-k vectors, *then* drop ones failing `brand`/`price`) can return **0 results** when matches sit at rank 5000 — the recall cliff. Push filters **into** the ANN search (`knn.filter` in ES, `filter` clause in Milvus/Qdrant) so the graph traversal only visits passing nodes. For very selective filters (<1% pass), ANN degrades to near-exhaustive — detect it and fall back to a **brute-force exact** vector scan over the pre-filtered set; it's faster than fighting the graph.

5. **Relevance tuning — change one lever, gate every change on an offline eval set. Never tune by eyeballing one query.**
   - Levers, in order of leverage: **field boosts** (`title^3 body^1`), **synonyms** (`synonym_graph` filter, expand at *search* time so you can edit without reindex), **fuzziness** (`AUTO` = 0 edits <3 chars, 1 <6, 2 else — never blanket `fuzziness:2`, it wrecks precision), `minimum_should_match`, phrase/proximity boosts, recency/popularity `function_score`.
   - Build a labeled judgment set (≥50 queries × graded docs) and gate with the **Ranking Evaluation API** (`_rank_eval`) or an offline harness. Metrics: **recall@k** (did we retrieve it at all), **P@k**, **NDCG@10** (rank quality with graded relevance). A change ships only if NDCG/recall **doesn't regress** on the set — local "looks better" is how you trade one query's win for ten silent losses.

6. **Capacity / topology — size shards to data, not to instinct.**
   - **Shard size 20–50 GB** each; target ≤ ~20 shards per GB of JVM heap; heap ≤ 31 GB (compressed-oops). Over-sharding (hundreds of tiny shards) is the #1 cluster-health killer — `shards = ceil(total_primary_GB / 40)`, round to your data-node count.
   - **Replicas ≥1** for HA and to scale **search** throughput (each replica serves queries); they don't help write throughput. Set `number_of_replicas: 0` during a bulk reindex, restore to ≥1 after — cuts reindex time ~2×.
   - **`refresh_interval`**: default `1s` is wasteful for write-heavy/bulk loads. Set **`30s`** (or `-1` during pure bulk, then restore) — controls the latency between index and searchability; raise it whenever you don't need sub-second freshness.
   - Vector graph memory is **separate from and on top of** BM25/heap budgeting (step 3) — size the box for resident HNSW graphs, not just heap.

7. **Lifecycle — alias-based zero-downtime reindex. The app NEVER names a concrete index.**
   Apps read/write the alias `products`, which points at `products-v1`. To change mapping/analyzer/`dims`:

   ```bash
   # 1. create v2 with the NEW mapping, replicas=0, refresh=-1 (fast bulk)
   PUT products-v2  { "settings": {"number_of_replicas":0,"refresh_interval":"-1"}, "mappings": {...} }

   # 2. backfill v1 -> v2 (async, throttled so you don't starve live traffic)
   POST _reindex?wait_for_completion=false  { "source":{"index":"products-v1","size":5000},
                                              "dest":{"index":"products-v2"} }
   # poll: GET _tasks/<taskId>   — bulk in 5–15k-doc batches; size by tuning until throughput plateaus, not by guessing

   # 3. restore prod settings, then ATOMIC alias swap (single request = no gap, no double-read)
   PUT products-v2/_settings { "number_of_replicas":1, "refresh_interval":"30s" }
   POST _aliases { "actions":[ {"remove":{"index":"products-v1","alias":"products"}},
                               {"add":   {"index":"products-v2","alias":"products"}} ]}
   # 4. keep v1 until v2 verified in prod, then delete
   ```

   **Catch-up writes during reindex:** rows changed *after* the `_reindex` snapshot are missed. Either dual-write to both indices during the window, or replay the change log from the snapshot timestamp — the source-of-truth → index sync is owned by **build-cdc-streaming-pipeline**; this skill only guarantees the swap is atomic.

## Common Errors

- **Dynamic mapping in prod.** First doc with a stringly-typed number makes the field `text`; later range queries silently match nothing. Set `"dynamic": "strict"`.
- **Wrong distance metric.** Indexing cosine-trained embeddings with `l2`/euclidean returns results — just in the wrong order, with no error. Match `similarity` to the model.
- **Summing BM25 + cosine scores raw.** Different scales; one retriever dominates. Use RRF, or min-max normalize each list before weighting.
- **Post-filtering vector results.** `knn` top-k then drop non-matching → empty or thin results when matches rank deep. Push the filter *into* the ANN search; brute-force exact for very selective filters.
- **`fuzziness: 2` on everything.** Matches "cat"→"car"→"can" — precision tanks. Use `AUTO` (edit distance scaled by term length).
- **Edge-ngram with the same analyzer at search time.** The query gets shredded into n-grams too, so "wire" matches "fire" via shared grams. Set `search_analyzer: standard` — index grams, search the whole term.
- **HNSW graph that doesn't fit RAM.** Once it spills to disk, query latency jumps 10–100×. Compute resident size *before* indexing; quantize (`int8_hnsw`) or go IVF-PQ if it won't fit.
- **Over-sharding.** 500 shards for 10 GB of data — each shard is a Lucene index with fixed overhead; cluster state bloats, GC thrashes. Aim 20–50 GB/shard.
- **Reindex with default `refresh_interval` and `replicas≥1`.** Every batch refreshes + replicates → reindex crawls. Set `refresh:-1, replicas:0` during, restore after.
- **App pinned to a concrete index name.** Any reindex is now downtime + a deploy. Always read/write through an alias from day one.
- **Tuning relevance on one query.** A title boost that fixes "iphone" can wreck "running shoes review." Gate every change on the offline eval set.

## Verify

- **Mapping is explicit & immutable-safe:** `GET <index>/_mapping` shows `dynamic: strict`, every searched field has the intended `type`/`analyzer`, and a `.raw` keyword exists for each sorted/aggregated field.
- **Analyzer does what you think:** `POST <index>/_analyze {"field":"title","text":"running shoes"}` emits the expected stemmed/lowercased/ngram tokens (e.g. `run`, `shoe`).
- **Vector metric & dims match the model:** `dims` equals the embedding model's output, `similarity` matches its training; a near-duplicate of an indexed doc returns itself as the #1 nearest neighbor.
- **Recall measured, not assumed:** kNN results compared against an exact brute-force scan on a sample → **recall@10 ≥ 0.95** at the chosen `ef_search`/`nprobe`; raise the param if below.
- **Hybrid beats either alone:** on the labeled judgment set, RRF NDCG@10 ≥ max(BM25-only, vector-only), and a query with a hard filter (`brand=X`) still returns relevant, filter-passing results (no recall cliff, no empty set).
- **Relevance change gated:** `_rank_eval` (or offline harness) shows NDCG@10 and recall@k did **not** regress vs the previous config across all judgment queries.
- **Topology sane:** shards are 20–50 GB each, heap ≤ 31 GB, `_cluster/health` is `green`, and HNSW graphs fit resident RAM (no disk spill in node stats).
- **Reindex was truly zero-downtime:** alias flipped in a single `_aliases` call, doc counts reconcile (`v2.count == v1.count + writes-during-window`), and live search returned 200s with no error spike across the swap.

Done = the index serves the target workload with explicit immutable-safe mapping, measured recall@10 ≥ 0.95 and a non-regressing NDCG@10 on the offline eval set, hybrid+filter returns no empty/cliffed results, and a mapping change can ship via an atomic alias swap with zero search downtime.
