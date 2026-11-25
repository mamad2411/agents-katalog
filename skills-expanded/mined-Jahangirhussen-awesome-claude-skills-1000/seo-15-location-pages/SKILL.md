---
name: seo-15-location-pages
description: Location pages (SEO). Use when the request involves: location x service. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Location pages

ID: 15.03 | Level: child | Parent: [Programmatic SEO](../SKILL.md)

## Purpose
Location pages within the seo-master tree: Location page template.

## When to use
Triggers: location x service

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../database-pages`, `../programmatic-internal-linking`, `../template-pages`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Dataset or database, template engine, Screaming Frog, GSC (indexing), sitemap generator, QA sampling script.

## Core workflow
1. Create pages only where you serve
2. Add local proof: team, reviews, projects, map, FAQs
3. Avoid city-swap doorway pages

## Decision rules and checks
- Only where real service exists
- Local proof/content per page

## Edge cases and failure handling
- Doorway pages -> consolidate or add unique content
- No local signals -> add GBP and citations

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Location page template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Doorway pages
- Action: consolidate or add unique content
- Output: Location page template.

## Dependencies (load only if needed)
- 07-local-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
