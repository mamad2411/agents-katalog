---
name: iterative-retrieval
description: Iterative retrieval — progressive context loading, retrieval-then-refine loops, query rewriting, adaptive top-k, multi-hop retrieval, confidence scoring, fallback for low-confidence results, retrieval-time prompt guards.
origin: AI Dev Kit
---

# Iterative Retrieval

Progressive context-loading patterns that retrieve only what's needed, refine queries
based on initial results, and handle low-confidence retrieval gracefully.

## When to Use

- Answering questions against a large codebase or document corpus where loading
  everything into context is impossible or cost-prohibitive.
- Building RAG pipelines that need multi-hop reasoning.
- Implementing search-augmented LLM calls that must adapt to retrieval quality.
- Designing agent workflows that progressively gather context before answering.
- Handling queries where the initial retrieval returns irrelevant or insufficient results.

## Core Concepts

### 1. Progressive Context Loading

Instead of loading all potentially relevant documents at once, retrieve in stages:

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class RetrievalResult:
    content: str
    source: str
    score: float
    metadata: dict


@dataclass
class RetrievalResponse:
    results: list[RetrievalResult]
    has_more: bool
    total_available: int
    query: str


class ProgressiveRetriever:
    """Retrieves context in stages, stopping when sufficient."""

    def __init__(self, vector_store, max_tokens: int = 8000):
        self.vector_store = vector_store
        self.max_tokens = max_tokens
        self.accumulated_tokens = 0
        self.results: list[RetrievalResult] = []

    def retrieve(self, query: str, top_k: int = 5) -> RetrievalResponse:
        """First-pass retrieval."""
        raw_results = self.vector_store.search(query, top_k=top_k)
        results = []
        for r in raw_results:
            token_count = estimate_tokens(r["content"])
            if self.accumulated_tokens + token_count > self.max_tokens:
                break
            results.append(RetrievalResult(
                content=r["content"],
                source=r["metadata"]["source"],
                score=r["score"],
                metadata=r["metadata"],
            ))
            self.accumulated_tokens += token_count

        self.results.extend(results)
        return RetrievalResponse(
            results=results,
            has_more=len(raw_results) > top_k,
            total_available=len(raw_results),
            query=query,
        )

    def retrieve_more(self, query: str, top_k: int = 5) -> RetrievalResponse:
        """Subsequent retrieval — skips already-loaded results."""
        offset = len(self.results)
        raw_results = self.vector_store.search(query, top_k=top_k, offset=offset)
        # Same accumulation logic...
        return self.retrieve(query, top_k)
```

### 2. Retrieval-Then-Refine Loop

```python
def retrieval_then_refine(
    retriever: ProgressiveRetriever,
    llm,
    initial_query: str,
    max_iterations: int = 3,
    confidence_threshold: float = 0.7,
) -> dict:
    """Iteratively retrieve and refine until confident or max iterations reached."""

    for iteration in range(max_iterations):
        # Step 1: Retrieve
        results = retriever.retrieve(initial_query, top_k=5)

        if not results.results:
            return {"answer": "No relevant context found.", "iterations": iteration + 1}

        # Step 2: Generate answer + confidence
        context = "\n---\n".join(r.content for r in results.results)
        response = llm.generate(
            system="Answer the question using ONLY the provided context. Also rate your confidence 0.0-1.0.",
            prompt=f"""
Context:
{context}

Question: {initial_query}

Return JSON: {{"answer": "...", "confidence": 0.XX, "missing_info": "..."}}
""",
        )

        parsed = parse_json_response(response)
        confidence = parsed.get("confidence", 0)

        if confidence >= confidence_threshold:
            return {"answer": parsed["answer"], "confidence": confidence, "iterations": iteration + 1}

        # Step 3: Refine query based on missing info
        if parsed.get("missing_info"):
            initial_query = f"{initial_query} {parsed['missing_info']}"
        else:
            # Expand retrieval scope
            initial_query = f"{initial_query} related context"

    # Final attempt with all accumulated context
    return {
        "answer": parsed.get("answer", "Could not find a confident answer."),
        "confidence": confidence,
        "iterations": max_iterations,
        "warning": "Max iterations reached — answer may be incomplete.",
    }
