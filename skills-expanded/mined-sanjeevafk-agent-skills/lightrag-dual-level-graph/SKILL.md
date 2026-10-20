---
name: lightrag-dual-level-graph
description: Dual-level graph indexing linking low-level entities with high-level thematic relationships.
metadata:
  category: rag
  stack: ["lightrag", "networkx", "nano-vectordb", "openai"]
  source_reference: "rag-architectures/light-rag-agent"
---

# LightRAG Dual-Level Knowledge Graph RAG

## 1. Architectural Pattern & Core Intent

Dual-level graph indexing linking low-level entities with high-level thematic relationships.

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `lightrag`, `networkx`, `nano-vectordb`, `openai`
- **Upstream Implementation:** [`rag-architectures/light-rag-agent`](file://rag-architectures/light-rag-agent)

This project demonstrates two different implementations of Retrieval-Augmented Generation (RAG) for answering questions about Pydantic AI using its documentation: 1. **BasicRAG**: A traditional RAG implementation using ChromaDB for vector storage and similarity search 2. **LightRAG**: An advanced, lightweight RAG implementation with enhanced knowledge graph capabilities The primary goal of this project is to showcase the power and efficiency of LightRAG compared to traditional RAG implementation

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install lightrag networkx nano-vectordb openai
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
Refer to the upstream reference code in `rag-architectures/light-rag-agent` for concrete implementation templates:

```python
# Minimal execution idiom for lightrag-dual-level-graph
# Inspect rag-architectures/light-rag-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
