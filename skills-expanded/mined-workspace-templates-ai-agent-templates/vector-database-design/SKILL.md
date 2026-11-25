---
name: vector-database-design
description: Chooses the index type, embedding dimensions, chunking and metadata filters for a vector store, with recall checked against a test set.
---

# Vector database design

Decide from data size, query shape and filters, not from what a tutorial used.

## Steps

1. Ask or measure: number of vectors now and in a year, update rate, query rate, latency target, and which filters every query needs (tenant, language, date, access level).
2. Pick the embedding model first. Note its dimensions and max input length. Higher dimensions cost memory and speed; test whether a truncated or smaller variant keeps recall.
3. Chunk by meaning: split on headings and paragraphs, 200 to 500 tokens, with small overlap. Store the source ID, position and title with each chunk.
4. Choose the index. Under about 100k vectors, exact search is often fast enough and has perfect recall. Beyond that use HNSW for low latency, or IVF with quantization when memory is the limit. Write down the tuning parameters (for HNSW: M, efConstruction, efSearch).
5. Design metadata: only fields you filter on, indexed, with fixed types. Enforce tenant and permission filters inside the query, never after retrieval.
6. Build a test set of 30 to 100 real questions with known correct chunks. Measure recall at 5 and 10 against exact search.
7. Add hybrid search (keyword plus vector) when queries contain names, codes or rare terms.

## Rules

- Never mix embeddings from two models in one index.
- Store the model name and version with every vector so you can re-embed later.

## Report

The chosen design with reasons, the parameters, and the measured recall and latency.
