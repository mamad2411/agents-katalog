---
name: seo-11-rank-math
description: Rank Math (SEO). Use when the request involves: rank math. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Rank Math

ID: 11.03 | Level: child | Parent: [WordPress SEO](../SKILL.md)

## Purpose
Rank Math within the seo-master tree: Rank Math configuration notes.

## When to use
Triggers: rank math

## When NOT to use
- The topic is covered by a sibling skill: `../plugins`, `../wordpress-performance`, `../wordpress-schema`, `../wordpress-technical`, `../yoast`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. Titles & Meta templates per post type and taxonomy
2. Schema: set default type per post type
3. Sitemap settings, redirections, 404 monitor
4. Use Content AI suggestions carefully; review manually

## Decision rules and checks
- Search appearance templates
- Schema module config
- Redirections + 404 monitor

## Edge cases and failure handling
- Wrong schema type site-wide -> adjust defaults
- Imported Yoast data mismatches -> verify after import

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Rank Math configuration notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Wrong schema type site-wide
- Action: adjust defaults
- Output: Rank Math configuration notes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
