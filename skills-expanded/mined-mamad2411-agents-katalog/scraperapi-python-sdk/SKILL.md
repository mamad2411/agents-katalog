---
name: scraperapi-python-sdk
description: >
  Best-practices reference for the ScraperAPI Python SDK (scraperapi-sdk package).
  Consult whenever the user is writing, debugging, or reviewing Python code that calls ScraperAPI.
  Use when user asks: "scrape a website with Python and ScraperAPI", "how do I use ScraperAPIClient",
  "ScraperAPI Python render example", "Python ScraperAPI async", "batch scraping Python ScraperAPI",
  "ScraperAPI premium Python", "how to handle ScraperAPI errors in Python",
  "ScraperAPI structured data Python". Covers client setup, all request parameters,
  the escalation ladder (standard → render → premium → ultra_premium), async jobs for batches,
  structured data endpoints, error handling, and credit budgeting.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🐍"
    homepage: https://docs.scraperapi.com/python/getting-started
---

# ScraperAPI — Python SDK Best Practices

**Requires:** Python 3.7+, `pip install scraperapi-sdk`, `SCRAPERAPI_API_KEY` environment variable.

## Setup

```python
import os
from scraperapi_sdk import ScraperAPIClient

client = ScraperAPIClient(os.environ["SCRAPERAPI_API_KEY"])
```

Never hardcode the API key. Read it from the environment every time.

## Decision Guide

Pick the right call pattern before writing any code.

| Situation | Pattern |
|-----------|---------|
| Single URL, response needed immediately | `client.get()` — synchronous |
| 20+ URLs, or single URL that often times out | Async Jobs API — `requests.post()` to `async.scraperapi.com/jobs` |
| Supported platform (Amazon, Google, Walmart, eBay, Redfin) | Structured Data endpoint — `api.scraperapi.com/structured/<vertical>` |
| Page loads content via JavaScript (React, Vue, Angular) | `client.get()` with `render=True` |
| Site blocks standard proxies | `client.get()` with `premium=True` |

Use the sync SDK for simple, single-URL work. Switch to raw `requests` against the async endpoint for batches — the SDK has no built-in async or batch support.

## Basic Usage

```python
# Simple scrape — returns HTML as a string
html = client.get(url="https://example.com/")

# With parameters
html = client.get(
    url="https://example.com/",
    params={"render": True, "country_code": "us"}
)
```

## Parameter Reference

### Rendering

```python
# Render JavaScript before returning HTML
# Use when: page uses React/Vue/Angular, or initial scrape returns empty/partial content
# Cost: +10 credits (standard: 1 → rendered: 10)
html = client.get(url="https://spa-site.com/", params={"render": True})

# Wait for a specific element before capturing (requires render=True)
# Use when: content loads lazily and simple render still misses it
html = client.get(
    url="https://spa-site.com/",
    params={"render": True, "wait_for_selector": ".product-list"}
)

# Capture a screenshot (auto-enables rendering)
html = client.get(url="https://example.com/", params={"screenshot": True})
```

Start without `render=True`. Add it only when the response is missing expected content — it increases cost and latency.

### Proxies and Geotargeting

```python
# Route through a specific country — no extra cost
html = client.get(url="https://example.com/", params={"country_code": "us"})

# Premium residential/mobile proxies — for sites that block datacenter IPs
# Cost: 10 credits per request (25 with render=True)
html = client.get(url="https://hard-site.com/", params={"premium": True})

# Ultra-premium — for the toughest anti-bot protections
# Cost: 30 credits per request (75 with render=True)
# Note: incompatible with custom headers (keep_headers is ignored)
html = client.get(url="https://hardest-site.com/", params={"ultra_premium": True})
```

`premium` and `ultra_premium` are mutually exclusive — never set both. Escalate gradually:
standard (1 cr) → render (10 cr) → premium (10 cr) → premium+render (25 cr) → ultra_premium (30 cr).

### Sessions (Sticky Proxy)

```python
# Reuse the same proxy IP across multiple requests
# Use for: multi-page flows, pagination, login-state scraping
# Sessions expire 15 minutes after last use; any integer is a valid session ID
html1 = client.get("https://example.com/page1", params={"session_number": 42})
html2 = client.get("https://example.com/page2", params={"session_number": 42})
```

### Headers and Device Type

```python
import requests

# Forward your own headers to the target site
# Note: keep_headers is incompatible with ultra_premium=True
html = client.get(
    url="https://example.com/",
    params={"keep_headers": True},
    headers={"Accept-Language": "en-US", "Referer": "https://google.com"}
)

# Emulate mobile or desktop user-agent
html = client.get(url="https://example.com/", params={"device_type": "mobile"})
```

### Response Format

```python
# Default: raw HTML
html = client.get(url="https://example.com/")

# Structured JSON for supported sites (Amazon, Google, etc.)
# autoparse extracts fields like title, price, reviews automatically
data = client.get(url="https://amazon.com/dp/B09V3KXJPB", params={"autoparse": True})

# Markdown — useful for LLM pipelines
text = client.get(url="https://docs.example.com/", params={"output_format": "markdown"})

# Plain text
text = client.get(url="https://example.com/", params={"output_format": "text"})

# Binary content (PDFs, images)
content = client.get(url="https://example.com/report.pdf", params={"binary_target": True})
```

