---
name: scraping-research-mcp-server
description: Model Context Protocol (MCP) server providing web crawling, page parsing, and research tools to agents.
metadata:
  category: scraping
  stack: ["fastmcp", "crawl4ai", "trafilatura"]
  source_reference: "web-scraping-agents/mcp_server.py"
---

# FastMCP Web Scraping & Research Server

## 1. Architectural Pattern & Core Intent

Model Context Protocol (MCP) server providing web crawling, page parsing, and research tools to agents.

### Key Characteristics:
- **Primary Domain:** `SCRAPING`
- **Core Technology Stack:** `fastmcp`, `crawl4ai`, `trafilatura`
- **Upstream Implementation:** [`web-scraping-agents/mcp_server.py`](file://web-scraping-agents/mcp_server.py)

Single-file MCP service providing unified web scraping and search tools.

---

## 2. Prerequisites & Environment Setup

Ensure the target execution environment contains the required dependencies:

```bash
# Core package installation
uv pip install fastmcp crawl4ai trafilatura
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
Refer to the upstream reference code in `web-scraping-agents/mcp_server.py` for concrete implementation templates:

```python
# Minimal execution idiom for scraping-research-mcp-server
# Inspect web-scraping-agents/mcp_server.py for production class definitions
```

---

## 4. Operational Best Practices & Failure Modes

1. **Memory & Concurrency:** When running parallel scrapers or vector ingestions, bind worker concurrency to avoid HTTP 429 rate limits or host memory pressure.
2. **Schema Validation:** Always enforce typed response validation (e.g. via Pydantic models) to prevent unstructured model hallucinations from corrupting graph and vector stores.
3. **Graceful Fallbacks:** Implement retry policies with exponential backoff on network failures and proxy rotations.
