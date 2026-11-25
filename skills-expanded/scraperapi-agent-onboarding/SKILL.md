---
name: scraperapi-agent-onboarding
description: >
  Entry point for agents and developers new to ScraperAPI. Read first when integrating ScraperAPI
  into an agent or app, setting up the MCP server for Claude Code or other LLM tools, choosing the
  right ScraperAPI product, or obtaining an API key.
  Trigger on: "how do I use ScraperAPI", "set up ScraperAPI", "connect ScraperAPI to Claude",
  "which ScraperAPI product should I use", "get web data for my agent", "scrape a website in my
  app", "add web scraping to my project", "ScraperAPI getting started".
  After reading, route to the narrower skill that owns the selected path.

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🌐"
    homepage: https://www.scraperapi.com
---

# ScraperAPI — Agent Onboarding

ScraperAPI gives agents and apps reliable access to web data: any URL returned as clean HTML or
markdown (with proxy rotation, CAPTCHA bypass, and JS rendering handled automatically), structured
JSON from 20+ supported platforms (Amazon, Walmart, eBay, Redfin, Google SERP), and a crawler for
multi-page extraction.

This skill is the entry point. Read it once, pick a path, then hand off to the narrower skill that
owns that path.

## Getting an API key

All paths require a ScraperAPI key. If you don't have one:

1. Sign up at https://www.scraperapi.com/ — free trial includes 5,000 credits
2. Copy your key from https://dashboard.scraperapi.com/
3. Set it in your environment — never hardcode it in code or configs:

```bash
# macOS / Linux
export SCRAPERAPI_API_KEY=<your-key>

# Windows PowerShell
$env:SCRAPERAPI_API_KEY = "<your-key>"

# .env file
SCRAPERAPI_API_KEY=...
```

Verify the key works before doing real work:

```bash
curl "https://api.scraperapi.com/?api_key=$SCRAPERAPI_API_KEY&url=https://httpbin.org/ip"
```

A JSON response with an `origin` IP confirms the key is valid. A `401` means the key is wrong or
inactive — do not retry with the same key, surface the error.

---

## Choose your path

| Situation | Path |
|-----------|------|
| LLM agent needs web data **during this session** | **Path A** — MCP Server |
| **Adding ScraperAPI to app code** | **Path B** — SDK / REST integration |
| Quick request, or environment without Node/Python | **Path C** — REST API directly |
| Need an API key first | **Path D** — Auth only (above) |

If your task spans paths, do them in order: get key → MCP or SDK → test one real request before
building.

---

## Path A — MCP Server (LLM tool layer)

Use this when the consumer is an LLM agent (Claude Code, custom agent loop) that should call
ScraperAPI as tools. The MCP server exposes up to 22 tools — scrape, Google, Amazon, Walmart, eBay,
Redfin, and crawler — over a single connection.

### Remote server (recommended)

No installation required. All 22 tools available.

Add to your `claude_desktop_config.json`, Claude Code project settings, or MCP client config:

```json
{
  "mcpServers": {
    "ScraperAPI": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.scraperapi.com/mcp",
        "--header",
        "Authorization: Bearer ${SCRAPERAPI_API_KEY}"
      ]
    }
  }
}
```

Requires `SCRAPERAPI_API_KEY` set in the environment. `npx mcp-remote` handles the remote
connection — no separate install step needed.

### Local server (self-hosted, scrape-only)

If you prefer a local server or the remote endpoint is unavailable. Requires Python 3.11+.

```bash
pip install scraperapi-mcp-server
```

```json
{
  "mcpServers": {
    "ScraperAPI": {
      "command": "python",
      "args": ["-m", "scraperapi_mcp_server"],
      "env": { "API_KEY": "<YOUR_SCRAPERAPI_API_KEY>" }
    }
  }
}
```

The local server exposes only the `scrape` tool. For structured Google search data on the local
variant, use `scrape` with `autoparse: true` and `outputFormat: "json"` on a Google search URL.

### After MCP setup

Hand off to the **`scraperapi-mcp`** skill. It owns tool selection, parameter optimization, credit
cost guidance, and error recovery for all 22 MCP tools. Also check the
[MCP setup reference](../scraperapi-mcp/references/setup.md) for variant detection and
troubleshooting.

---

## Path B — SDK / REST integration (app code)

Use this when you're building an application, script, or workflow that calls ScraperAPI from code.

### Smoke test first

Always run one real request before writing integration logic — catches auth, credit, and parameter
issues before they hide inside your app's error paths:

