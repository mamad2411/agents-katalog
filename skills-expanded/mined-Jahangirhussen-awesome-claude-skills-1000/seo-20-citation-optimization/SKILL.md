---
name: seo-20-citation-optimization
description: Citation optimization (SEO). Use when the request involves: citation optimization. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Citation optimization

ID: 20.03 | Level: child | Parent: [GEO](../SKILL.md)

## Purpose
Citation optimization within the seo-master tree: Citable-statements list.

## When to use
Triggers: citation optimization

## When NOT to use
- The topic is covered by a sibling skill: `../ai-brand-visibility`, `../entity-visibility`, `../generative-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, AI engines, citation checks, schema validator, brand mention monitoring.

## Core workflow
1. Publish unique facts others will cite
2. Make them easy to quote (short, specific, dated)
3. Link out to primary sources

## Decision rules and checks
- Quotable stats, sourced claims
- See 19-ai-seo/ai-citations

## Edge cases and failure handling
- Claims without sources -> add references

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Citable-statements list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Claims without sources
- Action: add references
- Output: Citable-statements list.

## Dependencies (load only if needed)
- 19-ai-seo/ai-citations

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
