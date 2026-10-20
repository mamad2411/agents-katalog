---
name: rag-engineering
description: Build retrieval-augmented generation pipelines. Use when grounding
  LLMs in your data.
metadata:
  tags: rag, engineering
---

# RAG Engineering

## Use this skill when
- Designing chunking and embeddings
- Choosing a vector store and retrieval
- Evaluating retrieval quality

## Do not use this skill when
- Bare prompt techniques where retrieval is core
- Fine-tuning when RAG fits

## Instructions
1. Chunk documents by coherent boundaries with overlap.
2. Embed with a consistent model; store metadata for filtering.
3. Retrieve with hybrid search (vector + keyword) and rerank.
4. Build the prompt from retrieved context with citations.
5. Evaluate with relevance and answer-quality metrics.
6. Handle missing/out-of-date context honestly.
7. Keep cost/latency in line by ranking top-k sensibly.

## Checklist
- Hybrid search in place
- Evaluation golden set
- Citations supported

## Output Format
- Chunking | embeddings | store | retrieval | eval set

## Common Mistakes
- Naiive chunks with no overlap
- No evaluation set
- Ignoring stale/duplicate content