```

### 3. Query Rewriting Based on Initial Results

```python
def rewrite_query(
    original_query: str,
    initial_results: RetrievalResponse,
    llm,
) -> str:
    """Rewrite the query based on what the initial retrieval found (or didn't find)."""

    if initial_results.results and all(r.score > 0.6 for r in initial_results.results):
        # Good results — no rewrite needed
        return original_query

    # Analyze why results were poor
    analysis = llm.generate(
        system="Analyze why this query returned poor results. Suggest 3 rewritten queries.",
        prompt=f"""
Original query: {original_query}
Top results (titles only): {[r.source for r in initial_results.results[:3]]}
Result scores: {[r.score for r in initial_results.results[:3]]}

Suggest 3 improved queries that would find better results.
Return JSON: {{"queries": ["...", "...", "..."]}}
""",
    )

    rewritten = parse_json_response(analysis)["queries"]
    return rewritten[0]  # Use the best suggested query
```

### 4. Adaptive Top-K Selection

```python
def adaptive_top_k(
    query: str,
    retriever,
    min_k: int = 3,
    max_k: int = 15,
    score_threshold: float = 0.5,
) -> list[RetrievalResult]:
    """Dynamically choose k based on result quality."""

    # Start with a small retrieval
    results = retriever.search(query, top_k=min_k)

    if not results:
        # Even min_k returned nothing — try max_k once
        return retriever.search(query, top_k=max_k)

    avg_score = sum(r["score"] for r in results) / len(results)

    if avg_score < score_threshold:
        # Low confidence — expand retrieval window
        expanded = retriever.search(query, top_k=max_k)
        # Filter to maintain quality
        return [r for r in expanded if r["score"] >= score_threshold * 0.8]

    if avg_score > 0.8 and len(results) >= min_k:
        # High confidence with few results — we have what we need
        return results

    # Moderate confidence — try middle ground
    mid_k = (min_k + max_k) // 2
    return retriever.search(query, top_k=mid_k)
```

### 5. Multi-Hop Retrieval

For questions that require connecting information from multiple sources:

```python
def multi_hop_retrieval(
    initial_query: str,
    retriever,
    llm,
    max_hops: int = 3,
) -> dict:
    """Chain retrievals: answer A leads to query B leads to answer C."""

    current_query = initial_query
    hop_results = []

    for hop in range(max_hops):
        # Retrieve for current query
        results = retriever.retrieve(current_query, top_k=3)
        context = "\n---\n".join(r.content for r in results)

        # Ask LLM if it can answer now, or needs another hop
        response = llm.generate(
            system=f"""You are answering a multi-hop question.
Hop {hop + 1} of {max_hops}.
Previous findings: {hop_results}
Current context: {context[:2000]}

Can you answer the original question now? If not, what specific information do you still need?
Return JSON: {{"can_answer": true/false, "answer": "...", "next_query": "..."}}
""",
            prompt=f"Original question: {initial_query}",
        )

        parsed = parse_json_response(response)

        if parsed.get("can_answer"):
            return {
                "answer": parsed["answer"],
                "hops": hop + 1,
                "findings": hop_results,
            }

        if parsed.get("next_query"):
            current_query = parsed["next_query"]
            hop_results.append(f"Hop {hop + 1}: Retrieved {len(results)} documents")
        else:
            break

    return {
        "answer": f"Could not answer after {max_hops} hops.",
        "hops": max_hops,
        "findings": hop_results,
        "warning": "Insufficient context for a complete answer.",
    }
```

### 6. Retrieval Confidence Scoring

```python
def score_retrieval_confidence(results: list[RetrievalResult], query: str) -> float:
    """Composite confidence score for retrieval results."""

    if not results:
        return 0.0

    # Factor 1: Average relevance score from vector store
    avg_vector_score = sum(r.score for r in results) / len(results)

    # Factor 2: Best score (ceiling)
    best_score = max(r.score for r in results)

    # Factor 3: Result count bonus (more results = higher confidence, up to a point)
    count_bonus = min(len(results) / 5.0, 1.0) * 0.1

    # Factor 4: Content overlap with query terms
    query_terms = set(query.lower().split())
    overlap_scores = []
    for r in results:
        content_terms = set(r.content.lower().split())
        overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
        overlap_scores.append(overlap)
    avg_overlap = sum(overlap_scores) / len(overlap_scores) if overlap_scores else 0

    # Weighted composite
    confidence = (
        avg_vector_score * 0.4
        + best_score * 0.3
        + count_bonus
        + avg_overlap * 0.2
    )

    return min(confidence, 1.0)
