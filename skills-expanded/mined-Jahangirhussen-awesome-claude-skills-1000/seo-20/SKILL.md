---
name: seo-20
description: 20. GEO (SEO). Use when the request involves: geo, generative engine optimization, ai overviews, generative search, ai brand visibility, entity authority. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 20. GEO

ID: 20 | Level: parent | Parent: SEO Master

## Purpose
Visibility inside generative answers. Reuses 19 children for citations/visibility.

## When to use
Triggers: geo, generative engine optimization, ai overviews, generative search, ai brand visibility, entity authority

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, AI engines, citation checks, schema validator, brand mention monitoring.

## Core workflow
1. Identify target prompts/queries and who is cited today
2. Optimize passages for retrieval (clear, factual, unique)
3. Strengthen entity signals and third-party corroboration
4. Test and iterate

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Optimizing for one engine only -> keep fundamentals shared (see 19)

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
GEO action list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Optimizing for one engine only
- Action: keep fundamentals shared (see 19)
- Output: GEO action list.

## Children
- [Generative search](generative-search/SKILL.md)
- [Entity visibility](entity-visibility/SKILL.md)
- [Citation optimization](citation-optimization/SKILL.md)
- [AI brand visibility](ai-brand-visibility/SKILL.md)

## Merged from (read for deep method)
- `../_source/seo-aeo-geo/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
