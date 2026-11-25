---
name: rag-pipeline
description: Use when building retrieval-augmented generation. Covers chunking strategy, embedding choice, vector stores, hybrid + reranking retrieval, prompt assembly, and evaluating retrieval and answer quality.
---

# RAG Pipeline

## Overview

RAG grounds an LLM in your data by retrieving relevant context at query time. Most RAG quality problems are **retrieval** problems, not generation problems — if the right chunk isn't retrieved, no prompt can save the answer. Optimize retrieval first.

## When to use

- The model must answer over private/large/changing documents.
- You need citations and reduced hallucination.
- Fine-tuning is overkill or data changes too often.

## Pipeline stages

1. **Ingest & chunk** documents.
2. **Embed** chunks → vector store.
3. **Retrieve** (dense + sparse) for a query.
4. **Rerank** top candidates.
5. **Assemble** prompt with context + citations.
6. **Generate** and **evaluate**.

## Chunking

- Start at **~500-1000 tokens with ~10-15% overlap**.
- Prefer **semantic/structural** boundaries (headings, paragraphs) over fixed char counts.
- Keep metadata (source, title, section, URL) on every chunk for citations and filtering.

## Embeddings & store

- Choose an embedding model by your domain + the MTEB leaderboard; match it at query and index time.
- Normalize vectors; use **cosine** similarity.
- Vector stores: pgvector (already have Postgres), Qdrant/Weaviate/Milvos (scale), FAISS (local/offline).

## Hybrid retrieval + reranking (the biggest quality lever)

```python
# 1. Dense (semantic) + 2. Sparse (BM25 keyword) -> union
dense_hits  = vstore.search(embed(query), k=20)
sparse_hits = bm25.search(query, k=20)
candidates  = dedupe(dense_hits + sparse_hits)

# 3. Cross-encoder rerank for precision
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
ranked = sorted(candidates,
                key=lambda c: reranker.predict([(query, c.text)]),
                reverse=True)[:5]
```

## Prompt assembly

- Insert only the top-k reranked chunks; respect the context window.
- Instruct: *"Answer only from the context; if it's not there, say you don't know."*
- Require **inline citations** to chunk metadata so answers are auditable.

## Evaluation (measure both halves)

- **Retrieval:** recall@k, MRR, hit-rate on a labeled query→chunk set.
- **Answer:** faithfulness/groundedness, answer-relevance, context-precision (e.g., RAGAS).
- Keep a fixed eval set; track scores via experiment-tracking as you tune chunking/k.

## Pitfalls

- **Dense-only retrieval** misses exact keywords/IDs — add BM25.
- **Chunks too large** dilute relevance; **too small** lose context.
- **Mismatched embedding models** at index vs query time.
- **No reranker** → low precision context → confident wrong answers.
- **No retrieval eval** → you tune blind.

## Hand-off

A retriever + generator with a measured retrieval/answer score that model-serving exposes behind an API.