```python
import os, requests

r = requests.get(
    "https://api.scraperapi.com/",
    params={"api_key": os.environ["SCRAPERAPI_API_KEY"], "url": "https://httpbin.org/ip"}
)
print(r.status_code, r.text[:200])
```

A `200` with valid JSON confirms you're wired up.

### Pick the right API

| Job in the app | API | Key docs |
|----------------|-----|----------|
| Fetch any URL as HTML or markdown | Standard API | [docs](https://docs.scraperapi.com/making-requests) |
| Render JS-heavy pages (React, Vue, SPAs) | Standard API + `render=true` | [docs](https://docs.scraperapi.com/making-requests/customizing-requests) |
| Structured JSON: Amazon, Google, Walmart, eBay, Redfin | Structured Data API | [docs](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method) |
| Batch scraping / 100+ URLs | Async Jobs API | [docs](https://docs.scraperapi.com/making-async-requests) |
| Recurring, scheduled scraping without managing infra | DataPipeline (dashboard) | [docs](https://docs.scraperapi.com/) |

### Python

```bash
pip install scraperapi-sdk
```

```python
import os
from scraperapi_sdk import ScraperAPIClient

client = ScraperAPIClient(os.environ["SCRAPERAPI_API_KEY"])
result = client.get("https://example.com", render=True, country_code="us")
print(result)
```

### Node.js

```bash
npm install scraperapi-sdk
```

```js
const scraperapi = require('scraperapi-sdk')(process.env.SCRAPERAPI_API_KEY);
const result = await scraperapi.get('https://example.com', { render: true, country_code: 'us' });
console.log(result);
```

PHP, Ruby, and Java SDKs are also available — see [docs.scraperapi.com](https://docs.scraperapi.com/)
for setup guides.

---

## Path C — REST API (no SDK required)

Use this when the environment can't run `pip` or `npm`, or when you only need a few requests.

**Base URL:** `https://api.scraperapi.com/`
**Auth:** `api_key` query parameter (or `apiKey` in the JSON body for async)

```bash
# Basic scrape
curl "https://api.scraperapi.com/?api_key=$SCRAPERAPI_API_KEY&url=https://example.com"

# With JS rendering
curl "https://api.scraperapi.com/?api_key=$SCRAPERAPI_API_KEY&url=https://example.com&render=true"

# Structured data — Google SERP
curl "https://api.scraperapi.com/structured/google/search?api_key=$SCRAPERAPI_API_KEY&query=web+scraping"

# Structured data — Amazon product
curl "https://api.scraperapi.com/structured/amazon/product?api_key=$SCRAPERAPI_API_KEY&asin=B09V3KXJPB"

# Submit an async job
curl -X POST "https://async.scraperapi.com/jobs" \
  -H "Content-Type: application/json" \
  -d "{\"apiKey\": \"$SCRAPERAPI_API_KEY\", \"url\": \"https://example.com\"}"

# Poll async job status
curl "https://async.scraperapi.com/jobs/<jobId>?apiKey=$SCRAPERAPI_API_KEY"
```

For the full parameter surface (premium proxies, country targeting, session stickiness, binary
targets), see the [API reference](https://docs.scraperapi.com/making-requests/customizing-requests).

### Common status codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Return / parse the body |
| `401` | Invalid API key | Surface error — do not retry |
| `403` | Blocked by target site | Retry with `premium=true`, `ultra_premium=true`, or a different `country_code` |
| `429` | Concurrent limit hit | Back off; switch to async for batch work |
| `500`/`503` | Transient failure | Retry with exponential backoff (3–5 attempts) |

---

## After onboarding — where to go next

Route to the narrowest skill or reference that fits the task:

| User says… | Go to |
|------------|-------|
| "scrape this URL" / "get this page" | `scraperapi-mcp` → `scrape` tool |
| "search Google for…" / "find URLs about…" | `scraperapi-mcp` → `google_search` |
| "get Amazon / Walmart / eBay data" | `scraperapi-mcp` → SDE tools |
| "real estate / Redfin listings" | `scraperapi-mcp` → Redfin tools |
| "crawl a website / extract all links" | `scraperapi-mcp` → `crawler_job_start` |
| "scrape 100+ URLs / batch job" | Async Jobs API — Path C above |
| "schedule recurring scraping" | DataPipeline — https://docs.scraperapi.com/ |
| "debug a failed scrape or blocked request" | `scraperapi-mcp` error recovery section |

When in doubt, prefer structured data endpoints over raw HTML scraping for supported platforms —
they return clean JSON with no parsing logic, are more reliable, and often cost fewer credits than
raw scraping with `render=true`.
