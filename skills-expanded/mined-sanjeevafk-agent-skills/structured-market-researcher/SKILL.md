---
name: structured-market-researcher
description: Broad web exploration engine synthesizing structured market research reports and competitor grids.
metadata:
  category: research
  stack: ["tavily-python", "pydantic-ai", "pandas"]
  source_reference: "web-scraping-agents/general-researcher-agent"
---

# Structured Market Intelligence Researcher

## 1. Architectural Pattern & Core Intent

Broad web exploration engine synthesizing structured market research reports and competitor grids.

### Key Characteristics:
- **Primary Domain:** `RESEARCH`
- **Core Technology Stack:** `tavily-python`, `pydantic-ai`, `pandas`
- **Upstream Implementation:** [`web-scraping-agents/general-researcher-agent`](file://web-scraping-agents/general-researcher-agent)

Author: [Sam Liu](https://www.youtube.com/@54mliu) **Platform:** n8n (you can import the .json file into your own n8n to check out the flow) Meet your personal AI research assistant! This intelligent agent scans the web for the latest information on topics, curates relevant articles, and delivers concise reports straight to you. Stay informed with updates on topics that matter most, all without the hassle of endless searching. Let AI keep you in the loop—effortlessly! - Scans the web to find the

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install tavily-python pydantic-ai pandas
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
Refer to the upstream reference code in `web-scraping-agents/general-researcher-agent` for concrete implementation templates:

```python
# Minimal execution idiom for structured-market-researcher
# Inspect web-scraping-agents/general-researcher-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
