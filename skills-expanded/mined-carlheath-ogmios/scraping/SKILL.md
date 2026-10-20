---
name: scraping
description: |
  Web scraping skill with a 4-tier strategy: WebFetch (fast, static),
  searxng (search-driven), BrightData scrape_as_markdown (anti-bot,
  JS-rendered), Playwright (interactive, login-required). Picks the right
  tool per target URL.

  [WHAT] Scraping for OSINT, intelligence monitoring, source verification.
  Default: start cheapest (WebFetch), escalate as needed. BrightData for
  Cloudflare / anti-bot-protected sites. Playwright for login or heavy SPAs.

  [WHEN] Use when: scrape, fetch URL, crawl, extract content, read site,
  capture article, mirror page, extract markdown, anti-bot.
  NOT for: web search (use searxng or exa), archiving (use Wayback).

  [LANGUAGE] English and other languages. Output content matches source language.
argument-hint: "[URL or scraping target]"
allowed-tools: WebFetch, Bash, mcp__brightdata__scrape_as_markdown, mcp__brightdata__discover, mcp__searxng__searxng_web_search, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot
---

# Scraping

**Role:** 4-tier scraping strategy.

## 4-tier escalation

### Tier 1: WebFetch (default)
Fast, free, works for 70% of sites. Static HTML, no JS rendering.

```
WebFetch URL prompt="Extract main article text"
```

### Tier 2: searxng (search-driven)
When you know the approximate target but not the exact URL. Searches first, fetches the best hit.

```
mcp__searxng__searxng_web_search query
mcp__searxng__web_url_read url
```

### Tier 3: BrightData scrape_as_markdown
For Cloudflare, anti-bot, JS rendering, sites that block simple bots.

```
mcp__brightdata__scrape_as_markdown URL
mcp__brightdata__discover URL  # for link discovery
```

### Tier 4: Playwright (interactive)
Login-required, multi-step (click first, then extract), heavy SPAs.

```
mcp__playwright__browser_navigate URL
mcp__playwright__browser_snapshot
mcp__playwright__browser_evaluate "..." # for dynamic content
```

## Decision rules

| Site type | Tier |
|-----------|------|
| Regular blog / Wikipedia / news article without paywall | 1 |
| Unknown URL but known topic | 2 |
| Cloudflare-protected / Reddit / X (if public) / site returning 403 to bots | 3 |
| Requires login / needs clicks / heavy SPA | 4 |

## Domain-specific defaults

| Domain | Tier strategy |
|--------|---------------|
| Government sites (parliament, ministries) | Tier 1 |
| State media with anti-bot defenses | Tier 3 |
| Telegram channels | Tier 4 (Playwright or Telegram API) |
| LinkedIn profile/post (public) | LinkedIn MCP > Tier 4 |
| Bluesky | Bluesky MCP, not scraping |
| Academic papers (arXiv, PubMed) | arxiv MCP > Tier 1 |
| Paywalled press | Tier 1 (open lede), Tier 3 if bypass via gift link |

## Output format

Markdown always. Preserve source language. Add a metadata block at the top:

```markdown
---
url: [original]
fetched: 2026-05-02T10:30:00Z
tier: 3
title: [extracted title]
---

[content]
```

## Archiving

For relevant content, offer to save to the user's vault via the `archive-to-vault` skill (typically routes to a sources MOC or an unsorted inbox).

## Version history

- v3.0 (2026-05-02): initial public release.
