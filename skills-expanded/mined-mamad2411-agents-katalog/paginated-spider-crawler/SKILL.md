---
name: paginated-spider-crawler
description: Robust crawler handling infinite scroll, dynamic URL query pagination, and rate limit backoff.
metadata:
  category: scraping
  stack: ["playwright", "selectolax", "httpx"]
  source_reference: "web-scraping-agents/multi-page-scraper-agent"
---

# Recursive Paginated Spider Crawler

## 1. Architectural Pattern & Core Intent

Robust crawler handling infinite scroll, dynamic URL query pagination, and rate limit backoff.

### Key Characteristics:
- **Primary Domain:** `SCRAPING`
- **Core Technology Stack:** `playwright`, `selectolax`, `httpx`
- **Upstream Implementation:** [`web-scraping-agents/multi-page-scraper-agent`](file://web-scraping-agents/multi-page-scraper-agent)

Author: [Tuan Medeiros](https://www.youtube.com/@tuanmedeiros) **Platform:** n8n (you can import the .json file into your own n8n to check out the flow) An AI-driven solution that searches multiple websites on the internet, requiring only a URL from the user. This agent streamlines the process of retrieving and analyzing data, delivering concise, relevant information to support research, content creation, and more. - Searches multiple websites with a single URL input - Retrieves and consolidates

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install playwright selectolax httpx
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
Refer to the upstream reference code in `web-scraping-agents/multi-page-scraper-agent` for concrete implementation templates:

```python
# Minimal execution idiom for paginated-spider-crawler
# Inspect web-scraping-agents/multi-page-scraper-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
