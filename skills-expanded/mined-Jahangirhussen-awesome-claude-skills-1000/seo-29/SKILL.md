---
name: seo-29
description: 29. SEO Tools and APIs (SEO). Use when the request involves: seo tools, ahrefs, semrush, screaming frog, dataforseo, pagespeed api, gsc api, seo scraping. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 29. SEO Tools and APIs

ID: 29 | Level: parent | Parent: SEO Master

## Purpose
Tools and data sources.

## When to use
Triggers: seo tools, ahrefs, semrush, screaming frog, dataforseo, pagespeed api, gsc api, seo scraping

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC API, GA4 Data API, PageSpeed Insights API, DataForSEO, Ahrefs/Semrush APIs, Python or Node scripts.

## Core workflow
1. Prefer free first: GSC, GA4, Lighthouse, PageSpeed, Trends
2. Add paid tools when needed (Ahrefs, Semrush, Screaming Frog)
3. Store keys in env vars; respect quotas

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Hardcoded keys -> move to env

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Tool/data map. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hardcoded keys
- Action: move to env
- Output: Tool/data map.

## Children
- [Keyword tools](keyword-tools/SKILL.md)
- [Backlink tools](backlink-tools/SKILL.md)
- [SEO APIs](seo-apis/SKILL.md)
- [Data collection](data-collection/SKILL.md)
- [Scraping (compliant)](scraping/SKILL.md)

## Topics handled here (no separate child)
- Never hardcode API keys; use env vars
- Free first: GSC, Lighthouse, PageSpeed; paid when needed

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
