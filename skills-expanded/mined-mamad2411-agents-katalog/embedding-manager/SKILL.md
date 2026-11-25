---
name: embedding-manager
description: "Embedding generation, vector storage, similarity search optimization, and embedding model selection. Use when building or tuning embedding pipelines."
version: 1.0.0
platforms: [linux, macos]
---

# Embedding Manager

## What It Does
Manages the embedding lifecycle — from model selection and generation through storage, indexing, similarity search optimization, and monitoring. Supports dense embeddings (text, code, images), sparse embeddings (BM25, SPLADE), and multi-vector representations. Handles batch embedding generation, incremental updates, dimensionality reduction, and embedding drift detection.

## Iron Laws (NEVER violate)
1. **Model-task alignment** — Embedding model must be evaluated on YOUR task. General-purpose benchmarks don't guarantee task-specific performance.
2. **Dimension is a cost** — Higher embedding dimensions = higher storage cost, slower search, and diminishing returns. Benchmark before scaling up.
3. **Re-embed on model change** — Switching embedding models requires re-embedding the entire corpus. Mixing embeddings from different models = broken similarity.
4. **Normalize for cosine** — All embeddings used with cosine similarity must be normalized. Unnormalized embeddings produce incorrect rankings.

## Red Flags (STOP immediately)
- **Embedding drift** — Same text produces significantly different embeddings after model update → re-index required
- **Dimension mismatch** — Query embedding dimension ≠ index embedding dimension → search silently broken
- **Index degradation** — Search recall dropping over time → index needs rebuilding or parameter tuning
- **Token limit exceeded** — Documents longer than embedding model's max tokens silently truncated → information loss

## Common Rationalizations (self-deception)
- "Any embedding model works for any task" → Embedding models are task-specific. Code embeddings ≠ semantic search embeddings.
- "768 dimensions is fine for everything" → Many tasks achieve 95% of performance at 384 dimensions. Smaller = faster + cheaper.
- "Just use cosine similarity" → Dot product, Euclidean, and Manhattan distances have different properties. Choose deliberately.

## When To Use
- Selecting an embedding model for a specific task (semantic search, clustering, classification)
- Setting up vector storage and similarity search infrastructure
- Generating embeddings at scale (batch processing, incremental updates)
- Optimizing search performance (index tuning, dimensionality reduction, quantization)
- Monitoring embedding quality and detecting drift

## Human Partner Signals (escalate to human)
- **Model deprecation** — Current embedding model announced as deprecated → migration planning needed
- **Cost inflection** — Embedding generation costs exceeding budget → optimization or model switch needed
- **Privacy concern** — Embeddings may encode sensitive information → privacy review
- **Scale limit** — Vector index approaching hardware limits → architecture decision (sharding, cloud migration)

## Pipeline
1. Select: evaluate embedding models on task-specific benchmark (MTEB, BEIR, or custom)
2. Generate: batch-embed corpus with progress tracking, error handling, and rate limiting
3. Store: configure vector database index (HNSW, IVF, PQ) tuned for recall/latency tradeoff
4. Search: implement similarity search with metadata filtering and hybrid retrieval
5. Optimize: apply dimensionality reduction (PCA, Matryoshka), quantization (scalar, product)
6. Monitor: track recall@k, index size, query latency, embedding drift
7. Maintain: handle incremental updates, model migration, index rebuilding

## Verification Checklist
- [ ] Embedding model evaluated on task-specific benchmark before selection
- [ ] All embeddings normalized for cosine similarity
- [ ] Document truncation handled (no silent loss beyond token limit)
- [ ] Vector index parameters tuned for target recall@k and latency
- [ ] Incremental update pipeline tested (new documents added without full re-index)
- [ ] Embedding drift monitoring configured with alerting
- [ ] Batch generation handles rate limits and errors gracefully

## Related Skills
- `rag-architect` — Embeddings are the foundation of RAG retrieval
- `model-evaluator` — Evaluate embedding models with task-specific metrics
- `dataset-curator` — Curate evaluation datasets for embedding quality measurement
- `huggingface-hub` — Embedding model discovery and download
