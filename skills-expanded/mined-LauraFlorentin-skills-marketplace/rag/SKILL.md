---
name: rag
description: Design retrieval-augmented generation systems with ingestion, access control, chunking, hybrid retrieval, reranking, citations, freshness, and evaluation. Use when a user asks to build document search, grounded question answering, enterprise knowledge retrieval, semantic search, or a RAG pipeline.
---

# Retrieval-Augmented Generation

RAG can improve grounding only when the corpus, permissions, retrieval, and answer attribution are reliable. Retrieved text is evidence and untrusted input—not an instruction with higher authority.

## Ingestion

1. Authorize and inventory sources; preserve document, version, owner, permission, and date metadata.
2. Extract text while retaining headings, tables, pages, and stable citation anchors.
3. Chunk by semantic structure, then tune size and overlap empirically.
4. Index lexical and semantic representations when the corpus benefits from hybrid retrieval.
5. Define update, deletion, retention, and re-indexing behavior.

Apply document-level and row-level access control before or during retrieval, not after generation. Never place one tenant's private content in another tenant's candidate set.

## Query path

```text
authenticate and authorize
→ normalize or clarify query
→ retrieve candidates with permission filters
→ rerank and diversify
→ assemble bounded context with provenance
→ generate only supported claims
→ cite source anchors
→ return uncertainty or no-answer when evidence is insufficient
```

Defend against prompt injection in indexed documents: delimit retrieved content, ignore embedded instructions, restrict tools, and validate requested actions independently.

## Evaluation

Use a representative, versioned question set and measure retrieval recall, precision or ranking quality, answer correctness, citation correctness, groundedness, abstention, latency, cost, freshness, and permission leakage. Include ambiguous questions, conflicting sources, missing answers, stale documents, and adversarial content.

Do not prescribe a universal chunk size, top-k, similarity threshold, or index type. Tune from corpus structure and evaluation results.

## Output

Provide the corpus and permission model, ingestion design, retrieval and reranking strategy, context budget, citation format, no-answer behavior, evaluation plan, and operational update and deletion process.
