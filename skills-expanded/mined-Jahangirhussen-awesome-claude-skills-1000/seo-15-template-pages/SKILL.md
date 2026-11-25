---
name: seo-15-template-pages
description: Template pages (SEO). Use when the request involves: template, dynamic landing pages. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Template pages

ID: 15.01 | Level: child | Parent: [Programmatic SEO](../SKILL.md)

## Purpose
Template pages within the seo-master tree: Template spec.

## When to use
Triggers: template, dynamic landing pages

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../database-pages`, `../location-pages`, `../programmatic-internal-linking`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Dataset or database, template engine, Screaming Frog, GSC (indexing), sitemap generator, QA sampling script.

## Core workflow
1. Design template with variable sections and fixed value blocks
2. Unique title/H1/intro from real data
3. Structured data where relevant

## Decision rules and checks
- Unique data/insight per page
- Variable titles/meta with real differentiation
- Small batch -> measure indexing

## Edge cases and failure handling
- Identical text across pages -> add differentiating data
- Too many variables -> keep readable

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Template spec. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Identical text across pages
- Action: add differentiating data
- Output: Template spec.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
