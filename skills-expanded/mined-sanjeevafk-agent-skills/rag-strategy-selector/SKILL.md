---
name: rag-strategy-selector
description: Decision matrix and implementation patterns across Naive, Sentence-Window, Auto-Merging, and HyDE.
metadata:
  category: rag
  stack: ["chromadb", "sentence-transformers", "rank-bm25"]
  source_reference: "rag-architectures/all-rag-strategies"
---

# Comprehensive RAG Strategy Selector

## 1. Architectural Pattern & Core Intent

Decision matrix and implementation patterns across Naive, Sentence-Window, Auto-Merging, and HyDE.

### Key Characteristics:
- **Primary Domain:** `RAG`
- **Core Technology Stack:** `chromadb`, `sentence-transformers`, `rank-bm25`
- **Upstream Implementation:** [`rag-architectures/all-rag-strategies`](file://rag-architectures/all-rag-strategies)

**A comprehensive resource for understanding and implementing advanced Retrieval-Augmented Generation strategies.** This repository demonstrates 11 RAG strategies with: - 📖 Detailed theory and research ([docs/](docs/)) - 💻 Simple pseudocode examples ([examples/](examples/)) - 🔧 Full code examples ([implementation/](implementation/)) Perfect for: AI engineers, ML practitioners, and anyone building RAG systems.

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install chromadb sentence-transformers rank-bm25
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
Refer to the upstream reference code in `rag-architectures/all-rag-strategies` for concrete implementation templates:

```python
# Minimal execution idiom for rag-strategy-selector
# Inspect rag-architectures/all-rag-strategies for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
