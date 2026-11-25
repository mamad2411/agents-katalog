---
name: seo-01-seo-strategy
description: SEO strategy and roadmap (SEO). Use when the request involves: seo strategy, seo plan, roadmap, kpis, prioritization. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# SEO strategy and roadmap

ID: 01.02 | Level: child | Parent: [Core SEO](../SKILL.md)

## Purpose
SEO strategy and roadmap within the seo-master tree: One-page roadmap with ranked initiatives and expected impact.

## When to use
Triggers: seo strategy, seo plan, roadmap, kpis, prioritization

## When NOT to use
- The topic is covered by a sibling skill: `../competitor-analysis`, `../keyword-research`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console, GA4, Ahrefs/Semrush (keywords, competitors), Google Trends, AnswerThePublic, a spreadsheet.

## Core workflow
1. Audit current state (technical, content, links) in the shallowest useful pass
2. List opportunities: quick wins (titles, internal links, striking-distance 8-20), structural (architecture, clusters), authority (links, PR)
3. Sequence: fix blockers -> publish/refresh -> build authority
4. Define reporting cadence and review dates

## Decision rules and checks
- Goal + KPI + baseline
- Audit -> opportunities -> impact/effort ranking
- Phased 30/60/90 roadmap
- Resource + budget notes

## Edge cases and failure handling
- Strategy without ownership stalls -> assign each action
- Chasing algorithm rumors -> anchor to user intent and evidence

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
One-page roadmap with ranked initiatives and expected impact. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Strategy without ownership stalls
- Action: assign each action
- Output: One-page roadmap with ranked initiatives and expected impact.

## Merged from (read for deep method)
- `../../_source/seo-specialist/SKILL.md`

## External sources merged (deep method)
- `../../_source/borghei__seo-specialist/SKILL.md`
- `../../_source/nurdamiron__seo/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
