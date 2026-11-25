---
name: seo-20-ai-brand-visibility
description: AI brand visibility (SEO). Use when the request involves: brand visibility in ai. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# AI brand visibility

ID: 20.04 | Level: child | Parent: [GEO](../SKILL.md)

## Purpose
AI brand visibility within the seo-master tree: Brand perception report.

## When to use
Triggers: brand visibility in ai

## When NOT to use
- The topic is covered by a sibling skill: `../citation-optimization`, `../entity-visibility`, `../generative-search`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Prompt tracking sheet, AI engines, citation checks, schema validator, brand mention monitoring.

## Core workflow
1. Get included in comparison lists, reviews, 'best X' articles
2. Encourage honest customer reviews and case studies
3. Monitor how AIs describe the brand; correct inaccuracies at source

## Decision rules and checks
- Brand mentions on trusted sites
- Reviews, comparisons, listicles

## Edge cases and failure handling
- Wrong facts in AI answers -> fix sources they rely on

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Brand perception report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Wrong facts in AI answers
- Action: fix sources they rely on
- Output: Brand perception report.

## Dependencies (load only if needed)
- 19-ai-seo/ai-visibility

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
