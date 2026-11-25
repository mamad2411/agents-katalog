---
name: rag-pipeline-design
description: Designs retrieval-augmented generation with sensible chunking, embeddings, reranking and cited answers. Use it when an LLM must answer from your documents.
---

# RAG pipeline design

Retrieval quality sets the ceiling. Measure it before tuning the prompt.

## Steps

1. Inspect the corpus: formats, size, languages, update frequency, tables and images, and access rules per document. Decide how updates and deletions will flow in.
2. Write 20 or more test questions with the document and passage that answers each. Include a few that have no answer. This is the retrieval test set.
3. Chunk by structure, not by fixed length alone: split on headings and paragraphs, target 200 to 500 tokens, add 10 to 15 percent overlap, and keep tables whole. Prepend the document title and section path to each chunk.
4. Store metadata with each chunk: source URL, title, section, date, and permission tags. Filter on permissions in the query, never after generation.
5. Retrieve hybrid: vector search plus keyword search (BM25), merged by reciprocal rank fusion. Fetch about 30 candidates.
6. Rerank the candidates with a cross-encoder or a reranking API and keep the top 5 to 8.
7. Generate with instructions to answer only from the supplied passages, to quote the chunk ID for each claim, and to say "not found" when the passages do not answer.
8. Measure recall at k and the share of answers whose citations support the claim. Change one thing at a time.

## Rules

- Never mix document text into the system instructions without marking it as untrusted data.
- Do not embed secrets or restricted documents into a shared index.

## Report

The design with each choice and its reason, the test set results, and the likely failure modes.
