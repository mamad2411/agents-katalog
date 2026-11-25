---
name: api
description: Find the best database and API interfaces for a particular subject. Recommends databases, REST/GraphQL APIs, SDKs, and data interfaces for any topic or use case. Use when you need APIs for a domain, want database recommendations, or /api.
---

# API Finder Skill (/api)

Find the **best database and API interfaces** for any subject. Uses AI to recommend databases, REST/GraphQL APIs, SDKs, and data marketplaces tailored to your topic or use case.

## Quick Start

```bash
python3 _scripts/api_finder.py "your subject here"
```

## What It Recommends

1. **Databases** — SQL, NoSQL, vector DBs, time-series, graph databases for the domain
2. **REST APIs** — Public/commercial APIs with endpoints, auth, rate limits, docs
3. **GraphQL APIs** — GraphQL interfaces when available
4. **SDKs & Client Libraries** — Official or well-maintained clients (npm, pypi, etc.)
5. **Data Marketplaces** — Aggregators like RapidAPI, Apify for the subject
6. **Alternative Interfaces** — Webhooks, streaming, bulk export options

## Options

- `topic` — Subject or use case (required)
- `--save` — Save output to vault

## Examples

```bash
# Find APIs for stock market data
python3 _scripts/api_finder.py "stock market data"

# Find databases and APIs for weather
python3 _scripts/api_finder.py "weather" --save

# Find options for AI embeddings
python3 _scripts/api_finder.py "AI/LLM embeddings"

# Find APIs for job listings
python3 _scripts/api_finder.py "job listings"
```

## Output

- **Terminal**: Markdown recommendations with Quick Start and comparison
- **Saved note** (with `--save`): `Sources/API Guide - [topic] - YYYY-MM-DD.md`

## Related

- `/source` — Find best content sources (newsletters, podcasts, videos)
- `/alpha` — Stock market data (Alpha Vantage API)
- `/crypto` — Cryptocurrency data (CoinGecko API)
