---
name: ottomarkdown-doc-converter
description: Universal file-to-markdown conversion pipeline handling PDF, DOCX, XLSX, and scanned images.
metadata:
  category: scraping
  stack: ["scrapling", "markitdown", "pillow", "pdfplumber"]
  source_reference: "web-scraping-agents/ottomarkdown-agent"
---

# Ottomarkdown Multimodal Document Converter

## 1. Architectural Pattern & Core Intent

Universal file-to-markdown conversion pipeline handling PDF, DOCX, XLSX, and scanned images.

### Key Characteristics:
- **Primary Domain:** `SCRAPING`
- **Core Technology Stack:** `scrapling`, `markitdown`, `pillow`, `pdfplumber`
- **Upstream Implementation:** [`web-scraping-agents/ottomarkdown-agent`](file://web-scraping-agents/ottomarkdown-agent)

Author: [Loic Baconnier](https://deeplearning.fr/) This is a specialized Python FastAPI agent that demonstrates how to handle file uploads in the Live Agent Studio. It shows how to process, store, and leverage file content in conversations with AI models. This agent builds upon the foundation laid out in [`~sample-python-agent~/sample_supabase_agent.py`](../~sample-python-agent~/sample_supabase_agent.py), extending it with file handling capabilities. Not all agents need file handling which is wh

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install scrapling markitdown pillow pdfplumber
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
Refer to the upstream reference code in `web-scraping-agents/ottomarkdown-agent` for concrete implementation templates:

```python
# Minimal execution idiom for ottomarkdown-doc-converter
# Inspect web-scraping-agents/ottomarkdown-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
