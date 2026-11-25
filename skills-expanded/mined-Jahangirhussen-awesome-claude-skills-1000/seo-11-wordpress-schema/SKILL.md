---
name: seo-11-wordpress-schema
description: WordPress schema (SEO). Use when the request involves: wordpress schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# WordPress schema

ID: 11.05 | Level: child | Parent: [WordPress SEO](../SKILL.md)

## Purpose
WordPress schema within the seo-master tree: Schema validation report.

## When to use
Triggers: wordpress schema

## When NOT to use
- The topic is covered by a sibling skill: `../plugins`, `../rank-math`, `../wordpress-performance`, `../wordpress-technical`, `../yoast`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. Choose one schema source (SEO plugin or theme)
2. Validate Organization, WebSite, Article, Breadcrumb; product schema for WooCommerce
3. Remove duplicates from builder or add-ons

## Decision rules and checks
- One graph source
- Validate on sample templates

## Edge cases and failure handling
- Schema duplicated by theme -> disable theme schema
- Invalid Article image sizes -> set featured image properly

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Schema validation report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Schema duplicated by theme
- Action: disable theme schema
- Output: Schema validation report.

## Dependencies (load only if needed)
- 27-schema-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
