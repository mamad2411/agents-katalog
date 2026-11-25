---
name: webpage-content-extract
description: Fetch a webpage and extract main content, removing navigation and ads
---

# Webpage Content Extractor

Fetch a webpage and extract main content, removing navigation and ads

## When to Use

- User wants to extract content
- User wants to read webpage
- Keywords: webpage, extract, content, readability

## Required Parameters

- **url** (string): URL to extract content from

## Output

- **title** (string): Page title
- **content** (string): Main text content
- **word_count** (number): Word count

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: *
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch` -> 7 steps -> Exit: `ret_ok`, `ret_fail`
