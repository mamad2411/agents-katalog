---
name: seo-11-wordpress-technical
description: WordPress technical (SEO). Use when the request involves: wordpress sitemap robots canonical. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# WordPress technical

ID: 11.01 | Level: child | Parent: [WordPress SEO](../SKILL.md)

## Purpose
WordPress technical within the seo-master tree: Technical config list.

## When to use
Triggers: wordpress sitemap robots canonical

## When NOT to use
- The topic is covered by a sibling skill: `../plugins`, `../rank-math`, `../wordpress-performance`, `../wordpress-schema`, `../yoast`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. Permalinks: post name; avoid changing without redirects
2. Sitemap from core or SEO plugin, not both
3. Robots.txt correct; noindex search, attachments, thin tag/author archives
4. Canonical output verified

## Decision rules and checks
- Core sitemap or plugin sitemap, not both
- Robots + canonical output check
- Search/attachment pages noindex

## Edge cases and failure handling
- Attachment pages indexed -> redirect to parent
- Staging noindex left on -> remove

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Technical config list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Attachment pages indexed
- Action: redirect to parent
- Output: Technical config list.

## Dependencies (load only if needed)
- 03-technical-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
