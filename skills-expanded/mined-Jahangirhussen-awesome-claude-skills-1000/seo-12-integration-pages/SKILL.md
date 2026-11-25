---
name: seo-12-integration-pages
description: Integration pages (SEO). Use when the request involves: integration page, app marketplace. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Integration pages

ID: 12.04 | Level: child | Parent: [SaaS SEO](../SKILL.md)

## Purpose
Integration pages within the seo-master tree: Integration page template.

## When to use
Triggers: integration page, app marketplace

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../feature-pages`, `../landing-pages`, `../programmatic-saas`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs/Semrush competitor tools, GSC, analytics funnels, CMS, screenshot tools, schema validator.

## Core workflow
1. One page per integration with what it does, setup steps, use cases
2. Link to partner docs and your docs
3. Add to a hub page listing integrations

## Decision rules and checks
- One page per integration
- How it works + setup + use cases

## Edge cases and failure handling
- Auto-generated near-duplicates -> add unique use cases
- No partner collaboration -> co-market for links

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Integration page template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Auto-generated near-duplicates
- Action: add unique use cases
- Output: Integration page template.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
