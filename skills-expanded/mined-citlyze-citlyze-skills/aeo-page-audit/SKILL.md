---
name: aeo-page-audit
description: Audit any web page for Answer Engine Optimization (AEO) readiness - can AI crawlers reach it, and can AI engines extract answers from it. Use when asked "is this page AEO ready", "audit this page for AI search", "why don't AI engines cite my page", or "check AI crawler access". Works standalone; no account needed.
license: MIT
metadata:
  author: Citlyze (https://www.citlyze.com)
---

# AEO page audit

Grade a page on the two things that decide whether AI engines use it: crawlability (can AI bots fetch it) and extractability (can an engine lift a clean answer from it). Scored out of 100 using the same public checklist as the free [Citlyze AEO grader](https://www.citlyze.com/free-tools/aeo-grader).

## What you need

Only fetch tools (WebFetch, curl, or equivalent). Fetch raw HTML and judge it as served: AI crawlers generally do not execute JavaScript, so content that only appears after hydration does not count.

## Checks and scoring

Fetch `https://<domain>/robots.txt`, the page HTML, and probe `https://<domain>/llms.txt`, then score:

| # | Check | Max | Pass condition |
| --- | --- | --- | --- |
| 1 | AI crawler access | 25 | robots.txt does not block major AI crawlers (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Bingbot, CCBot, and similar) for this path. Any blocked major crawler scores 0. |
| 2 | Reachable and indexable | 15 | HTTP status below 400 and no `noindex` in meta robots or `X-Robots-Tag`. |
| 3 | One descriptive H1 | 10 | Exactly one H1 with at least 3 words. Multiple H1s: half credit. None: 0. |
| 4 | Question-shaped headings | 12 | At least 2 subheadings phrased as questions users would ask. Exactly 1: half credit. |
| 5 | Extractable answer blocks | 15 | At least 2 headings immediately followed by a direct 25-90 word answer. Exactly 1: half credit. |
| 6 | Entity structured data | 10 | JSON-LD declaring who/what the page is about (Organization, Product, Article, or similar entity types). |
| 7 | Tables and lists | 8 | Content uses tables or lists AI engines can lift verbatim, where the content type calls for them. |
| 8 | Title and meta description | 5 | Title at least 15 characters and meta description at least 50, both describing the page honestly. |
| - | llms.txt | 0 | Informational only: note whether it exists. There is no strong evidence engines consume it yet, so it earns no points. |

## Report format

1. **Score: N/100** with a one-sentence verdict.
2. **Check table**: each check with pass/warn/fail, points earned, and a one-line finding quoting the evidence (the robots rule matched, the H1 text, the failing heading).
3. **Fix list**, ordered by points recoverable: concrete edits ("add a 40-word direct answer under 'How does X work?'", "unblock GPTBot for /blog/*"), not generalities.
4. If several pages were audited, add a comparison table.

## Judgment calls

- Blocking AI crawlers may be a deliberate policy; if the site clearly intends it, say so instead of calling it a defect.
- Question headings and answer blocks are about genuine user questions and honest answers, not keyword stuffing; flag content that games the shape but says nothing.
- For sites where content loads only via JavaScript, report it as the primary finding: fix that before polishing anything else.

Prefer running this online? The hosted [AEO grader](https://www.citlyze.com/free-tools/aeo-grader) runs the same checks on any URL for free. To track how your pages actually perform inside AI answers over time, that's what [Citlyze](https://www.citlyze.com) does.
