---
name: seo-11-yoast
description: Yoast SEO (SEO). Use when the request involves: yoast. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Yoast SEO

ID: 11.04 | Level: child | Parent: [WordPress SEO](../SKILL.md)

## Purpose
Yoast SEO within the seo-master tree: Yoast configuration notes.

## When to use
Triggers: yoast

## When NOT to use
- The topic is covered by a sibling skill: `../plugins`, `../rank-math`, `../wordpress-performance`, `../wordpress-schema`, `../wordpress-technical`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. Search appearance templates for post types and taxonomies
2. Indexation settings per type; noindex low-value archives
3. Schema graph settings and organization/person info
4. Review Yoast redirects (premium) and breadcrumbs

## Decision rules and checks
- Titles & Metas templates
- Indexation settings for taxonomies
- Schema graph settings

## Edge cases and failure handling
- Titles default to site name only -> set templates
- Category base duplication -> disable if not needed

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Yoast configuration notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Titles default to site name only
- Action: set templates
- Output: Yoast configuration notes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
