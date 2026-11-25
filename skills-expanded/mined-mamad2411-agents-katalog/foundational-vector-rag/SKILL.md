---
name: foundational-vector-rag
description: Canonical vector ingestion, recursive chunking, metadata enrichment, and reciprocal rank fusion (RRF).
metadata:
  category: rag
  stack: ["llamaindex", "faiss-cpu", "tiktoken"]
  source_reference: "rag-architectures/foundational-rag-agent"
---

# Foundational Vector RAG Architecture

## 1. Architectural Pattern & Core Intent

Canonical vector ingestion, recursive chunking, metadata enrichment, and reciprocal rank fusion (RRF).

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `llamaindex`, `faiss-cpu`, `tiktoken`
- **Upstream Implementation:** [`rag-architectures/foundational-rag-agent`](file://rag-architectures/foundational-rag-agent)

A simple Retrieval-Augmented Generation (RAG) AI agent using Pydantic AI and Supabase with pgvector for document storage and retrieval. - Document ingestion pipeline for TXT and PDF files - Vector embeddings using OpenAI - Document storage in Supabase with pgvector - Pydantic AI agent with knowledge base search capabilities - Streamlit UI for document uploads and agent interaction

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install llamaindex faiss-cpu tiktoken
```

### Essential Environment Variables:
```env
# Configure matching credentials based on active provider
OPENAI_API_KEY="your-api-key"
ANTHROPIC_API_KEY="your-api-key"
# Database / Vector store connections if applicable
NEO4J_URI="bolt://localhost:7687"
QDRANT_URL="http://localhost:6333"
```

---

## 3. Standard Execution Workflows

### Primary Invocation Pattern:
Refer to the upstream reference code in `rag-architectures/foundational-rag-agent` for concrete implementation templates:

```python
# Minimal execution idiom for foundational-vector-rag
# Inspect rag-architectures/foundational-rag-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
