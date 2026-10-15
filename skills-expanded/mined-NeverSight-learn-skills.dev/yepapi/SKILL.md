---
name: yepapi
description: "Full API context for YepAPI — 30 endpoints for SEO, SERP, web scraping, YouTube, and AI. Plus 110 skills for Next.js, React, TypeScript, shadcn/ui, security, SEO, dashboards, and more."
homepage: https://yepapi.com/skills
metadata:
  tags: [yepapi, api, seo, serp, scraping, youtube, ai, vibe-coding]
  requires:
    env: [YEP_API_KEY]
    mcp: [yepapi]
---

# YepAPI — API Reference

Base URL: `https://api.yepapi.com`
Auth: `x-api-key` header
Response: `{ ok: true, data: {...} }` or `{ ok: false, error: { code, message } }`
Rate limit: 60 req/min

## SEO — Keywords

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/seo/keywords` | $0.15 | `keywords[]`, `location` | Bulk metrics: volume, CPC, difficulty, intent, trends (up to 100) |
| POST | `/v1/seo/keywords/ideas` | $0.03 | `keyword`, `location` | Keyword suggestions from seed |
| POST | `/v1/seo/keywords/related` | $0.03 | `keyword`, `location` | Related keywords for seed |

Returns: `volume`, `cpc`, `difficulty` (0-100), `intent` (informational/commercial/navigational/transactional), `trend` (12-month array)

## SERP

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/serp/google` | $0.01 | `query`, `location` | Google organic results |
| POST | `/v1/serp/google/news` | $0.01 | `query`, `location` | Google News results |
| POST | `/v1/serp/google/maps` | $0.01 | `query`, `location` | Google Maps / local results |

Returns: `results[]` with `title`, `url`, `snippet`, `position`. Maps adds `rating`, `reviews`, `address`, `phone`.

## Domain Analysis

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/seo/domain/overview` | $0.01 | `domain` | Traffic, keywords, backlinks, domain rank |
| POST | `/v1/seo/domain/keywords` | $0.04 | `domain` | Keywords a domain ranks for |
| POST | `/v1/seo/domain/backlinks` | $0.05 | `domain` | Domain backlink profile |

Returns: overview gives `traffic`, `keywords_count`, `backlinks`, `domain_rank`. Keywords gives `keyword`, `position`, `volume`, `url`.

## Competitors

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/seo/competitors` | $0.04 | `domain` | Competitor domains by keyword overlap |
| POST | `/v1/seo/keyword-gap` | $0.04 | `domain`, `competitor` | Keyword gap between two domains |

Returns: competitors gives `domain`, `overlap`, `traffic`. Gap gives `keyword`, `your_position`, `competitor_position`, `volume`.

## Backlinks

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/seo/backlinks` | $0.05 | `target` | Individual backlinks to domain/URL |
| POST | `/v1/seo/backlinks/summary` | $0.03 | `target` | Aggregate metrics + dofollow ratio |
| POST | `/v1/seo/referring-domains` | $0.03 | `target` | Referring domains with authority |

Returns: summary gives `total_backlinks`, `dofollow_ratio`, `domain_rank`. Backlinks gives `source_url`, `anchor`, `type`, `domain_rank`.

## On-Page & Trends

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/seo/page-audit` | $0.03 | `url` | Technical SEO audit (meta, headings, links, images) |
| POST | `/v1/seo/lighthouse` | $0.05 | `url` | Lighthouse scores (performance, a11y, SEO, best practices) |
| POST | `/v1/seo/trends` | $0.02 | `keywords[]` | Google Trends interest over time (up to 5 keywords) |

Returns: page-audit gives `issues[]`, `meta`, `headings`, `links`, `images`. Lighthouse gives `performance`, `accessibility`, `seo`, `best_practices` (0-100). Trends gives `interest_over_time[]`.

## AI Visibility

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/seo/ai/chatgpt` | $0.05 | `query` | What ChatGPT says about a brand/query |
| POST | `/v1/seo/ai/gemini` | $0.05 | `query` | What Gemini says about a brand/query |

Returns: `response` (text), `mentions[]`, `sentiment`.

## Web Scraping

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/scrape` | $0.01 | `url` | Scrape to markdown/HTML/text |
| POST | `/v1/scrape/js` | $0.02 | `url` | JS-rendered scrape (headless browser) |
| POST | `/v1/scrape/stealth` | $0.03 | `url` | Anti-bot bypass (residential proxies) |
| POST | `/v1/scrape/ai-extract` | $0.03 | `url`, `prompt` | AI-powered structured extraction |

Optional: `format` ("markdown"/"html"/"text"), `waitFor` (CSS selector), `timeout` (ms).
Returns: `content` (string), `metadata` (title, description, url).

## YouTube

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/youtube/search` | $0.01 | `query` | Search videos, channels, playlists |
| POST | `/v1/youtube/video` | $0.02 | `videoId` | Full video metadata + formats |
| POST | `/v1/youtube/transcript` | $0.01 | `videoId` | Transcript with timestamps |
| POST | `/v1/youtube/channel` | $0.01 | `channelId` or `handle` | Channel overview |
| POST | `/v1/youtube/comments` | $0.01 | `videoId` | Comments and replies |

Returns: search gives `results[]` with `videoId`, `title`, `views`, `published`. Transcript gives `segments[]` with `text`, `start`, `duration`.

## AI Chat

| Method | Path | Cost | Required | Description |
|--------|------|------|----------|-------------|
| POST | `/v1/ai/chat` | variable | `model`, `messages[]` | Chat with 69 AI models |
| GET | `/v1/ai/models` | free | — | List available models + pricing |

## Common Optional Fields

SEO endpoints: `location` (default "us"), `language` (default "en"), `limit`, `offset`.
Scraping endpoints: `format`, `waitFor`, `timeout`.

## Error Codes

| Code | HTTP | Meaning |
|------|------|---------|
| `INVALID_API_KEY` | 401 | Missing or invalid key |
| `REVOKED_API_KEY` | 401 | Key revoked |
| `NO_CREDITS` | 402 | Insufficient balance |
| `RATE_LIMITED` | 429 | 60 req/min exceeded |
| `VALIDATION_ERROR` | 400 | Bad request body |
| `UPSTREAM_ERROR` | 502 | Provider error |
| `MODEL_NOT_FOUND` | 400 | Invalid AI model |
| `AI_UPSTREAM_ERROR` | 502 | AI provider error |
| `STREAM_ERROR` | 502 | SSE interrupted |
| `NOT_FOUND` | 404 | Endpoint not found |
| `INTERNAL_ERROR` | 500 | Server error |

## Links

- Docs: https://docs.yepapi.com
- Dashboard: https://yepapi.com/dashboard
- API Keys: https://yepapi.com/dashboard/api-keys
- Full Reference: https://docs.yepapi.com/llms-full.txt
- MCP Server: `npx -y @yepapi/mcp`
