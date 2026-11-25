---
name: agent-generated-mediahost-coding-agent
description: Reusable skill for coding agents to build mediahost integrations, API clients, scrapers, bulk downloaders, and media tools. Incorporates the unofficial Python wrapper, auth flow, endpoints, rate-limit handling, and cross-language patterns ...
metadata:
  type: agent-generated
---

# mediahost Coding Agent Skill

**Purpose**: When the user asks you to write code involving mediahost (searching GIFs, downloading videos, building bots, API wrappers, or media pipelines), follow this recipe exactly. Always prioritize the community-maintained `mediahost` Python library unless the user specifies another language.

## Core Principles
- Use the official community wrapper first: `pip install -U mediahost`
- All access is reverse-engineered (no official public developer portal).
- Temporary token auth is mandatory and short-lived.
- Expect rate limits (429 on /auth/temporary); implement exponential backoff + retries.
- Always set a proper User-Agent matching the library: `mediahost (https://github.com/scrazzz/mediahost {version}) Python/{pyver}`.
- Support both sync and async patterns.
- For bulk or high-volume work, add delays and respect CDN hotlinking blocks.
- Output code that is installable, runnable, and includes error handling for auth failures and rate limits.
- Warn about restricted content, Terms of Service compliance, and responsible use.

## Primary Reference (Always Consult First)
- GitHub: https://github.com/scrazzz/mediahost (162 stars, MIT, active 2026)
- Docs: https://mediahost.readthedocs.io/en/stable/api.html
- PyPI: https://pypi.org/project/mediahost/
- Raw HTTP client for endpoints: https://raw.githubusercontent.com/scrazzz/mediahost/main/mediahost/http.py

## Authentication Flow (Mandatory First Step)
1. GET https://api.mediahost.com/v2/auth/temporary with header `Accept: application/json`
2. Extract `token` from response.
3. Pass to `API.login()` or use as `Authorization: Bearer <token>`.
4. Token is temporary — refresh on 401/429.

Example skeleton:
```python
from mediahost import API
api = API()
api.login()  # handles temporary token internally
```

## Key Methods (from API class)
- `api.search(tags="...", order=Order.TopThisWeek, count=80)` → SearchResult
- `api.get_gif(gif_id)` → GIF model with hd_url, sd_url, thumbnail
- `api.get_trending_gifs()`
- `api.get_top_this_week()`
- `api.search_creators(username)`
- `api.fetch_tag_suggestions(query)`
- Async equivalent: `mediahost.aio.API`

Models: GIF, Image, SearchResult, CreatorsResult, User.

Enums: Order (TopThisWeek, etc.), MediaType (g for GIF, i for image).

## CLI Usage (for quick testing)
After install: `mediahost --help` or `mediahost download <url or id>`

## Custom / Low-Level Patterns (when wrapper insufficient)
Reference the gist infrastructure analysis (https://gist.github.com/devinschumacher/54e082d8bdb907aa669036cabe51634f) for:
- CDN/stream URL patterns
- Signature requirements (some endpoints combine IP + UA)
- Direct media extraction without full library
- Fallbacks when hotlinking is blocked

From raw http.py: concrete routes include:
- `/v2/gifs/{id}`
- `/v2/gifs/search?type=g&order=...&tags=...`
- `/v2/explore/trending-gifs`
- `/v2/users/{username}`
- `/v2/niches/search`

Always include the library's UA to avoid 403s.

## Handling Common Issues
- 429 Rate Limit on auth: sleep 5-30s + retry with backoff. Cache tokens when possible.
- API changes (2022+): signature requirements; monitor Reddit r/learnpython or r/DataHoarder for breakage.
- Hotlinking blocked: download via library methods or use yt-dlp/gallery-dl extractors (they have mediahost support).
- Async for scale: use `mediahost.aio` + asyncio.gather for bulk downloads.

## Cross-Language Alternatives
- JavaScript: https://github.com/losparviero/redgif (zero-dep, getGif(id) → buffer)
- Go: https://pkg.go.dev/github.com/StellarReddit/mediahostWrapper
- CLI-only: https://github.com/TadavomnisT/mediahost-downloader

## Example Agent Output Structure
When generating code for the user:
1. Show `pip install` command.
2. Provide complete runnable example (login + search + download one item).
3. Include comments referencing the sources above.
4. Add rate-limit and error handling.
5. Provide async version if bulk work is requested.
6. Suggest testing with small counts first.

## Related Ecosystem
- yt-dlp and gallery-dl have mediahost extractors (check their GitHub issues for current token handling).
- Apify actors for bulk scraping.
- Reddit bots (e.g. restricted-mediahost-Reddit-Bot) for posting automation examples.

## Limitations & Ethics
- No official API key or stable public docs.
- Frequent breaking changes — always verify against current GitHub repo.
- This skill is for educational / personal tooling only. Respect mediahost TOS, rate limits, and do not build abusive scrapers.
- All media is adult/restricted — handle responsibly.

## How to Extend This Skill
If user asks for new features (e.g. niche search, creator following, custom signatures), first check the latest `mediahost` repo, then implement using the http.py patterns or subclass the API class.

**Citations**: All URLs and details above were returned by the deep research sub-agent in this session (GitHub, ReadTheDocs, PyPI, Gist, Reddit, Stack Overflow). Never invent endpoints.

This skill makes any coding agent immediately productive with mediahost without hallucinating the auth flow or endpoints.
