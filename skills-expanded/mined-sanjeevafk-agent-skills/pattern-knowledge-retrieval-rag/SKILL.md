---
name: pattern-knowledge-retrieval-rag
description: Augment model context with external factual retrieval through query reformulation, hybrid dense-sparse indexing, re-ranking, and citation grounding.
metadata:
  category: agent-architecture
  tier: production
  chapter: 14
  source: "Antonio Gulli: Agentic Design Patterns"
---

# Knowledge Retrieval (RAG) Pattern

## 1. Overview & Intent

Augment model context with external factual retrieval through query reformulation, hybrid dense-sparse indexing, re-ranking, and citation grounding.

> **Intent & Scope:** Use when models require private, domain-specific, or up-to-the-minute enterprise knowledge with anti-hallucination guarantees.

---

## 2. Architectural Blueprint

```
[User Query] --> [Query Rewriter] --> [Dense Vector + BM25 Sparse Search]
                                                  |
                                                  v
                                      [Cross-Encoder Reranker]
                                                  |
                                                  v
[Synthesis Prompt: Retrieved Passages + Citations] --> [Grounded Output]
```

---

## 3. Core Implementation Principles

- Rewrite and decompose user queries before querying vector databases.\n- Use hybrid search (Dense embeddings + BM25 sparse lexical) to catch semantic concepts and exact keywords.\n- Rerank top-k candidates with a cross-encoder to select the most relevant chunks.\n- Ground outputs with mandatory source citations and strict anti-hallucination system prompts.

---

## 4. Reference Implementation Pattern

```python
def hybrid_rag_pipeline(query: str, vector_store, reranker, llm):
    # Step 1: Hybrid retrieval
    dense_matches = vector_store.similarity_search(query, k=15)
    sparse_matches = vector_store.bm25_search(query, k=15)
    combined = list({doc.id: doc for doc in dense_matches + sparse_matches}.values())
    
    # Step 2: Rerank
    ranked_chunks = reranker.rank(query, combined, top_n=5)
    
    # Step 3: Synthesis with grounded citations
    context_str = "\n\n".join([f"[{i}] {c.text}" for i, c in enumerate(ranked_chunks)])
    prompt = f"Answer using ONLY the provided context and cite brackets [0]:\n\n{context_str}\n\nQuestion: {query}"
    return llm.generate(prompt)

```

---

## 5. Verification & Failure Modes

- **Verification Checklist:**
  - [ ] Inputs are validated via strict typed schemas before processing.
  - [ ] Error cascades and timeouts are bounded.
  - [ ] Intermediate artifacts and trace telemetry are logged.
  - [ ] Verification criteria are objectively evaluated before task completion.

- **Common Failure Modes:**
  - **Cascading Hallucination:** Unchecked intermediate model drift polluting downstream stages.
  - **Infinite Looping:** Lack of maximum iteration guards or convergence detection.
  - **Context Bloat:** Carrying unpruned conversational history or verbose tool errors across turns.
