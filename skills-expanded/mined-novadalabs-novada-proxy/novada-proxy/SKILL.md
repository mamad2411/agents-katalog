---
name: novada-proxy
description: >-
  Residential proxy tools for AI agents — fetch, crawl, search, extract,
  render through 2M+ IPs. Bypass anti-bot, geo-target 195+ countries.
  Use when: scraping websites, researching topics, extracting structured
  data, or any task that needs web access through a proxy.
version: 1.8.2
author: NovadaLabs
platform: clawhub
install:
  mcp:
    command: npx
    args: ["-y", "novada-proxy-mcp"]
    transport: stdio
    env:
      NOVADA_PROXY_USER: "required — proxy username"
      NOVADA_PROXY_PASS: "required — proxy password"
      NOVADA_API_KEY: "optional — enables novada_proxy_search"
      NOVADA_BROWSER_WS: "optional — enables novada_proxy_render"
security:
  network: outbound only (proxy requests to target URLs)
  credentials: proxy credentials via env vars
  filesystem: none
  telemetry: none
tags: [proxy, scraping, web-access, anti-bot, geo-targeting, mcp, residential-ip]
trigger:
  - "scrape"
  - "fetch through proxy"
  - "bypass cloudflare"
  - "geo-target"
  - "residential proxy"
  - "extract product data"
  - "crawl site"
  - "web search"
  - "research"
  - "competitive analysis"
  - "topic investigation"
---

# Novada Proxy — Skill for Claude Code

## When to Use This Skill

- Fetching URLs that block direct requests (Cloudflare, Akamai, DataDome)
- Scraping e-commerce, news, or professional sites (Amazon, LinkedIn, etc.)
- Extracting structured fields (title, price, rating) without HTML parsing
- Researching topics (search + batch read pipeline)
- Crawling entire sites (discover URLs + parallel fetch)
- Accessing geo-restricted content from 195+ countries
- Multi-step flows requiring the same IP (login, pagination)
- Rendering JS-heavy SPAs that return blank with standard HTTP

## Setup

```bash
# Core (proxy fetch)
claude mcp add novada-proxy-mcp \
  -e NOVADA_PROXY_USER=your_username \
  -e NOVADA_PROXY_PASS=your_password \
  -- npx -y novada-proxy-mcp

# All tools (proxy + search + browser render)
claude mcp add novada-proxy-mcp \
  -e NOVADA_PROXY_USER=your_username \
  -e NOVADA_PROXY_PASS=your_password \
  -e NOVADA_API_KEY=your_key \
  -e NOVADA_BROWSER_WS=your_wss_url \
  -- npx -y novada-proxy-mcp
```

