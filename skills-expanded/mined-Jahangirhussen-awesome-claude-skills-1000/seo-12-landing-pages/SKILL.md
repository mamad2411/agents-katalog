---
name: seo-12-landing-pages
description: Landing pages (SEO). Use when the request involves: saas landing page. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Landing pages

ID: 12.01 | Level: child | Parent: [SaaS SEO](../SKILL.md)

## Purpose
Landing pages within the seo-master tree: Landing page brief.

## When to use
Triggers: saas landing page

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../feature-pages`, `../integration-pages`, `../programmatic-saas`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs/Semrush competitor tools, GSC, analytics funnels, CMS, screenshot tools, schema validator.

## Core workflow
1. Target one primary intent per page
2. Benefit-led H1, proof (logos, numbers, testimonials), clear CTA
3. SoftwareApplication/Product + Organization schema
4. Fast, accessible, indexable

## Decision rules and checks
- One primary intent
- Benefit-led H1 + proof + CTA
- Schema: SoftwareApplication

## Edge cases and failure handling
- Generic homepage trying to rank for everything -> split by use case
- JS-heavy hero -> ensure SSR

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Landing page brief. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Generic homepage trying to rank for everything
- Action: split by use case
- Output: Landing page brief.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
