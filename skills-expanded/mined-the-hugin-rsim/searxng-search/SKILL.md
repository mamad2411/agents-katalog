---
name: searxng-search
description: Search the internet and news using a local SearXNG instance. Use when the user wants to search the web, find current information, search for news, or research a topic without depending on third-party APIs.
compatibility: Requires Python 3 (stdlib only — no extra packages needed). Requires a running SearXNG instance (Docker).
group: domain
triggers:
  - "поиск в интернете"
  - "актуальная информация"
output: "search results with titles, URLs, and snippets"
calls: []
---

# SearXNG Search

Search the internet and news using a self-hosted SearXNG metasearch engine.

## When to use this skill

- User wants to search the internet for information
- User wants to find recent news on a topic
- User needs current information beyond the model's knowledge cutoff
- User wants privacy-respecting search (no API keys, no tracking)

## Prerequisites

### 1. Install Docker Desktop (first time only)

```bash
winget install -e --id Docker.DockerDesktop
```

After installation, **restart the computer** and launch Docker Desktop.

### 2. Start SearXNG

```bash
cd D:/Projects/searxng && docker compose up -d
```

To stop:
```bash
cd D:/Projects/searxng && docker compose down
```

To check status:
```bash
docker ps --filter name=searxng
```

> **First run**: SearXNG generates its own `uwsgi.ini` on startup. The `settings.yml` in `D:/Projects/searxng/searxng/` overrides defaults.

> **IMPORTANT**: Before the first start, generate a real secret key and replace the placeholder in `settings.yml`:
> ```bash
> py -c "import secrets; print(secrets.token_hex(32))"
> ```

## Steps

### Search the web (general)

```bash
py scripts/search_searxng.py "your query"
```

### Search for news

```bash
py scripts/search_searxng.py "your query" --category news
```

### Options

| Option | Description | Default |
|---|---|---|
| `--category` | `general`, `news`, `images`, `videos`, `science`, `it`, `social media` | `general` |
| `--max-results N` | Number of results to return | `10` |
| `--language CODE` | Language code: `en`, `ru`, `de`, `all` | `all` |
| `--url URL` | SearXNG base URL | `http://localhost:8888` |
| `--json` | Output raw JSON | off |

### Examples

```bash
# General search
py scripts/search_searxng.py "Python asyncio best practices"

# News search in Russian
py scripts/search_searxng.py "искусственный интеллект новости" --category news --language ru

# Tech news, top 5
py scripts/search_searxng.py "OpenAI GPT" --category news --max-results 5

# IT-focused search
py scripts/search_searxng.py "Docker networking" --category it

# Raw JSON for further processing
py scripts/search_searxng.py "machine learning" --json
```

## Troubleshooting

| Error | Fix |
|---|---|
| `Cannot connect to SearXNG` | Run `docker compose up -d` in `D:/Projects/searxng/` |
| `Invalid JSON response` | Add `json` to `search.formats` in `settings.yml` and restart |
| `No results found` | Try a different query or category; check SearXNG web UI at http://localhost:8888 |
| Docker not found | Install Docker Desktop via `winget install -e --id Docker.DockerDesktop` |

## Scripts

- [search_searxng.py](scripts/search_searxng.py) — Query SearXNG and display formatted results
