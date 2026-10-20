---
name: exa-semantic-search
description: Search the web semantically using Exa AI API with neural search
---

# Exa AI Semantic Search

Search the web semantically using Exa AI API with neural search

## When to Use

- User wants to exa search
- User wants to semantic search
- Keywords: search, semantic, exa, neural

## Required Parameters

- **query** (string): Natural language search query
- **api_key** (string): Exa API key

## Output

- **results** (array): Search results with title, url, text
- **total** (number): Results count

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: api.exa.ai
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `search` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
