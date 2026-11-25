---
name: seo-20-entity-visibility
description: Entity visibility (SEO). Use when the request involves: entity authority, knowledge graph. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Entity visibility

ID: 20.02 | Level: child | Parent: [GEO](../SKILL.md)

## Purpose
Entity visibility within the seo-master tree: Entity fact sheet.

## When to use
Triggers: entity authority, knowledge graph

## When NOT to use
- The topic is covered by a sibling skill: `../ai-brand-visibility`, `../citation-optimization`, `../generative-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, AI engines, citation checks, schema validator, brand mention monitoring.

## Core workflow
1. Ensure Organization/Person schema with sameAs
2. Maintain consistent descriptions across web profiles
3. Pursue Wikipedia/Wikidata only when notability criteria are met

## Decision rules and checks
- Org/Person schema + sameAs
- Consistent descriptions across web

## Edge cases and failure handling
- Brand confused with another entity -> disambiguate on about page

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Entity fact sheet. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Brand confused with another entity
- Action: disambiguate on about page
- Output: Entity fact sheet.

## Dependencies (load only if needed)
- 04-on-page-seo/entity-optimization

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
