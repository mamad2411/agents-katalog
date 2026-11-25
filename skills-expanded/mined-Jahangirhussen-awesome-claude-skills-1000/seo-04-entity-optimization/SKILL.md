---
name: seo-04-entity-optimization
description: Entity optimization (SEO). Use when the request involves: entity seo, knowledge graph, sameas, brand entity. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Entity optimization

ID: 04.07 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
Entity optimization within the seo-master tree: Entity fact sheet and schema.

## When to use
Triggers: entity seo, knowledge graph, sameas, brand entity

## When NOT to use
- The topic is covered by a sibling skill: `../content-optimization`, `../headings`, `../internal-linking`, `../meta-descriptions`, `../title-tags`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Define the main entities (brand, people, products, places) and consistent names
2. Add Organization/Person schema with sameAs to official profiles
3. Align facts across site, Google Business Profile, LinkedIn, Wikipedia/Wikidata where valid
4. Use clear 'about' content and author pages

## Decision rules and checks
- Consistent name/description/NAP
- Organization + sameAs schema
- Wikipedia/Wikidata/LinkedIn alignment where valid

## Edge cases and failure handling
- Inconsistent brand naming -> standardize
- No notable presence -> earn mentions on credible sites

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Entity fact sheet and schema. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Inconsistent brand naming
- Action: standardize
- Output: Entity fact sheet and schema.

## External sources merged (deep method)
- `../../_source/aaron__entity-optimizer/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