## Escalation Ladder

Always start cheapest. Move up only when the site blocks the previous tier.

```python
def scrape_with_escalation(url):
    for params in [
        {},                       # 1 credit
        {"render": True},         # 10 credits
        {"premium": True},        # 10 credits
        {"premium": True, "render": True},  # 25 credits
        {"ultra_premium": True},  # 30 credits
    ]:
        result = client.get(url=url, params=params)
        if result and "<html" in result.lower():
            return result
    return None
```

Log which tier succeeded so you can start there next time for the same domain.

## Async Jobs (for Batches)

The sync SDK blocks on each call (up to 70 seconds per URL). For 20+ URLs, use the async endpoint with `requests` directly — it submits jobs in the background and lets you poll or receive webhooks.

```python
import os, requests, time

API_KEY = os.environ["SCRAPERAPI_API_KEY"]

def submit_job(url, extra_params=None):
    payload = {"apiKey": API_KEY, "url": url, "apiParams": extra_params or {}}
    r = requests.post("https://async.scraperapi.com/jobs", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()  # {"id": "...", "status": "running", "statusUrl": "..."}

def poll_job(job, max_wait=120, interval=5):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        r = requests.get(job["statusUrl"], timeout=10)
        data = r.json()
        if data["status"] == "finished":
            return data["response"]["body"]
        if data["status"] == "failed":
            raise RuntimeError(f"Job failed: {job['id']}")
        time.sleep(interval)
    raise TimeoutError(f"Job {job['id']} did not finish in {max_wait}s")

# Batch pattern — submit all, then collect
urls = ["https://example.com/page1", "https://example.com/page2"]
jobs = [submit_job(u) for u in urls]
results = [poll_job(j) for j in jobs]
```

Use webhooks (`"callback": {"type": "webhook", "url": "https://yourapp.com/cb"}`) when you control a server — eliminates polling entirely. See [async docs](https://docs.scraperapi.com/making-async-requests).

For very large batches (up to 50,000 URLs), use `https://async.scraperapi.com/batchjobs` with a `"urls": [...]` array.

## Structured Data Endpoints

Use these instead of scraping raw HTML when the target platform is supported. They return clean JSON, cost fewer credits than raw scraping with `render=True`, and require no parsing logic.

```python
import os, requests

API_KEY = os.environ["SCRAPERAPI_API_KEY"]

def structured_get(vertical, params):
    """Call a structured data endpoint synchronously."""
    url = f"https://api.scraperapi.com/structured/{vertical}"
    r = requests.get(url, params={"api_key": API_KEY, **params}, timeout=70)
    r.raise_for_status()
    return r.json()

# Google SERP
results = structured_get("google/search", {"query": "best Python web scrapers"})

# Amazon product details
product = structured_get("amazon/product", {"asin": "B09V3KXJPB"})

# Walmart product search
items = structured_get("walmart/search", {"query": "standing desk", "tld": "com"})
```

Supported verticals: `google/search`, `google/news`, `google/jobs`, `google/shopping`,
`google/maps`, `amazon/product`, `amazon/search`, `amazon/offers`,
`walmart/product`, `walmart/search`, `walmart/category`,
`ebay/product`, `ebay/search`, `redfin/listing`, `redfin/search`.

See [structured data docs](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method) for required parameters per vertical.

## Error Handling

```python
import os, requests
from scraperapi_sdk import ScraperAPIClient

client = ScraperAPIClient(os.environ["SCRAPERAPI_API_KEY"])

def scrape(url, params=None):
    try:
        result = client.get(url=url, params=params or {})
        return result
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        if status == 401:
            raise ValueError("Invalid API key — check SCRAPERAPI_API_KEY") from e
        if status == 403:
            # Blocked or credits exhausted — try escalating proxy tier
            raise RuntimeError("Blocked or out of credits") from e
        if status == 429:
            # Concurrent request limit — back off and retry
            raise RuntimeError("Rate limit — reduce concurrency or switch to async") from e
        if status in (500, 503):
            # Transient failure — retry with exponential backoff
            raise RuntimeError(f"Transient error {status} — retry") from e
        raise
```

Status code reference: 200 success, 401 bad key, 403 blocked/no credits, 404 target not found,
429 rate limit, 500/503 transient (safe to retry). ScraperAPI does not charge for 500 responses.

## Credit Cost Reference

| Request type | Credits |
|---|---|
| Standard | 1 |
| `render=True` | 10 |
| `premium=True` | 10 |
| `premium=True` + `render=True` | 25 |
| `ultra_premium=True` | 30 |
| `ultra_premium=True` + `render=True` | 75 |
| Structured Data (most verticals) | 1–5 |

Add `"max_cost": N` to any request to cap credit spend — returns 403 if the request would exceed N credits.

## Documentation

- [Python SDK getting started](https://docs.scraperapi.com/python/getting-started)
- [Request parameters](https://docs.scraperapi.com/python/making-requests/customizing-requests)
- [Structured data endpoints](https://docs.scraperapi.com/python/making-requests/structured-data-collection-method)
- [Async API](https://docs.scraperapi.com/making-async-requests)
- [Dashboard & credits](https://dashboard.scraperapi.com/)
