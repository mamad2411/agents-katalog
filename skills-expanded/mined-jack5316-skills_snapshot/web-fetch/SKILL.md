---
name: web-fetch
description: Fetch URL and extract content as markdown. Generic URL-to-markdown for any web page. Use when user asks to fetch URL, extract web content, URL to markdown, or /web-fetch.
---

# Web Fetch Skill (/web-fetch)

Fetch a URL and extract readable content as markdown. No AI—pure extraction.

## Quick Start

```bash
python3 _scripts/web_fetch.py https://example.com/article
python3 _scripts/web_fetch.py https://blog.example.com/post --save
```

## Options

- `url` — URL to fetch (required)
- `--save`, `-s` — Save to `Sources/Web Fetch - {title}.md`
- `--max-chars`, `-m` — Max chars (default 100000)

## Output

- **Terminal**: Extracted markdown
- **Saved**: `Sources/Web Fetch - {title}.md`

## Combine with Article

For AI summary: `web-fetch` → `article` (or pipe content).
