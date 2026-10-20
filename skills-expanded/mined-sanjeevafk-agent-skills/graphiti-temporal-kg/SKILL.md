---
name: graphiti-temporal-kg
description: Episodic memory and dynamic knowledge graphs with temporally bounded relationships and facts.
metadata:
  category: rag
  stack: ["graphiti-core", "neo4j", "openai"]
  source_reference: "rag-architectures/graphiti-agent"
---

# Graphiti Temporal Knowledge Graph RAG

## 1. Architectural Pattern & Core Intent

Episodic memory and dynamic knowledge graphs with temporally bounded relationships and facts.

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `graphiti-core`, `neo4j`, `openai`
- **Upstream Implementation:** [`rag-architectures/graphiti-agent`](file://rag-architectures/graphiti-agent)

Here we demonstrate the power of Graphiti, a temporal knowledge graph solution that enables AI agents to maintain and query evolving knowledge over time. The implementation showcases how to use Graphiti with Pydantic AI to build intelligent agents that can reason about changing facts. This demo includes three main components: 1. **Quickstart Example (`quickstart.py`)**: A comprehensive tutorial demonstrating Graphiti's core features. 2. **Agent Interface (`agent.py`)**: A conversational agent po

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install graphiti-core neo4j openai
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
Refer to the upstream reference code in `rag-architectures/graphiti-agent` for concrete implementation templates:

```python
# Minimal execution idiom for graphiti-temporal-kg
# Inspect rag-architectures/graphiti-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
