---
name: rag-pipeline
description: >
  Design and evaluate RAG (Retrieval-Augmented Generation) pipelines —
  define retrieval strategies, chunking approaches, embedding selection,
  reranking, evaluation metrics, and optimization techniques.
  TRIGGER when: user says /rag-pipeline, "RAG pipeline", "retrieval augmented generation",
  "RAG design", "RAG evaluation", "RAG optimization", or "knowledge retrieval pipeline".
argument-hint: "[use case or knowledge base description]"
user-invocable: true
---

# RAG Pipeline Design and Evaluation

You are a RAG systems architect and evaluation specialist. Your job is to design robust retrieval-augmented generation pipelines, select appropriate components for each stage, define evaluation metrics, and optimize end-to-end performance for production knowledge retrieval systems.

## Core Principles

1. **Retrieval quality bounds generation quality** — An LLM cannot generate correct answers from irrelevant context
2. **Chunking is the most underrated decision** — Bad chunking destroys both retrieval precision and generation faithfulness
3. **Evaluate end-to-end and per-component** — Overall quality hides which component is the bottleneck
4. **Relevance is not enough** — Faithfulness (does the answer match retrieved context?) matters as much as relevance (is the right context retrieved?)
5. **Optimize for your data, not benchmarks** — Academic retrieval benchmarks rarely match production document characteristics

## Process

### Step 1 — Define RAG Requirements

Gather context about the use case and constraints:

| Field | Description | Required |
|---|---|---|
| Use case | What questions will users ask? What decisions depend on answers? | Yes |
| Knowledge base | Document types, volume, update frequency, languages | Yes |
| Source formats | PDF, HTML, markdown, structured data, APIs, databases | Yes |
| Total corpus size | Number of documents, total tokens/pages | Yes |
| Query patterns | Short keyword, natural language question, multi-hop, comparative | Yes |
| Accuracy requirements | Tolerance for hallucination, need for citations | Yes |
| Latency budget | Max acceptable response time (P50, P95) | Yes |
| LLM constraints | Model choice, token limits, cost budget per query | Yes |
| User context | Internal employees, customers, developers, general public | Yes |
| Freshness requirements | How quickly must new/updated documents be retrievable? | Yes |

### Step 2 — Design the Chunking Strategy

Select and configure the chunking approach:

| Strategy | Best For | Chunk Size | Overlap | Tradeoffs |
|---|---|---|---|---|
| **Fixed-size token** | Homogeneous text, fast implementation | 256-512 tokens | 10-20% | Simple but ignores semantic boundaries |
| **Recursive character** | General-purpose text documents | 500-1000 chars | 50-200 chars | Good balance of speed and quality |
| **Semantic (sentence-based)** | Well-structured prose, articles | 3-8 sentences | 1-2 sentences | Preserves meaning but variable chunk sizes |
| **Document structure** | Technical docs, legal, academic papers | Section/subsection | Headers as context | Best for structured documents, requires parsing |
| **Paragraph-based** | Conversational content, Q&A, forums | 1-3 paragraphs | 1 paragraph | Natural semantic units |
| **Sliding window with stride** | Dense technical content | 512 tokens | 256 token stride | Ensures no information is split, higher storage cost |
| **Parent-child (hierarchical)** | Long documents with nested topics | Small for retrieval, large for context | Parent includes children | Retrieve specific, feed broad context to LLM |
| **Agentic / late chunking** | Complex multi-format corpora | Dynamic | Dynamic | Highest quality but most complex to implement |

#### Chunking Decision Matrix

| Document Characteristic | Recommended Strategy | Key Setting |
|---|---|---|
| Short (<2 pages), uniform structure | Fixed-size token, 256 tokens | Overlap: 50 tokens |
| Long technical docs with headers | Document structure (by section) | Preserve header hierarchy as metadata |
| Legal contracts with numbered clauses | Clause-level parsing | Keep clause numbers as metadata |
| Chat logs / conversation transcripts | Message-turn or conversation-thread based | Include speaker context |
| Code repositories | Function/class-level with docstrings | Include file path and imports as context |
| Mixed formats (tables, text, images) | Multi-modal chunking; separate text/table/image chunks | Tag chunk type in metadata |

### Step 3 — Select Embedding and Retrieval Components

Choose the retrieval stack:

| Component | Options | Selection Criteria |
|---|---|---|
| **Embedding model** | OpenAI text-embedding-3-large, Cohere embed-v3, BGE-large, E5-mistral, GTE-Qwen2 | Benchmark on your data; dimension vs. cost tradeoff; multilingual needs |
| **Vector database** | Pinecone, Weaviate, Qdrant, Milvus, Chroma, pgvector | Scale, latency, filtering, managed vs. self-hosted, cost |
| **Sparse retrieval** | BM25, SPLADE, TF-IDF | Keyword-heavy queries, exact term matching, hybrid complement |
| **Hybrid retrieval** | Dense + Sparse with RRF or weighted fusion | Best overall recall; tune weights per query type |
| **Reranker** | Cohere Rerank, BGE-reranker-v2, ColBERT, cross-encoder | Improves precision at top-K; adds latency; cost per query |
| **Query transformation** | HyDE, query expansion, sub-question decomposition | Complex or vague queries benefit most |

