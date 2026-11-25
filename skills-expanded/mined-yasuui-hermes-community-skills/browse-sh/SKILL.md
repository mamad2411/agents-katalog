---
name: browse-sh
title: Browse.sh — AI Agent Skill Catalog (Browserbase)
version: 1.0.0
description: >
  Use the browse.sh open-source skill catalog (171+ skills) to interact with websites
  via their documented APIs or browser automation. Provides precise, token-efficient
  workflows for weather, flights, jobs, shopping, research, GitHub, and more.
  Requires `browse` CLI (npm) and Browserbase API key for browser-requiring skills.
category: web
license: MIT
tags:
  - browse
  - browserbase
  - skills
  - api
  - web-automation
  - scraping
tested: schema-only
tested_note: Frontmatter and docs validated; external browse.sh runtime not executed by this repo.
---

# Browse.sh — AI Agent Skill Catalog

## Overview

Browse.sh is an open-source CLI and skill catalog from Browserbase. It provides **171+ pre-built skill files** that teach an AI agent exactly how to interact with a website — which API endpoints to call, what headers to send, how to parse responses, and what gotchas exist. This is NOT a runtime — it's a **precision instruction layer** that eliminates LLM guessing.

Browser-use/browser-harness style *domain skills* fit this pattern: they are site playbooks, not a separate executor. Use them to decide whether to browse, call an endpoint, or combine both.

**Install:** `npm install -g browse`

**Skill catalog:** https://browse.sh

**GitHub:** https://github.com/browserbase/skills

## Architecture

```
browse skills add <domain/task>     → downloads SKILL.md to ~/.config/browserbase/skills/
browse skills find <keyword>       → search the catalog
browse skills list                  → list all 171 skills with metadata
browse skills install               → install the browse CLI skill itself
browse open <url>                   → open a browser session (requires Browserbase API key)
browse cloud fetch <url>            → lightweight fetch via Browserbase API
browse cloud search <query>         → web search via Browserbase API
```

## Skill Locations on This Machine

- Catalog skills: `~/.config/browserbase/skills/<domain>/<task>/SKILL.md`
- CLI skill: `~/.agents/skills/browse/SKILL.md`
- Installed local skills (5):
  - `weather.gov/get-forecast-1uezib`
  - `github.com/get-repo-metadata-iglddk`
  - `news.ycombinator.com/get-stories-wyej87`
  - `arxiv.org/search-papers-zv05w6`
  - `amazon.com/search-products-5170mf`

## API-Only Skills (No Browser Needed)

These use clean public APIs — no auth, no proxy, no Browserbase required:

| Skill | Method | Key Endpoint |
|-------|--------|---------------|
| weather.gov/get-forecast | `api` | `api.weather.gov/points/{lat},{lon}` → forecast grid |
| github.com/get-repo-metadata | `api` | `api.github.com/repos/{owner}/{repo}` + parallel sub-requests |
| news.ycombinator.com/get-stories | `api` | Firebase API `hacker-news.firebaseio.com/v0/` |
| arxiv.org/search-papers | `api` | `export.arxiv.org/api/query?search_query=...` (Atom XML) |
| sec.gov/search-edgar-fulltext | `api` | `efts.api.sec.gov/v4/EDGAR/search` |

### Weather.gov Workflow (Tested ✓)

1. **Geocode** (if ZIP/city): `GET https://nominatim.openstreetmap.org/search?postalcode=ZIP&country=us&format=json&limit=1`
2. **Resolve point**: `GET https://api.weather.gov/points/{lat},{lon}` with `Accept: application/geo+json` and `User-Agent: hermes-agent/1.0`
3. **Fetch forecast**: Follow `.properties.forecast` URL from step 2
4. **Fetch alerts**: `GET https://api.weather.gov/alerts?area={state}`

Gotcha: Round lat/lon to ≤4 decimal places. NWS only covers US territories.

### GitHub Metadata Workflow (Tested ✓)

1. `GET /repos/{owner}/{repo}` — core metadata (stars, forks, language, license, topics)
2. `GET /repos/{owner}/{repo}/languages` — byte breakdown per language
3. `GET /repos/{owner}/{repo}/commits/{default_branch}` — latest commit
4. `GET /repos/{owner}/{repo}/releases/latest` — latest release (404 = no releases)
5. Parallel: community profile, license body, README (base64), contributors, pages, funding

Gotcha: `User-Agent` header is REQUIRED or GitHub 403s. `subscribers_count` = watchers, NOT `watchers_count`.

### Hacker News Workflow (Tested ✓)

1. `GET https://hacker-news.firebaseio.com/v0/topstories.json` → array of IDs
2. For each ID: `GET https://hacker-news.firebaseio.com/v0/item/{id}.json`
3. Fields: `.title`, `.by`, `.score`, `.url`, `.time`, `.kids` (comment IDs)

### arXiv Search Workflow

