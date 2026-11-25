---
name: web_search
description: Search the web via DuckDuckGo HTML and return structured result snippets.
module: builtin_tools.web_search
tools:
  - web_search
---

# Web Search Skill

Provides current-information lookup over the public web.

## `web_search`

- Required: `query`
- Optional: `count` (1..10, default `5`)
- Returns: title, URL, snippet list

## Usage guidance

- Use when information may be outdated or unknown locally.
- Follow up with fetch/scrape tools for source verification when needed.
