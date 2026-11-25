---
name: embedding-systems
version: 1.0.0
min_mindforge_version: 10.5.0
status: stable
triggers: embedding system design, vector database architecture, semantic search implementation, embedding pipeline, similarity algorithm, vector index optimization, vector embedding model selection, vector similarity search, dense vector retrieval, embedding dimension reduction, hybrid search design, vector store scaling
compose:
  - rag-architecture
---

# Embedding Systems & Vector Databases

## When this skill activates

This skill activates when designing semantic search systems, implementing vector databases, building dense retrieval pipelines, or optimizing embedding-based similarity search. It applies to any system where AI must find semantically related content (documents, images, code) using vector representations.

## Mandatory actions when this skill is active

### Before writing any code

1. **Select embedding model** — Choose based on modality (text: sentence-transformers, OpenAI ada-002; code: CodeBERT, StarCoder; images: CLIP; multimodal: CLIP, ImageBind) and performance requirements (dimension size vs. accuracy trade-off, encoding speed, cost). Validate model on your domain data before committing.
2. **Design vector schema** — Define embedding dimensions (384, 768, 1536), metadata fields (timestamps, tags, source IDs), and filtering constraints. Schema changes require full reindexing. Get it right upfront.
3. **Choose vector database** — Evaluate based on scale (millions vs. billions of vectors), query latency requirements (<100ms for real-time, <1s for batch), indexing strategy (HNSW, IVF, Product Quantization), and ecosystem (Pinecone, Weaviate, Qdrant, Milvus, pgvector). Run benchmarks on your data before selecting.
4. **Establish similarity metrics** — Select distance function: cosine similarity (most common, normalized), dot product (unnormalized, faster), Euclidean distance (position-sensitive). Different metrics produce different rankings. Test which aligns with human judgment.

### During implementation

- **Normalize embeddings consistently** — Always L2-normalize embeddings before storage if using cosine similarity. Unnormalized embeddings produce incorrect rankings. Validate normalization: check that ||embedding|| = 1.0 for all vectors.
- **Batch encode for efficiency** — Encode embeddings in batches (32-256 examples) to maximize GPU utilization. Single-example encoding wastes 90%+ of GPU compute. Implement batching with dynamic padding to handle variable-length inputs.
- **Design hybrid search** — Combine dense retrieval (semantic similarity) with sparse retrieval (BM25, TF-IDF keyword matching). Hybrid search outperforms either alone: semantic search finds conceptually similar content, keyword search ensures exact term matches are included. Fuse rankings with reciprocal rank fusion (RRF).
- **Implement metadata filtering** — Support filtering by metadata (date ranges, categories, tags) before or after vector search. Pre-filtering (filter then search) is faster but less accurate. Post-filtering (search then filter) is more accurate but slower. Choose based on selectivity (how many vectors match the filter).
- **Optimize index parameters** — Tune HNSW parameters (M, efConstruction, efSearch) for your accuracy/latency trade-off. Higher M and efConstruction improve accuracy but slow indexing. Higher efSearch improves query accuracy but slows search. Benchmark with your data.
- **Handle embedding drift** — Embedding models change (model updates, fine-tuning). When embeddings change, you must reindex all vectors. Implement versioned indexes: maintain old index while building new index, then hot-swap. Monitor query quality after model changes.

### After implementation

- **Validate recall accuracy** — Measure recall@k: for a set of ground-truth similar pairs, what percentage are in the top-k search results? Target: recall@10 >90%. If lower, increase k, tune index parameters, or use a better embedding model.
- **Benchmark query latency** — Measure p50, p95, p99 latency under realistic load (queries per second, index size). Target: p95 <100ms for real-time search. If higher, scale horizontally, optimize index, or use approximate search (lower accuracy, higher speed).
- **Test edge cases** — Query with empty strings, extremely long texts, rare languages, special characters. Ensure system degrades gracefully (return empty results, not crashes). Validate that out-of-domain queries (content very different from training data) still return sensible results.
- **Monitor index size and cost** — Track storage cost (GB per million vectors), indexing throughput (vectors/second), and query cost ($/1000 queries). Embedding systems can become expensive at scale. Optimize dimension size (use dimension reduction if accuracy is acceptable).

## Self-check before task completion

- [ ] Embedding model is selected and validated on domain-specific data
- [ ] Vector schema (dimensions, metadata, filters) is defined and documented
- [ ] Vector database is chosen based on benchmarks with realistic data scale and latency
- [ ] Similarity metric (cosine/dot product/Euclidean) is selected and justified
- [ ] Embeddings are L2-normalized before storage (if using cosine similarity)
- [ ] Batch encoding is implemented with dynamic padding for efficiency
- [ ] Hybrid search combines dense (semantic) and sparse (keyword) retrieval with RRF fusion
- [ ] Metadata filtering is implemented with pre/post-filtering strategy documented
- [ ] Recall@10 is validated at >90% on ground-truth similar pairs
- [ ] Query latency p95 is <100ms under realistic load
- [ ] Edge cases (empty queries, long texts, out-of-domain) are tested and handled gracefully
- [ ] Storage cost, indexing throughput, and query cost are measured and acceptable