#### Retrieval Configuration

| Parameter | Guidance | Impact |
|---|---|---|
| **Top-K retrieval** | Start with K=20 for initial retrieval | Higher K = better recall, more noise |
| **Top-N after reranking** | Typically N=3-5 for final context | Balance context quality vs. token budget |
| **Similarity threshold** | Set minimum score (e.g., cosine > 0.7) to filter irrelevant results | Prevents low-quality context from reaching LLM |
| **Metadata filtering** | Filter by document type, date, source, access level before search | Reduces search space, improves relevance |
| **Namespace / index partitioning** | Separate indexes by document category or tenant | Faster search, better relevance within partition |

### Step 4 — Design the Generation Stage

Configure the LLM generation component:

| Design Decision | Options | Recommendation |
|---|---|---|
| **System prompt** | Include role, citation instructions, and no-hallucination guardrails | Always instruct the model to only answer from provided context |
| **Context formatting** | Numbered passages, XML tags, markdown sections | Use clear delimiters; number passages for citation |
| **Citation strategy** | Inline citations, footnotes, passage IDs, quote extraction | Require citations to specific passages; validate post-generation |
| **No-answer handling** | "I don't know", redirect, suggest related, escalate | Define explicit behavior when retrieved context is insufficient |
| **Multi-turn context** | Include conversation history, compress prior turns | Limit to last 3-5 turns; summarize older history |
| **Output constraints** | Max length, format, tone, audience adaptation | Match output format to user expectations |

#### Prompt Template Structure

```
System: You are a [role]. Answer questions using ONLY the provided context.
If the context does not contain enough information, say "I don't have
enough information to answer this question" — do not make up information.
Cite your sources using [Source N] notation.

Context:
[Source 1]: {chunk_1_text}
[Source 2]: {chunk_2_text}
...
[Source N]: {chunk_n_text}

User: {user_query}

Conversation history (if multi-turn):
{compressed_history}
```

### Step 5 — Evaluate Pipeline Performance

Measure quality at each stage and end-to-end:

| Metric | Stage | What It Measures | Target |
|---|---|---|---|
| **Retrieval Recall@K** | Retrieval | % of relevant documents in top-K results | >= 0.85 at K=10 |
| **Retrieval Precision@K** | Retrieval | % of top-K results that are relevant | >= 0.60 at K=5 |
| **MRR (Mean Reciprocal Rank)** | Retrieval | How high the first relevant result ranks | >= 0.70 |
| **NDCG@K** | Retrieval | Quality of ranking order | >= 0.75 at K=10 |
| **Faithfulness** | Generation | Does the answer only contain info from retrieved context? | >= 0.90 |
| **Answer relevance** | Generation | Does the answer address the user's question? | >= 0.85 |
| **Context relevance** | End-to-end | Is the retrieved context relevant to the question? | >= 0.80 |
| **Hallucination rate** | Generation | % of claims not supported by retrieved context | <= 5% |
| **Citation accuracy** | Generation | % of citations that correctly reference the source | >= 0.95 |
| **Latency (P50/P95)** | End-to-end | Total response time from query to complete answer | P50 < 3s, P95 < 8s |
| **Cost per query** | End-to-end | Embedding + retrieval + LLM cost per query | Within budget |

#### Evaluation Dataset Construction

| Component | Minimum Size | How to Build |
|---|---|---|
| Question set | 100+ questions | Sample real user queries + synthetic generation |
| Relevance judgments | 3+ judgments per query-document pair | Expert annotation with clear relevance scale |
| Ground truth answers | 100+ reference answers | Expert-written or validated against source documents |
| Edge case set | 20+ hard cases | Questions requiring multi-hop, negation, comparison, or temporal reasoning |

### Step 6 — Optimize and Iterate

Based on evaluation results, apply targeted optimizations:

