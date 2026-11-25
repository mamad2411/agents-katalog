---
name: n8n-youtube-monitor
description: Automated YouTube channel monitor triggering webhooks and transcript downstream flows on new uploads.
metadata:
  category: research
  stack: ["n8n", "google-api-python-client"]
  source_reference: "web-scraping-agents/n8n-youtube-agent"
---

# n8n YouTube Channel Polling & Pipeline

## 1. Architectural Pattern & Core Intent

Automated YouTube channel monitor triggering webhooks and transcript downstream flows on new uploads.

### Key Characteristics:
- **Primary Domain:** `RESEARCH`
- **Core Technology Stack:** `n8n`, `google-api-python-client`
- **Upstream Implementation:** [`web-scraping-agents/n8n-youtube-agent`](file://web-scraping-agents/n8n-youtube-agent)

Author: [Dominik Fretz](https://www.linkedin.com/in/dominikfretz/) **Platform:** n8n (you can import the .json file into your own n8n instance to check out the flow) This agent can go and load the youtube transcripts of videos, based on the URL. It then adds the transcripts into a vector store, creates a summary, key points, quotes and other information and stores it in a supabase DB. You then can chat about the videos. Ask for summaries, or follow up questions to sepecific videos. You can also 

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install n8n google-api-python-client
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
Refer to the upstream reference code in `web-scraping-agents/n8n-youtube-agent` for concrete implementation templates:

```python
# Minimal execution idiom for n8n-youtube-monitor
# Inspect web-scraping-agents/n8n-youtube-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
