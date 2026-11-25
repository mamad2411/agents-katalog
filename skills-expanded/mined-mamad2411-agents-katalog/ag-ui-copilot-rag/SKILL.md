---
name: ag-ui-copilot-rag
description: Full-stack generative canvas with bidirectional agent state synchronization and human steering.
metadata:
  category: rag
  stack: ["copilotkit", "next", "react", "tailwind"]
  source_reference: "rag-architectures/ag-ui-rag-agent"
---

# Agentic UI Generative Canvas RAG

## 1. Architectural Pattern & Core Intent

Full-stack generative canvas with bidirectional agent state synchronization and human steering.

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `copilotkit`, `next`, `react`, `tailwind`
- **Upstream Implementation:** [`rag-architectures/ag-ui-rag-agent`](file://rag-architectures/ag-ui-rag-agent)

This is a starter template for building AI agents using [PydanticAI](https://ai.pydantic.dev/) and [CopilotKit](https://copilotkit.ai). It provides a modern Next.js application with an integrated investment analyst agent that can research stocks, analyze market data, and provide investment insights. - Node.js 18+ - Python 3.8+ - OpenAI API Key (for the PydanticAI agent) - Any of the following package managers: - pnpm (recommended)

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install copilotkit next react tailwind
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
Refer to the upstream reference code in `rag-architectures/ag-ui-rag-agent` for concrete implementation templates:

```python
# Minimal execution idiom for ag-ui-copilot-rag
# Inspect rag-architectures/ag-ui-rag-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
