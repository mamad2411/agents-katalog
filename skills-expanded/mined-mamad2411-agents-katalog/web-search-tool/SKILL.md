---
name: web-search-tool
description: >-
  Web search tool. Searches for information on the internet using the Brave Search API.
  Use when: Use when: researching the latest news, searching technical documentation, fact-checking, or retrieving a list of search results.
tags: [search, web, external]
---


# Web Search Tool

An external web search tool that uses the Brave Search API.

## How to Call

**Bash**: Run with `animaworks-tool web_search "検索クエリ" [オプション]`

## Parameters

| Parameter | Type | Default | Description |
|-----------|-----|---------|-------------|
| query | string | (required) | Search query |
| count | integer | 10 | Number of results to retrieve |
| lang | string | "ja" | Search language |
| freshness | string | null | Freshness filter (pd=24h, pw=1 week, pm=1 month, py=1 year) |

## CLI Usage

```bash
animaworks-tool web_search "検索クエリ" [-n 10] [-l ja] [-f pd]
```

## Notes

- Requires BRAVE_API_KEY configuration
- Search results are treated as external sources (untrusted)
