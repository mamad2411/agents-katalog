---
name: seo-15-programmatic-internal-linking
description: Programmatic internal linking (SEO). Use when the request involves: internal linking automation, index bloat. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Programmatic internal linking

ID: 15.05 | Level: child | Parent: [Programmatic SEO](../SKILL.md)

## Purpose
Programmatic internal linking within the seo-master tree: Linking rules and sitemap plan.

## When to use
Triggers: internal linking automation, index bloat

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../database-pages`, `../location-pages`, `../template-pages`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Dataset or database, template engine, Screaming Frog, GSC (indexing), sitemap generator, QA sampling script.

## Core workflow
1. Hubs link to spokes; spokes link to siblings and hub
2. Related blocks by similarity
3. Segment sitemaps by template
4. Prevent index bloat with noindex rules

## Decision rules and checks
- Hub -> spokes, related blocks
- Sitemap segmentation
- Index bloat prevention

## Edge cases and failure handling
- Orphan generated pages -> add hub links
- Too many links -> cap per page

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Linking rules and sitemap plan. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Orphan generated pages
- Action: add hub links
- Output: Linking rules and sitemap plan.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
