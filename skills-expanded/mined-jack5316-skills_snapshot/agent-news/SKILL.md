---
name: agent-news
description: >
  Fetch, parse, and summarize news from machine-readable sources designed for
  AI agents. Use when the user asks for news, headlines, or current events via
  structured feeds — RSS/Atom, JSON APIs, or llms.txt-compatible endpoints —
  without scraping human-facing GUIs.
---

# Agent News Skill

Retrieves news from AI-friendly structured sources (JSON APIs > RSS/Atom > llms.txt). Never scrapes GUI pages when a feed exists.

## Usage

```bash
python3 _scripts/agent_news.py                        # RSS only (no API key needed)
python3 _scripts/agent_news.py --topic "AI"
python3 _scripts/agent_news.py --sources "BBC,TechCrunch" --limit 20
python3 _scripts/agent_news.py --use-api              # activates all 3 JSON API sources
python3 _scripts/agent_news.py --use-api --topic "AI agents"
```

## Source Hierarchy

1. **JSON APIs** (requires `--use-api` flag + keys in `.env`):
   - **World News API** (`WORLD_NEWS_API_KEY`) — global coverage, topic search + top news
   - **NewsAPI.org** (`NEWS_API_KEY`) — top headlines from major outlets
   - **GNews** (`GNEWS_API_KEY`) — breaking news by topic
2. **RSS/Atom** — BBC, Reuters, NYT, TechCrunch, VentureBeat, OpenAI, Anthropic, etc.
3. **llms.txt** — emerging machine-readable index standard
4. **tophub.today** — Chinese news (legacy, via `tophub_news.py`)

## Key Principles

- Only report articles actually returned by the feed (no hallucination)
- Always include outlet name, original URL, and published timestamp
- Cache results locally if running multiple queries (respect rate limits)

## Output

`Sources/Agent News Digest - YYYY-MM-DD.md`
