---
name: seo-11-plugins
description: SEO plugin conflicts (SEO). Use when the request involves: plugin conflict, duplicate meta, duplicate schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# SEO plugin conflicts

ID: 11.02 | Level: child | Parent: [WordPress SEO](../SKILL.md)

## Purpose
SEO plugin conflicts within the seo-master tree: Plugin conflict matrix.

## When to use
Triggers: plugin conflict, duplicate meta, duplicate schema

## When NOT to use
- The topic is covered by a sibling skill: `../rank-math`, `../wordpress-performance`, `../wordpress-schema`, `../wordpress-technical`, `../yoast`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WordPress admin, Yoast/Rank Math, Query Monitor, WP-CLI, caching plugin, PageSpeed Insights.

## Core workflow
1. List active plugins affecting head output (SEO, schema, cache, builders)
2. Detect duplicates: meta, OG, schema
3. Remove unused; update; test after changes

## Decision rules and checks
- One SEO plugin
- Check duplicate meta/schema from theme or builder
- Disable unused modules

## Edge cases and failure handling
- Builder and SEO plugin both set titles -> choose one source
- Cache plugin serving noindex -> purge and test

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Plugin conflict matrix. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Builder and SEO plugin both set titles
- Action: choose one source
- Output: Plugin conflict matrix.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
