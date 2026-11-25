---
name: couchbase-ai-applications
description: "Design and build AI-powered applications on Couchbase, including RAG pipelines, vector search architecture, embedding strategies, and AI agent data patterns. Use whenever the user asks about RAG, retrieval-augmented generation, vector search for AI, Hyperscale Vector Index (HVI), Composite Vector Index (CVI), Search Vector Index (SVI), embedding pipelines, semantic search, AI agent memory, grounding LLMs with Couchbase, agentic data patterns, billion-scale vector search, multi-vector search, AI application architecture, or 'how do I build an AI app with Couchbase.' Distinct from couchbase-fts (which covers FTS index mechanics and query syntax) — this skill is about end-to-end AI application design: the data model, embedding pipeline, index type selection, retrieval strategy, and integration with LLM frameworks. Use proactively when the user is building AI features or has a use case involving language models, embeddings, or semantic retrieval."
license: MIT
---

# Couchbase AI Applications

A skill for *designing AI-powered applications* on Couchbase — RAG pipelines, vector search architecture, embedding strategies, and agent memory patterns. Covers the full stack from document design through embedding generation, index selection, retrieval, and LLM integration.

Distinct from:
- `couchbase-fts` — FTS index mechanics and query syntax (the lower-level how); this skill is about the application-level what and why
- `couchbase-data-modeling` — general document design; this skill covers AI-specific document patterns
- `couchbase-app-integration` — SDK patterns; this skill covers AI framework integration

If the conversation is "I'm building an AI feature / RAG pipeline / agent," this is the right skill.

## When this skill applies

- "How do I build a RAG pipeline with Couchbase?"
- "Which vector index type should I use — HVI, CVI, or SVI?"
- "How do I store and search embeddings at scale?"
- "How do I combine vector search with keyword/metadata filters?"
- "How do I use Couchbase as memory for an AI agent?"
- "What's the difference between Hyperscale and Composite vector indexes?"
- "How do I integrate Couchbase with LangChain / LlamaIndex?"
- "How do I build a billion-scale vector search?"
- "How do I evaluate retrieval quality in my RAG pipeline?"

## Pick the right reference

| Question | Read |
|---|---|
| "Which of the three vector index types should I use?" | `references/vector-index-types.md` |
| "How do I design my documents and data pipeline for AI?" | `references/data-design.md` |
| "How do I build a RAG pipeline end to end?" | `references/rag-patterns.md` |
| "LangChain / LlamaIndex / custom framework integration" | `references/framework-integration.md` |

## Three core principles

**Principle 1 — Choose the index type before writing any code.**
Couchbase 8.0 has three vector index types with meaningfully different characteristics. Choosing wrong means an index rebuild. HVI (Hyperscale) is for billion-scale with low memory; CVI (Composite) is for filtered vector search; SVI (Search Vector Index, inside FTS) is for hybrid text+vector in one index. See `references/vector-index-types.md` before picking.

**Principle 2 — The embedding pipeline is outside Couchbase.**
Couchbase stores and searches vectors; it does not generate them. Your pipeline generates embeddings (at write time for documents, at query time for queries) using an external model. The embedding model must be consistent across indexing and querying — a dimension or model mismatch produces silently wrong results, not errors.

**Principle 3 — RAG quality is a retrieval problem, not a generation problem.**
Most RAG failures are retrieval failures: wrong chunks returned, too few chunks, no metadata filtering, stale chunks. Invest in retrieval quality (chunk strategy, hybrid search, metadata filters, reranking) before tuning the LLM prompt.

## Quick tool map

| Task | Tool |
|---|---|
| Create Composite Vector Index (filtered vector search) | `admin_vector_index_create_composite` |
| Create Hyperscale Vector Index (billion-scale) | `admin_vector_index_create_hyperscale` |
| List vector indexes | `admin_vector_index_list` |
| Drop a vector index | `admin_vector_index_drop` |
| Run a kNN vector search | `cb_fts_search` with `knn` query |
| Run hybrid text + vector search | `cb_fts_search` with `knn` + `query` combined |
| SQL++ with vector function (CVI) | `cb_query` with `APPROX_VECTOR_DISTANCE()` |

## Version notes

- **Pre-8.0:** FTS-based vector search (Search Vector Index) only. Limited to ~10M vectors per index, lower recall at scale.
- **8.0 (GA October 2025):** Three index types. HVI and CVI use the Index Service (not FTS). Billion-scale supported. Composite Vector Index enables scalar-filtered vector search in SQL++.
- **Capella:** All three index types available. HVI requires an appropriately sized compute tier.
- **AI Data Plane (GA June 30, 2026):** Couchbase now offers agent-focused building blocks beyond raw vector search — **Agent Memory** (managed conversational/agent memory store) and **Agent Catalog** (tool/prompt catalog for agentic apps), delivered as part of the self-managed **AI Data Plane** (the successor to the managed-Capella AI Services line, which GA'd alongside 8.0). Licensing the AI Data Plane also provides enterprise support for the official Couchbase MCP server (see `couchbase-mcp`). Detailed first-party API references for Agent Memory / Agent Catalog were still rolling out as of this writing; treat specific method signatures as unverified until confirmed against current docs, and prefer the vectorization/RAG patterns in this skill for anything you need to ship today.

## Related skills

- `couchbase-fts` — FTS index mechanics, analyzers, query syntax, SVI configuration details
- `couchbase-data-modeling` — document shape decisions that affect chunking and embedding storage
- `couchbase-sizing` — vector index memory budgeting
- `couchbase-sqlpp-tuning` — SQL++ queries using `APPROX_VECTOR_DISTANCE()` with CVI
