---
name: seo-11
description: 11. WordPress SEO (SEO). Use when the request involves: wordpress seo, yoast, rank math, permalink, wp plugin conflict, wp theme seo, wp speed. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 11. WordPress SEO

ID: 11 | Level: parent | Parent: SEO Master

## Purpose
WordPress specifics.

## When to use
Triggers: wordpress seo, yoast, rank math, permalink, wp plugin conflict, wp theme seo, wp speed

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. Check Settings > Reading (discourage search engines off), Permalinks, SEO plugin config
2. Audit taxonomies, archives, attachments, author pages
3. Review plugin/theme conflicts and speed

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- 'Discourage search engines' checked -> uncheck
- Multiple SEO plugins -> keep one

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
WordPress SEO audit. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: 'Discourage search engines' checked
- Action: uncheck
- Output: WordPress SEO audit.

## Children
- [WordPress technical](wordpress-technical/SKILL.md)
- [SEO plugin conflicts](plugins/SKILL.md)
- [Rank Math](rank-math/SKILL.md)
- [Yoast SEO](yoast/SKILL.md)
- [WordPress schema](wordpress-schema/SKILL.md)
- [WordPress performance](wordpress-performance/SKILL.md)

## Topics handled here (no separate child)
- Permalinks: post name; avoid dates
- Archives/tags/author pages: noindex if thin
- Single SEO plugin only

## Related installed skills (kept in place; invoke only if needed)
- `wordpress-pro`
- `wordpress-site-dna`
- `wp-performance-review`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