Credentials: [novada.com](https://www.novada.com) -> Dashboard -> Residential Proxies

## Tool Decision Tree

```
Need to fetch a URL?
  Static HTML page             -> novada_proxy_fetch
  Need specific fields         -> novada_proxy_extract
  JS-heavy / SPA / blank page  -> novada_proxy_render (5 credits)

Need multiple URLs?
  Have the URLs already        -> novada_proxy_batch_fetch (2-20 URLs, up to 5x parallel)
  Need links from ONE page     -> novada_proxy_map -> novada_proxy_batch_fetch
  Need to crawl a whole site   -> novada_proxy_crawl (recursive BFS, depth 1-5)

Need to find URLs by topic?    -> novada_proxy_search -> novada_proxy_batch_fetch

Need research on a topic?      -> novada_proxy_research (search + read + summarize)

Need same IP across calls?     -> novada_proxy_session (sticky IP via session_id)

Need to check connectivity?    -> novada_proxy_status
```

## Tools Reference

| Tool | Purpose | Credits | Key Params |
|------|---------|---------|------------|
| `novada_proxy_fetch` | Fetch single URL via residential proxy | 1 | `url`, `country`, `format`, `session_id` |
| `novada_proxy_batch_fetch` | Fetch 2-20 URLs concurrently | 1/URL | `urls`, `concurrency` (1-5), `country` |
| `novada_proxy_extract` | Extract structured fields from URL | 1 (5 if render fallback) | `url`, `fields[]`, `render_fallback` |
| `novada_proxy_map` | Discover all internal links on a page | 1 | `url`, `limit` (10-200) |
| `novada_proxy_crawl` | Recursive site crawl (BFS, depth 1-5) | 1/page | `url`, `depth` (1-5), `limit`, `include_content` |
| `novada_proxy_session` | Sticky session (same IP across calls) | 1 (3 if verify) | `session_id`, `url`, `verify_sticky` |
| `novada_proxy_search` | Google search as structured JSON | 1 | `query`, `num` (1-20), `country` |
| `novada_proxy_render` | Render JS pages via real Chromium [BETA] | 5 | `url`, `format`, `wait_for` (CSS selector) |
| `novada_proxy_research` | Search + read + summarize on a topic | varies | `query`, `num_sources` (1-10), `country` |
| `novada_proxy_status` | Check proxy health + version | 1 | _(none)_ |

## Common Workflows

**1. Site Crawl (map -> batch)**
```
novada_proxy_map(url, limit=50)           -> internal_urls[]
novada_proxy_batch_fetch(urls, concurrency=5) -> all pages in parallel
```

**2. Research (search -> batch)**
```
novada_proxy_search(query, num=5)         -> titles + URLs + snippets
novada_proxy_batch_fetch(urls, format="markdown") -> full page content
```

**3. Sticky Session (login + multi-page)**
```
novada_proxy_session(session_id="job001", url="/login")
novada_proxy_session(session_id="job001", url="/dashboard")
novada_proxy_session(session_id="job001", url="/data/page/1")
```

**4. Price Monitoring (geo comparison)**
```
novada_proxy_fetch(url=product_url, country="US")
novada_proxy_fetch(url=product_url, country="DE")
novada_proxy_fetch(url=product_url, country="JP")
# 2nd call per URL+country is a cache hit (0 credits)
```

**5. Structured Extraction (with JS fallback)**
```
novada_proxy_extract(url, fields=["title","price","rating"], render_fallback=true)
# Auto-escalates to Chromium if proxy fetch is blocked
```

## Error Recovery

| Error Code | Recoverable | Next Step |
|------------|-------------|-----------|
| `BOT_DETECTION_SUSPECTED` | Yes | Retry with `novada_proxy_render`, or different `country` |
| `TLS_ERROR` | Yes | Retry with different `country`, or use `novada_proxy_render` |
| `TIMEOUT` | Yes | Increase `timeout` param (max 120s), or retry |
| `RATE_LIMITED` | Yes | Wait 5s, then retry |
| `NETWORK_ERROR` | No | DNS failed. Check URL/domain. |
| `SESSION_STICKINESS_FAILED` | Yes | Retry with `verify_sticky: true` |
| `INVALID_INPUT` | No | Fix params per tool's inputSchema |
| `PROVIDER_NOT_CONFIGURED` | No | Set env vars and restart MCP |

**Escalation chain:** `novada_proxy_fetch` fails -> try different `country` -> try `novada_proxy_render` -> check `novada_proxy_status`

## Cost Guide

| Tool | Credits | Cache? |
|------|---------|--------|
| fetch | 1 | Yes (300s TTL) |
| batch_fetch | 1 per URL | Yes |
| extract | 1 (5 if render fallback) | No |
| map | 1 | No |
| crawl | 1 per page crawled | Yes (pages use fetch cache) |
| session | 1 (3 if verify_sticky) | Never (sticky routing) |
| search | 1 | No |
| render | 5 | No |
| status | 1 | No |

**Optimization:** Always try `fetch` before `render` (5x cheaper). Cache key = `url + format + country`. Repeated calls within 300s = 0 credits (`meta.cache_hit: true`). Check `meta.quota.credits_estimated` on every response.
