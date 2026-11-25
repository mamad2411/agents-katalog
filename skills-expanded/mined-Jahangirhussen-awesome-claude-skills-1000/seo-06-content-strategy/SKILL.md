---
name: seo-06-content-strategy
description: Content strategy (SEO). Use when the request involves: content strategy, content calendar, content brief. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Content strategy

ID: 06.01 | Level: child | Parent: [Content SEO](../SKILL.md)

## Purpose
Content strategy within the seo-master tree: Calendar with briefs.

## When to use
Triggers: content strategy, content calendar, content brief

## When NOT to use
- The topic is covered by a sibling skill: `../content-clusters`, `../content-gap`, `../content-refresh`, `../seo-copywriting`, `../topical-authority`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush content gap, SERP analysis, content brief template, CMS.

## Core workflow
1. Define audience, funnel stages, and business goals
2. Map topics to funnel (awareness, consideration, decision)
3. Create briefs: intent, outline, entities, internal links, schema, CTA
4. Set a realistic calendar and review loop

## Decision rules and checks
- Audience + intent + funnel stage
- Brief: intent, outline, entities, links, schema
- Calendar tied to clusters

## Edge cases and failure handling
- Topics without business tie -> add conversion path
- No expert input -> add SMEs/authors

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Calendar with briefs. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Topics without business tie
- Action: add conversion path
- Output: Calendar with briefs.

## Dependencies (load only if needed)
- content-strategy (installed skill)

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
