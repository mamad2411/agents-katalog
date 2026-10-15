---
name: seo-audit-plan
description: Turns SEO symptoms into a prioritized, skill-routed audit plan. Use when traffic drops, index issues appear, or a full-site SEO review is requested.
---

# SEO Audit Plan

## Overview

Scope audits from evidence (GSC, crawl samples, page checks) into ordered work.

## When to Use

- Traffic drops, coverage spikes, or “full SEO audit” requests

**Not for:** Deep-fixing a single issue (use the domain skill after planning).

## Official sources

- https://developers.google.com/search/docs/monitor-debug/debugging-drops
- https://developers.google.com/search/docs/monitor-debug/search-console-start

## Process

1. Collect symptoms: GSC charts, sample URLs, recent deploys, manual actions.
2. Classify likely buckets: crawl/index, canonical, metadata, JS, mobile/CWV, content/quality, spam, international, ecommerce.
3. Prioritize: **Blockers** (noindex mistakes, 5xx, wrong canonical) → **High** (thin/spam risk, CWV failures) → **Medium** (schema gaps) → **Low** (nice-to-have appearance).
4. Emit an Audit Plan table: Finding hypothesis | Evidence needed | Skill | Owner order.
5. Execute top items with domain skills; re-check GSC after fixes.
6. Optional `auto` mode: after plan approval, run skills in order and pause on blockers.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Audit everything equally." | Fix indexation blockers before cosmetic schema. |
| "Traffic drop means content rewrite." | Separate coverage, CTR, and sitewide bugs first. |
| "Skip evidence; I know the issue." | Plans need GSC/crawl evidence, not vibes. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Plan lists prioritized items with skill routing
- [ ] Evidence sources named (not guesses only)
- [ ] Blockers ordered before cosmetics
