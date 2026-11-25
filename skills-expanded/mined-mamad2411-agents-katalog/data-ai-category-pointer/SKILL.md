---
name: data-ai-category-pointer
description: "Pointer to a library of 14 specialized Data Ai skills. Use when working on data-ai-related tasks."
risk: none
---

# Data Ai Capability Library 🎯

This is a **pointer skill**. The 14 specialized Data Ai skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **ai-engineering-toolkit** — 6 production-ready AI engineering workflows: prompt evaluation (8-dimension scoring), context budget planning, RAG pipeline design, agent security audit (65-point checklist), eval harness building, and product sense coaching.
- **clarity-gate** — Pre-ingestion verification for epistemic quality in RAG systems. Ensures documents are properly qualified before entering knowledge bases. Produces CGD (Clarity-Gated Documents) and validates SOT (Source of Truth) files.

- **embedding-strategies** — Guide to selecting and optimizing embedding models for vector search applications.
- **exa-search** — Semantic search, similar content discovery, and structured research using Exa API. Use when you need semantic/embeddings-based search, finding similar content, or searching by category (company, people, research papers, etc.).
- **llm-app-patterns** — Architecture and integration sketches for LLM applications, with explicit retrieval, tool, privacy and verification boundaries.
- **local-llm-expert** — Master local LLM inference, model selection, VRAM optimization, and local deployment using Ollama, llama.cpp, vLLM, and LM Studio. Expert in quantization formats (GGUF, EXL2) and local AI privacy.
- **notebooklm** — Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.
- **rag-engineer** — Expert in building Retrieval-Augmented Generation systems. Masters embedding models, vector databases, chunking strategies, and retrieval optimization for LLM applications.
- **recsys-pipeline-architect** — Designs composable recommendation, ranking, and feed pipelines using the six-stage Source→Hydrator→Filter→Scorer→Selector→SideEffect framework
- **seek-and-analyze-video** — Seek and analyze video content using Memories.ai Large Visual Memory Model for persistent video intelligence
- **similarity-search-patterns** — Implement efficient similarity search with vector databases. Use when building semantic search, implementing nearest neighbor queries, or optimizing retrieval performance.
- **tavily-web** — Web search, content extraction, crawling, and research capabilities using Tavily API. Use when you need to search the web for current information, extracting content from URLs, or crawling websites.
- **vector-database-engineer** — Expert in vector databases, embedding strategies, and semantic search implementation. Masters Pinecone, Weaviate, Qdrant, Milvus, and pgvector for RAG applications, recommendation systems, and similar
- **vector-index-tuning** — Optimize vector index performance for latency, recall, and memory. Use when tuning HNSW parameters, selecting quantization strategies, or scaling vector search infrastructure.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/data-ai/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/data-ai`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
