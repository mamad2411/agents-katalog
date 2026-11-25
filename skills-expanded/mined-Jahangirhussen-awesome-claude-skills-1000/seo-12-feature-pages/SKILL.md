---
name: seo-12-feature-pages
description: Feature pages (SEO). Use when the request involves: feature page, use case. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Feature pages

ID: 12.02 | Level: child | Parent: [SaaS SEO](../SKILL.md)

## Purpose
Feature pages within the seo-master tree: Feature page template.

## When to use
Triggers: feature page, use case

## When NOT to use
- The topic is covered by a sibling skill: `../comparison-pages`, `../integration-pages`, `../landing-pages`, `../programmatic-saas`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs/Semrush competitor tools, GSC, analytics funnels, CMS, screenshot tools, schema validator.

## Core workflow
1. One page per major feature or use case with intent
2. Show screenshots/demos and real use cases
3. Internal links to related features, integrations, pricing

## Decision rules and checks
- One feature = one intent
- Screenshots + use cases
- Link to related features/integrations

## Edge cases and failure handling
- Thin feature pages -> add scenarios and outcomes
- Cannibalization with homepage -> differentiate

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Feature page template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Thin feature pages
- Action: add scenarios and outcomes
- Output: Feature page template.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
