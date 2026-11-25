---
name: seo-02
description: 02. Google SEO (SEO). Use when the request involves: google search, search console, gsc, google indexing, core update, discover, serp features, manual action. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 02. Google SEO

ID: 02 | Level: parent | Parent: SEO Master

## Purpose
Google-specific visibility: GSC, indexing, SERP features, updates, Discover.

## When to use
Triggers: google search, search console, gsc, google indexing, core update, discover, serp features, manual action

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, technical seo, on page seo, off page seo, content seo, local seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console (+API), GA4, URL Inspection tool, Search Status Dashboard, Looker Studio.

## Core workflow
1. Verify GSC property ownership (domain property preferred) and GA4 link
2. Read Performance, Pages/Indexing, Sitemaps, Core Web Vitals, Manual actions & Security
3. Cross-check with URL Inspection on key URLs

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- No data -> property not verified or new site; wait and check sitemap submission
- Sudden drop -> check indexing, manual actions, then update dates

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Findings list: issue, evidence (GSC report/URL), fix, expected effect. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: No data
- Action: property not verified or new site; wait and check sitemap submission
- Output: Findings list: issue, evidence (GSC report/URL), fix, expected effect.

## Children
- [Search Console](search-console/SKILL.md)
- [Google indexing](indexing/SKILL.md)
- [Core updates and volatility](core-updates/SKILL.md)

## Topics handled here (no separate child)
- Google Search: SERP features (snippets, PAA, knowledge panel, image/video/shopping), organic ranking
- Crawling: Googlebot access, crawl stats, rendering
- Discover: high-quality visuals, E-E-A-T, timely content, large images (1200px+)

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
