---
name: seo-32-rankings
description: Rank tracking (SEO). Use when the request involves: rank tracking, keyword rankings. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Rank tracking

ID: 32.01 | Level: child | Parent: [SEO Monitoring](../SKILL.md)

## Purpose
Rank tracking within the seo-master tree: Ranking report.

## When to use
Triggers: rank tracking, keyword rankings

## When NOT to use
- The topic is covered by a sibling skill: `../alerts`, `../indexing`, `../technical-errors`, `../traffic`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC, GA4, rank tracker, scheduled crawler, uptime monitor, alerting (Slack/email).

## Core workflow
1. Track keywords by segment with fixed location/device
2. Compare vs competitors; weekly trend
3. Use GSC average position as sanity check

## Decision rules and checks
- Track by purpose segments
- Compare vs competitors

## Edge cases and failure handling
- Rank tracker differs from GSC -> expected; use GSC for truth

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Ranking report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Rank tracker differs from GSC
- Action: expected; use GSC for truth
- Output: Ranking report.

## Merged from (read for deep method)
- `../../_source/seo-rank-tracking/SKILL.md`

## External sources merged (deep method)
- `../../_source/aaron__rank-tracker/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
