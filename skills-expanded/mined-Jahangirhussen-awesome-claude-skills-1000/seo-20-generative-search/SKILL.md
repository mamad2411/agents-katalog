---
name: seo-20-generative-search
description: Generative search (SEO). Use when the request involves: generative search, google ai overviews, copilot. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Generative search

ID: 20.01 | Level: child | Parent: [GEO](../SKILL.md)

## Purpose
Generative search within the seo-master tree: Page restructure plan.

## When to use
Triggers: generative search, google ai overviews, copilot

## When NOT to use
- The topic is covered by a sibling skill: `../ai-brand-visibility`, `../citation-optimization`, `../entity-visibility`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, AI engines, citation checks, schema validator, brand mention monitoring.

## Core workflow
1. Cover sub-questions the model will fan out into
2. Provide definitions, comparisons, pros/cons, steps in clean formats
3. Use stats with sources; avoid fluff

## Decision rules and checks
- Passage-level optimization
- Cover query fan-out subtopics
- Comparison/definition formats

## Edge cases and failure handling
- Overlong intros -> answer first

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Page restructure plan. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Overlong intros
- Action: answer first
- Output: Page restructure plan.

## External sources merged (deep method)
- `../../_source/aaron__geo-content-optimizer/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
