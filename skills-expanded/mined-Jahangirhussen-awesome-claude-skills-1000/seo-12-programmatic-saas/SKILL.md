---
name: seo-12-programmatic-saas
description: Programmatic SaaS pages (SEO). Use when the request involves: programmatic saas, templates at scale. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Programmatic SaaS pages

ID: 12.05 | Level: child | Parent: [SaaS SEO](../SKILL.md)

## Purpose
Programmatic SaaS pages within the seo-master tree: Batch plan and quality gate.

## When to use
Triggers: programmatic saas, templates at scale

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../feature-pages`, `../integration-pages`, `../landing-pages`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs/Semrush competitor tools, GSC, analytics funnels, CMS, screenshot tools, schema validator.

## Core workflow
1. Pick templates with unique data per page (integrations, templates, alternatives)
2. Ship a small batch, check indexing and engagement, then scale
3. Noindex pages below quality threshold

## Decision rules and checks
- Unique data per page
- Small batch first

## Edge cases and failure handling
- Index bloat -> prune
- Thin permutations -> add unique value or drop

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Batch plan and quality gate. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Index bloat
- Action: prune
- Output: Batch plan and quality gate.

## Dependencies (load only if needed)
- 15-programmatic-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
