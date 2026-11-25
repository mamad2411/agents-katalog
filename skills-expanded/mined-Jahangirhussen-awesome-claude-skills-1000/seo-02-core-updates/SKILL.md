---
name: seo-02-core-updates
description: Core updates and volatility (SEO). Use when the request involves: core update, algorithm update, ranking drop, helpful content. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Core updates and volatility

ID: 02.03 | Level: child | Parent: [Google SEO](../SKILL.md)

## Purpose
Core updates and volatility within the seo-master tree: Impact analysis: affected segments, hypotheses, actions.

## When to use
Triggers: core update, algorithm update, ranking drop, helpful content

## When NOT to use
- The topic is covered by a sibling skill: `../indexing`, `../search-console`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Google Search Console (+API), GA4, URL Inspection tool, Search Status Dashboard, Looker Studio.

## Core workflow
1. Get update dates from Google Search Status Dashboard
2. Overlay GSC clicks on dates; segment by page type and query class
3. Compare winners vs losers on intent match, expertise, UX, ads, content freshness
4. Improve content quality and E-E-A-T on affected sections; wait for next update to judge

## Decision rules and checks
- Align drop date with update date in GSC
- Segment by page type/query
- Fix quality/intent mismatch; do not chase tricks

## Edge cases and failure handling
- Tempted to change everything -> change only affected segment, log changes
- No recovery in weeks -> normal; recoveries often arrive with later updates

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Impact analysis: affected segments, hypotheses, actions. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Tempted to change everything
- Action: change only affected segment, log changes
- Output: Impact analysis: affected segments, hypotheses, actions.

## Dependencies (load only if needed)
- 32-seo-monitoring/traffic

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