```

### 7. Fallback for Low-Confidence Results

```python
def retrieval_with_fallback(
    query: str,
    retriever,
    llm,
    confidence_threshold: float = 0.5,
) -> dict:
    """Retrieve, score, and fall back gracefully if confidence is too low."""

    results = retriever.retrieve(query, top_k=5)
    confidence = score_retrieval_confidence(results, query)

    if confidence < confidence_threshold:
        return {
            "answer": f"I could only find low-confidence results for '{query}'. "
                       "The available context may not be sufficient for an accurate answer.",
            "confidence": confidence,
            "fallback": True,
            "partial_context": results.results[0].content[:500] if results.results else None,
        }

    # Proceed with answer generation
    context = "\n---\n".join(r.content for r in results.results)
    answer = llm.generate(
        system="Answer using ONLY the provided context. Cite sources.",
        prompt=f"Context:\n{context}\n\nQuestion: {query}",
    )

    return {
        "answer": answer,
        "confidence": confidence,
        "fallback": False,
        "sources": [r.source for r in results.results],
    }
```

### 8. Retrieval-Time Prompt Guards

```python
def build_retrieval_guarded_prompt(query: str, results: list[RetrievalResult]) -> str:
    """Build a prompt that guards against retrieval hallucination."""

    context_blocks = []
    for i, r in enumerate(results, 1):
        context_blocks.append(f"[Source {i}: {r.source}] (relevance: {r.score:.2f})\n{r.content}")

    separator = "\n---\n"

    return f"""\
Answer the following question using ONLY the provided sources.

Rules:
1. Every claim MUST be supported by a cited source [Source N].
2. If the sources do not contain the answer, say "The provided sources do not contain enough information."
3. Do NOT invent information not present in the sources.
4. If sources conflict, note the conflict and cite both sources.

Sources:
{separator.join(context_blocks)}

Question: {query}
"""
```

## Anti-Patterns

- **Dump everything into context** — defeats the purpose of retrieval; use progressive loading
- **Single-pass retrieval** — one shot often misses key context; use refine loops
- **Ignoring confidence scores** — always score retrieval quality before passing to LLM
- **No query rewriting** — bad queries return bad results; rewrite based on initial findings
- **Unlimited multi-hop chains** — cap at 3 hops to avoid runaway retrieval
- **No fallback path** — when retrieval fails, tell the user instead of hallucinating
- **Trusting vector scores alone** — combine with query overlap and result count

## Best Practices

1. **Start small, expand gradually** — retrieve 3-5 docs first, only expand if confidence is low.
2. **Implement retrieval-then-refine** — use LLM feedback to rewrite queries for subsequent hops.
3. **Score retrieval confidence** — composite score from vector similarity, query overlap, and result count.
4. **Cap multi-hop at 3 iterations** — beyond that, the answer is likely not findable via retrieval.
5. **Use adaptive top-k** — don't use a fixed k; adjust based on result quality.
6. **Always have a fallback** — when confidence is below threshold, acknowledge the limitation.
7. **Guard prompts against hallucination** — force source citations and explicit "don't know" responses.
8. **Log retrieval metrics** — query, results count, confidence score, iterations, final answer quality.
9. **Rewrite queries automatically** — when initial results score below 0.6, trigger query rewriting.
10. **Chunk documents appropriately** — 500-1000 token chunks balance specificity and context.

## Related Skills

- `prompt-optimizer` — Prompt design that incorporates retrieved context effectively
- `exa-search` — Web search as an external retrieval source
- `document-processing` — Preparing documents for vector store ingestion
- `iterative-retrieval` — Complementary retrieval patterns and RAG pipelines
- `token-budget-advisor` — Managing token budgets across retrieval iterations
