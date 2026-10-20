---
name: knowledge-graph-cypher-rag
description: Autonomous Text-to-Cypher query generation with graph schema validation and vector-graph fusion.
metadata:
  category: rag
  stack: ["langchain-community", "neo4j", "langgraph"]
  source_reference: "rag-architectures/agentic-rag-knowledge-graph"
---

# Knowledge Graph Cypher Query RAG

## 1. Architectural Pattern & Core Intent

Autonomous Text-to-Cypher query generation with graph schema validation and vector-graph fusion.

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `langchain-community`, `neo4j`, `langgraph`
- **Upstream Implementation:** [`rag-architectures/agentic-rag-knowledge-graph`](file://rag-architectures/agentic-rag-knowledge-graph)

Agentic knowledge retrieval redefined with an AI agent system that combines traditional RAG (vector search) with knowledge graph capabilities to analyze and provide insights about big tech companies and their AI initiatives. The system uses PostgreSQL with pgvector for semantic search and Neo4j with Graphiti for temporal knowledge graphs. The goal is to create Agentic RAG at its finest. Built with: - Pydantic AI for the AI Agent Framework - Graphiti for the Knowledge Graph - Postgres with PGVect

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install langchain-community neo4j langgraph
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
Refer to the upstream reference code in `rag-architectures/agentic-rag-knowledge-graph` for concrete implementation templates:

```python
# Minimal execution idiom for knowledge-graph-cypher-rag
# Inspect rag-architectures/agentic-rag-knowledge-graph for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
