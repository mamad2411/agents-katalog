---
name: b2b-lead-enrichment-agent
description: Corporate directory and public record parser for structured lead extraction and validation.
metadata:
  category: scraping
  stack: ["playwright", "phonenumbers", "email-validator"]
  source_reference: "web-scraping-agents/lead-generator-agent"
---

# B2B Directory Crawler & Lead Enrichment

## 1. Architectural Pattern & Core Intent

Corporate directory and public record parser for structured lead extraction and validation.

### Key Characteristics:
- **Primary Domain:** `SCRAPING`
- **Core Technology Stack:** `playwright`, `phonenumbers`, `email-validator`
- **Upstream Implementation:** [`web-scraping-agents/lead-generator-agent`](file://web-scraping-agents/lead-generator-agent)

Author: [Asvin Kumar](https://www.linkedin.com/in/asvin-kumar-1107/) An intelligent lead generation agent built using Pydantic AI and Hunter.io API, capable of finding business email addresses, verifying emails, and generating leads. The agent can search domains for email addresses, verify email validity, and provide detailed statistics about email distribution within organizations. **Note**: For the Live Agent Studio (see the studio_ versions of the scripts), the Hunter.io calls have been mocke

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install playwright phonenumbers email-validator
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
Refer to the upstream reference code in `web-scraping-agents/lead-generator-agent` for concrete implementation templates:

```python
# Minimal execution idiom for b2b-lead-enrichment-agent
# Inspect web-scraping-agents/lead-generator-agent for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
