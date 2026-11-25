---
name: seo-03-website-architecture
description: Website architecture (SEO). Use when the request involves: site structure, url hierarchy, navigation, silo, breadcrumbs, information architecture. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Website architecture

ID: 03.11 | Level: child | Parent: [Technical SEO](../SKILL.md)

## Purpose
Website architecture within the seo-master tree: Architecture diagram and migration notes.

## When to use
Triggers: site structure, url hierarchy, navigation, silo, breadcrumbs, information architecture

## When NOT to use
- The topic is covered by a sibling skill: `../canonical`, `../core-web-vitals`, `../crawlability`, `../https`, `../indexability`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog or Sitebulb, Google Search Console, Lighthouse, PageSpeed Insights, CrUX, WebPageTest, curl -I, server logs.

## Core workflow
1. Map content into hierarchy: home > category > subcategory > page
2. Keep important pages within 3 clicks; URLs mirror hierarchy
3. Use hub pages and breadcrumbs; link hubs to children and back
4. Avoid deep or flat extremes; merge thin branches

## Decision rules and checks
- Flat, logical hierarchy
- Clean URL patterns
- Breadcrumbs + nav match hierarchy
- Hub pages link to children

## Edge cases and failure handling
- Orphan sections -> link from hubs and nav
- Duplicate paths to same content -> choose one canonical path

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Architecture diagram and migration notes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Orphan sections
- Action: link from hubs and nav
- Output: Architecture diagram and migration notes.

## Dependencies (load only if needed)
- site-architecture (installed skill)

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
