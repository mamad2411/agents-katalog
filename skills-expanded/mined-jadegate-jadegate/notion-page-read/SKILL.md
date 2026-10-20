---
name: notion-page-read
description: Read a Notion page content via official API with block parsing
---

# Notion Page Reader

Read a Notion page content via official API with block parsing

## When to Use

- User wants to read notion
- User wants to notion read
- Keywords: notion, api, page, read

## Required Parameters

- **page_id** (string): Notion page ID
- **api_key** (string): Notion integration API key

## Output

- **title** (string): Page title
- **content** (string): Page content as text
- **blocks** (number): Number of blocks

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: api.notion.com
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch_page` -> 7 steps -> Exit: `ret_ok`, `ret_fail`