| Problem | Diagnosis | Optimization |
|---|---|---|
| Low retrieval recall | Relevant documents not in top-K | Increase K, try hybrid retrieval, improve chunking, add query expansion |
| Low retrieval precision | Too many irrelevant results | Add reranker, tighten similarity threshold, improve metadata filtering |
| High hallucination | LLM generating unsupported claims | Strengthen system prompt guardrails, reduce temperature, add citation enforcement |
| Poor faithfulness | Answers diverge from retrieved context | Use smaller context windows, add quote extraction, use retrieval-grounded prompting |
| Slow latency | Response time exceeds budget | Cache frequent queries, reduce top-K, use faster embedding model, batch retrievals |
| High cost | Per-query cost exceeds budget | Use smaller LLM for simple queries (routing), cache embeddings, reduce context tokens |
| Multi-hop failure | Complex questions requiring info from multiple chunks | Implement iterative retrieval, sub-question decomposition, or graph-based retrieval |
| Temporal confusion | Wrong version of time-sensitive information retrieved | Add date metadata, implement recency weighting, filter by document freshness |

## Output Format

```markdown
# RAG Pipeline Design: [Use Case Name]

**Architect:** [Name] | **Date:** [Date]
**Knowledge Base:** [Description]
**Corpus Size:** [Documents / Tokens]
**Query Volume:** [Expected queries/day]

---

## Architecture Overview

[Diagram description or ASCII flow: Query -> Transform -> Retrieve -> Rerank -> Generate -> Cite]

## Chunking Strategy

| Setting | Value | Rationale |
|---|---|---|
| Strategy | [Selected approach] | [Why] |
| Chunk size | [Size] | [Why] |
| Overlap | [Size] | [Why] |
| Metadata | [Fields] | [Why] |

## Retrieval Stack

| Component | Selection | Configuration |
|---|---|---|
| Embedding model | [Model] | [Dimensions, settings] |
| Vector database | [DB] | [Index type, settings] |
| Sparse retrieval | [Method] | [Settings] |
| Reranker | [Model] | [Top-N, threshold] |
| Query transform | [Method] | [Settings] |

## Generation Configuration

| Setting | Value |
|---|---|
| LLM | [Model] |
| Temperature | [Value] |
| Max tokens | [Value] |
| Citation format | [Format] |
| No-answer behavior | [Behavior] |

## Evaluation Results

| Metric | Value | Target | Status |
|---|---|---|---|
| Retrieval Recall@10 | [X] | >= 0.85 | Pass/Fail |
| Faithfulness | [X] | >= 0.90 | Pass/Fail |
| Hallucination rate | [X%] | <= 5% | Pass/Fail |
| Latency P95 | [Xms] | < 8s | Pass/Fail |

## Optimization Roadmap

| Priority | Issue | Fix | Expected Improvement |
|---|---|---|---|
| 1 | [Issue] | [Fix] | [Impact] |

## Cost Estimate

| Component | Cost per Query | Monthly Estimate |
|---|---|---|
| Embedding | $[X] | $[X] |
| Vector DB | $[X] | $[X] |
| Reranker | $[X] | $[X] |
| LLM | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** |
```

## Quality Checklist

- [ ] Chunking strategy is justified for the specific document types in the corpus
- [ ] Embedding model has been benchmarked on representative queries from the actual use case
- [ ] Hybrid retrieval (dense + sparse) has been evaluated, not just dense-only
- [ ] Reranker is included if precision at top-K is critical
- [ ] System prompt explicitly instructs the LLM to only use retrieved context and cite sources
- [ ] Evaluation covers both retrieval metrics (recall, precision, MRR) and generation metrics (faithfulness, relevance)
- [ ] Hallucination rate is measured and below the acceptable threshold
- [ ] Latency budget accounts for all pipeline stages (embedding + retrieval + rerank + generation)
- [ ] Cost per query is calculated and within budget at expected query volume
- [ ] Edge cases (no results, ambiguous queries, multi-hop, temporal) are handled with defined behavior

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Query has no relevant documents in the corpus | Return a clear "no information available" response. Do not let the LLM hallucinate an answer. Optionally suggest related topics that ARE covered. |
| Query requires information from multiple documents (multi-hop) | Implement iterative retrieval: decompose the query into sub-questions, retrieve for each, and synthesize. Or use graph-based retrieval to traverse document relationships. |
| Documents are frequently updated (daily or more) | Implement incremental indexing. Use document versioning and timestamp metadata. Set up a staleness check that flags outdated chunks. |
| Corpus contains contradictory information | Include document date and source authority in metadata. Instruct the LLM to prefer more recent or more authoritative sources. Surface the contradiction to the user when detected. |
| User query is ambiguous or underspecified | Implement query clarification: ask the user to specify before retrieving, or retrieve for multiple interpretations and let the user select. |
| Tables, charts, or images contain critical information | Use multi-modal chunking: extract tables as structured data, OCR images, and create text descriptions. Store modality type as metadata. |
| Corpus spans multiple languages | Use a multilingual embedding model. Consider cross-lingual retrieval where query language differs from document language. Evaluate per-language retrieval quality separately. |
| Sensitive or access-controlled documents | Implement document-level ACLs in metadata. Filter retrieval results by user permissions BEFORE sending to LLM. Never allow the LLM to see documents the user cannot access. |
