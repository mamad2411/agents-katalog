---
name: web-fallback
description: Alternative web fetching using Jina Reader when WebFetch fails. Use when WebFetch returns an error, site blocks standard fetching, need to fetch JavaScript-heavy pages, or user asks for alternative fetch method.
---

# Web Fallback

Fallback web fetching skill using Jina Reader API. Use this when the native WebFetch tool fails or returns an error.

## Activation

This skill activates when:
- WebFetch fails or returns an error
- A site blocks standard web fetching
- User explicitly asks for alternative fetching
- Fetching JavaScript-heavy or complex pages

## Usage

Run the fetch script with the target URL:

```bash
uv run .claude/skills/web-fallback/scripts/fetch.py "https://example.com/page"
```

The script returns clean markdown content suitable for LLM consumption.

## Features

Jina Reader handles:
- JavaScript-heavy pages (SPAs)
- PDF documents
- Image captioning
- Complex page layouts
- Sites that block standard fetching

## Notes

- No API key required for basic usage
- Content is returned as clean markdown
- Timeout is set to 30 seconds by default
