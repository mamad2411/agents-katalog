---
name: ai-rag-pipeline
version: 1.0.0
description: Design a retrieval-augmented generation pipeline covering chunking, embeddings, hybrid search, reranking, and retrieval evaluation.
author: matrixx0070
tags: [rag, retrieval, embeddings, reranking, eval]
---

## When to use

Use this when an LLM needs facts it was not trained on — internal docs, a knowledge base, changing data — and you must ground answers in retrieved passages with citations.

**Not for:** static knowledge already in the model, tasks needing reasoning over the WHOLE corpus at once (use a map-reduce summarizer), or deciding to fine-tune instead (see `ai-fine-tune-plan`).

## Method

1. Define the retrieval unit: what a single answer-supporting passage looks like. This drives chunking, not the reverse.
2. Chunk by structure (headings, sections) before falling back to fixed tokens. Decision point: prose → 300-500 tokens with ~15% overlap; code/tables → keep semantic units whole.
3. Add a contextual prefix to each chunk (document title + section + a one-line summary) before embedding. This alone cuts retrieval failures materially.
4. Embed with a current model; store vectors plus the raw text and metadata (source, section, timestamp).
5. Retrieve hybrid: dense (cosine) + sparse (BM25/keyword), then fuse with Reciprocal Rank Fusion. Decision point: exact IDs/error codes/names → weight sparse higher.
6. Rerank the top ~30 with a cross-encoder down to the top 3-5. Skip only if latency budget forbids it (see `ai-cost-latency`).
7. Build the prompt: retrieved passages + a rule to answer ONLY from them and cite, else say "not found".
8. Evaluate retrieval separately from generation: recall@k on a labeled query set BEFORE judging answers (see `ai-eval-harness`).

## Example

Query: "What is the timeout for the billing webhook?"

Dense search returns a "webhooks overview" chunk (topic match, no number). BM25 catches the chunk containing `BILLING_WEBHOOK_TIMEOUT=30s`. RRF fuses both; the reranker floats the config chunk to rank 1. The model answers "30 seconds" and cites `billing/config.md#timeouts`. Recall@5 measured at 0.92 on 40 labeled queries.

## Pitfalls

- **Chunk-then-think.** Picking 512 tokens before knowing what an answer needs. Design the retrieval unit first.
- **Dense-only.** Cosine similarity misses exact tokens (IDs, versions, error codes). Always add a sparse channel.
- **No retrieval eval.** Blaming the LLM when the right passage was never retrieved. Measure recall@k first.
- **Stale index.** Serving deleted/updated docs. Store timestamps and re-index on source change.

## Output format

```
# RAG Pipeline: <name>
RETRIEVAL UNIT: <what one passage is>
CHUNKING: <strategy | size | overlap>
CONTEXT PREFIX: <fields prepended before embedding>
EMBEDDING: <model | dim>
STORE: <vector db | metadata fields>
SEARCH: dense + sparse -> RRF (k=<n>)
RERANK: <model | top_in -> top_out>
GEN PROMPT: grounded-only + cite + "not found" fallback
EVAL: recall@<k>=<x> | answer grader=<y>
```
