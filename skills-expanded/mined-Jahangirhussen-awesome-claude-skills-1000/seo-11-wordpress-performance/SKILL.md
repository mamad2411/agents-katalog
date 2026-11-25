---
name: seo-11-wordpress-performance
description: WordPress performance (SEO). Use when the request involves: wordpress speed, wp rocket, cache. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# WordPress performance

ID: 11.06 | Level: child | Parent: [WordPress SEO](../SKILL.md)

## Purpose
WordPress performance within the seo-master tree: Performance fix list with expected gains.

## When to use
Triggers: wordpress speed, wp rocket, cache

## When NOT to use
- The topic is covered by a sibling skill: `../plugins`, `../rank-math`, `../wordpress-schema`, `../wordpress-technical`, `../yoast`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. Measure with PageSpeed/CrUX and Query Monitor
2. Enable page cache, object cache (Redis), CDN, GZIP/Brotli
3. Optimize images (WebP/AVIF), lazy-load below fold, limit plugins
4. Defer non-critical JS, remove unused CSS carefully

## Decision rules and checks
- Page cache + object cache
- Image optimization/lazy-load below fold
- Remove render-blocking plugin assets

## Edge cases and failure handling
- Heavy page builder output -> simplify sections or optimize assets
- Slow TTFB -> hosting/caching upgrade

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Performance fix list with expected gains. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Heavy page builder output
- Action: simplify sections or optimize assets
- Output: Performance fix list with expected gains.

## Dependencies (load only if needed)
- 03-technical-seo/core-web-vitals

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