1. Build query: `http://export.arxiv.org/api/query?search_query=all:{terms}&start=0&max_results=10&sortBy=submittedDate&sortOrder=descending`
2. Parse Atom XML response: `<entry>` elements with `<title>`, `<author>`, `<category>`, `<published>`
3. Gotcha: Rate limited — don't hammer. Use `max_results` ≤ 20 per request.

## Browser-Requiring Skills (Need Browserbase)

These need a real browser session because the target site uses JS rendering, anti-bot, or OAuth:

| Skill | Method | Why Browser |
|-------|--------|-------------|
| amazon.com/search-products | `url-param` + proxy | PerimeterX anti-bot, JS-rendered prices |
| airbnb.com/search-listings | `url-param` + proxy | Dynamic pricing, PerimeterX |
| linkedin.com/search-jobs | `browser` | Auth wall, JS-rendered |
| yelp.com/extract-reviews | `browser` | Dynamic content, rate limits |
| doordash.com/extract-menu | `browser` | JS-rendered menu |

### Setup Browserbase (Required for cloud browser skills)

1. Create account: https://browserbase.com (free tier available)
2. Get API key: https://browserbase.com/settings
3. Set env var: `export BROWSERBASE_API_KEY=your_key_here`
4. Also set in Hermes: `hermes config set env.BROWSERBASE_API_KEY your_key_here`
5. Test: `browse cloud fetch https://example.com`

## Local Browser Mode (No API key needed)

For sites without aggressive anti-bot, use `--local` flag:

```bash
browse open https://example.com --local      # local headless Chromium
browse snapshot                               # accessibility tree of current page
browse eval "document.title"                  # run JS in page
browse get title                              # get page title
| Skill | Method | Why Browser |
|-------|--------|-------------|
| amazon.com/search-products | `url-param` + proxy | PerimeterX anti-bot, JS-rendered prices |
| airbnb.com/search-listings | `url-param` + proxy | Dynamic pricing, PerimeterX |
| linkedin.com/search-jobs | `browser` | Auth wall, JS-rendered |
| yelp.com/extract-reviews | `browser` | Dynamic content, rate limits |
| doordash.com/extract-menu | `browser` | JS-rendered menu |

## Adding New Skills

```bash
# Find a skill
browse skills find "restaurants"

# Add it (downloads SKILL.md)
browse skills add opentable.com/check-availability-f2fwrm

# Read the skill instructions
cat ~/.config/browserbase/skills/opentable.com/check-availability-f2fwrm/SKILL.md
```

## Catalog Quick Reference (Top Skills by Installs)

| Install Count | Skill | Category |
|:-:|---|---|
| 17 | airbnb.com/search-listings | travel |
| 16 | amazon.com/search-products | shopping |
| 11 | allrecipes.com/search-recipes | recipes |
| 11 | linkedin.com/search-linkedin-jobs | careers |
| 9 | craigslist.org/search-listings | marketplace |
| 9 | github.com/get-repo-metadata | developer-tools |
| 9 | opentable.com/check-availability | restaurants |
| 9 | resy.com/check-availability | restaurants |
| 8 | indeed.com/search-jobs | jobs |
| 8 | weather.gov/get-forecast | weather |
| 7 | google.com/search-flights | travel |
| 7 | news.ycombinator.com/get-stories | news |
| 6 | kayak.com/compare-flights | travel |
| 6 | sec.gov/search-edgar-fulltext | finance |

## When to Use Browse.sh vs Other Tools

- **Use browse.sh skills** when: User asks about a specific website that has a skill, and the skill documents a clean API path. More precise than `web_search` or `web_extract`.
- **Use `browse cloud fetch`** when: You need a headless fetch with proxy support for sites with anti-bot.
- **Use `browse cloud search`** when: You need web search results via Browserbase instead of the default search tool.
- **Use `browse open` + `browse snapshot/click/fill`** when: Full browser automation is needed (JS-heavy sites, forms, multi-step workflows).
- **Use `web_search` / `web_extract`** when: No skill exists for the target site and you just need information, not structured interaction.
- **Translate browse.sh playbooks onto Hermes tools** when you are already operating inside Hermes: `new_tab` → `browser_navigate`, screenshots → `browser_snapshot`/`browser_vision`, click/fill → `browser_click`/`browser_type`, JS/DOM inspection → `browser_console`, and clean endpoint steps → `terminal` with `curl` or `execute_code`.

See `references/hermes-browser-tool-bridge.md` for the mapping and execution heuristics.

## Pitfalls

- **arXiv rate limits aggressively.** Space requests out. Use `max_results ≤ 20`.
- **GitHub requires `User-Agent` header** or returns 403 with "Request forbidden by administrative rules."
- **NWS API rounds coordinates.** Pass lat/lon with ≤4 decimal places or you get 404.
- **Browserbase free tier** has session limits. Check at https://browserbase.com/settings.
- **`browse skills add`** opens an interactive multi-select for agent targets. It still downloads the SKILL.md regardless — press Enter to accept defaults.
- **Skill files average 15-25KB each.** The full 171-skill catalog is ~4.5MB. Trivially cacheable.
