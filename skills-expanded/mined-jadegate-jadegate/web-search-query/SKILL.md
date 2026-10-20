---
name: web-search-query
description: Search the web using DuckDuckGo HTML with result extraction and fallback
---

# Web Search Query

Search the web using DuckDuckGo HTML with result extraction and fallback

## When to Use

- User wants to web search
- User wants to search web
- Keywords: search, web, duckduckgo, query

## Required Parameters

- **query** (string): Search query

## Output

- **results** (array): Search results
- **provider** (string): Provider used

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: html.duckduckgo.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `encode_q` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
