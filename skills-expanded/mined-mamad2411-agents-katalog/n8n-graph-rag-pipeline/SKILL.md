---
name: n8n-graph-rag-pipeline
description: Webhook-driven knowledge graph construction and dynamic property graph query execution.
metadata:
  category: rag
  stack: ["n8n", "neo4j-driver", "apoc"]
  source_reference: "rag-architectures/n8n_knowledge_graph_rag"
---

# n8n Event-Driven Knowledge Graph RAG

## 1. Architectural Pattern & Core Intent

Webhook-driven knowledge graph construction and dynamic property graph query execution.

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `n8n`, `neo4j-driver`, `apoc`
- **Upstream Implementation:** [`rag-architectures/n8n_knowledge_graph_rag`](file://rag-architectures/n8n_knowledge_graph_rag)

**Author:** [Cole Medin](https://www.youtube.com/@ColeMedin) NOTE: This n8n RAG template works for self-hosted n8n and requires you to install the [community MCP node](https://www.npmjs.com/package/n8n-nodes-mcp). This template provides a complete implementation of an **Agentic RAG (Retrieval Augmented Generation)** system in n8n that can be extended easily for your specific use case and knowledge base. Unlike standard RAG which only performs simple lookups, this agent can reason about your know

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install n8n neo4j-driver apoc
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
Refer to the upstream reference code in `rag-architectures/n8n_knowledge_graph_rag` for concrete implementation templates:

```python
# Minimal execution idiom for n8n-graph-rag-pipeline
# Inspect rag-architectures/n8n_knowledge_graph_rag for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
