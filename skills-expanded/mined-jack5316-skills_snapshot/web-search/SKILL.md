---
name: web-search
description: Search the web via Brave or Tavily API. Use when user asks to search the web, web search, find online, or /web-search.
---

# Web Search Skill (/web-search)

Search the web using Brave or Tavily API.

| Provider | Env var | Free tier |
|----------|---------|-----------|
| Brave (default) | `BRAVE_API_KEY` | 2000 queries/month |
| Tavily | `TAVILY_API_KEY` | 1000 credits/month |

## Quick Start

```bash
python3 _scripts/web_search.py "Python asyncio tutorial"
python3 _scripts/web_search.py "Claude API" --count 5 --save
python3 _scripts/web_search.py "AI news" --provider tavily
```

## Configuration

Add to `.env`:
```
BRAVE_API_KEY=your_key   # https://api.search.brave.com/app/dashboard
TAVILY_API_KEY=your_key # https://tavily.com
```

## Options

- `query` — Search query
- `--count`, `-n` — Number of results (default 10)
- `--provider`, `-p` — `brave` (default) or `tavily`
- `--save`, `-s` — Save to `Sources/Web Search - {query}.md`

## Output

- **Terminal**: Numbered results with title, URL, description
- **Saved**: `Sources/Web Search - {query}.md`
