---
name: no-more-fomo
description: >
  Use when user says 'fomo', 'digest', 'daily', 'AI news', 'today's papers',
  'what's new in AI', 'catch up', or on a scheduled daily cron trigger.
---

# No More FOMO

Daily AI intelligence briefing: Twitter KOLs + AI lab blogs + tech podcasts + arxiv + HackerNews.

**Primary digest is always in English.** After generating, automatically translate to Chinese (`YYYY-MM-DD-zh.md`). Both get HTML rendering. Skip translation with `--en-only`.

## When to Use

- User asks about today's AI papers, news, or trending research
- Morning routine check-in on new releases
- Scheduled daily cron trigger

**When NOT to use:** Searching for a specific paper (use web-fetcher or arxiv directly).

## Process Overview

1. **Fetch** — independent source batches when available (see `references/sources.md` for full list)
2. **Filter** — 24h for Twitter/HN, 7 days for blogs/podcasts
3. **Enrich** — fetch abstracts, repo descriptions, resolve URLs
4. **Categorize** — 10 sections from Models to Discovery
5. **Output** — save to `~/no-more-fomo/YYYY-MM-DD.md` + HTML render
6. **Phase 2** — podcast deep summaries, topic search, discovery (skip with `--quick`)

Full process details: `references/process.md` and `references/phase2.md`.

## Arguments

| Argument | Effect |
|----------|--------|
| (none) | Phase 1 + Phase 2 (all defaults) |
| `--full` | Also fetch Tier 2 company accounts |
| `--quick` | Phase 1 only, skip Phase 2 |
| `@handle` | Add extra Twitter accounts |
| `--twitter-only` | Skip blogs, podcasts, HN |
| `--hn-only` | Skip Twitter, blogs, podcasts |
| `--podcasts-only` | Only podcast feeds + deep processing |
| `--no-save` | Print results, don't save |
| `--no-html` | Only .md, skip HTML |
| `--en-only` | Skip Chinese translation |
| `--query "term"` | Add custom HN search query |

## Key Rules

- Every digest item MUST have at least one clickable `[link](URL)`
- Prefer bounded parallel RSS/API fetches; serialize dependent work and shared browser state.
- xreach JSON: `.items[]` (not `.data.items[]`), no `.entities.urls` field
- Construct tweet links from `.id`: `https://x.com/HANDLE/status/ID`
- Dedup against previous day's digest
- Adapt batching to observed rate limits; report unavailable sources without inventing coverage.

## Scheduling

Each invocation produces one bounded digest. Configure recurrence through the
current host's native scheduler, or invoke manually when the host has none.
Keep scheduling, completion notification, and archive location in the
automation configuration rather than embedding a host command here.

## Evidence and fallback

Use native/structured reading or optional adapters as available. Keep RSS/API,
deduplication and caches for inexpensive breadth; use visual/media inspection
only for items whose claims require it. Mark abstract-, metadata- or caption-only
coverage. Never promote these to full-paper or full-video analysis.

Optional HTTP fallbacks:

- xreach fails → `curl -s "https://r.jina.ai/https://twitter.com/HANDLE"`
- HN API fails → `curl -s "https://r.jina.ai/https://news.ycombinator.com"`
- Podcast RSS fails → `curl -s "https://r.jina.ai/PODCAST_WEBSITE"`
