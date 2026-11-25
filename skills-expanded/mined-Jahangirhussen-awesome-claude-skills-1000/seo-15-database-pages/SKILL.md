---
name: seo-15-database-pages
description: Database-driven pages (SEO). Use when the request involves: database seo, directory. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Database-driven pages

ID: 15.02 | Level: child | Parent: [Programmatic SEO](../SKILL.md)

## Purpose
Database-driven pages within the seo-master tree: Data schema and indexing rules.

## When to use
Triggers: database seo, directory

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../location-pages`, `../programmatic-internal-linking`, `../template-pages`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Dataset or database, template engine, Screaming Frog, GSC (indexing), sitemap generator, QA sampling script.

## Core workflow
1. Clean, accurate data source with update process
2. Set quality thresholds; noindex incomplete entries
3. Pagination and internal linking from hubs

## Decision rules and checks
- Clean data source
- Quality threshold: noindex below it

## Edge cases and failure handling
- Stale data -> schedule refresh
- Duplicate entities -> dedupe

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Data schema and indexing rules. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Stale data
- Action: schedule refresh
- Output: Data schema and indexing rules.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
