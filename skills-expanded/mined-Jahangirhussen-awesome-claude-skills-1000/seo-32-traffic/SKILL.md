---
name: seo-32-traffic
description: Traffic diagnosis (SEO). Use when the request involves: traffic drop, traffic decline. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Traffic diagnosis

ID: 32.03 | Level: child | Parent: [SEO Monitoring](../SKILL.md)

## Purpose
Traffic diagnosis within the seo-master tree: Traffic diagnosis memo.

## When to use
Triggers: traffic drop, traffic decline

## When NOT to use
- The topic is covered by a sibling skill: `../alerts`, `../indexing`, `../rankings`, `../technical-errors`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC, GA4, rank tracker, scheduled crawler, uptime monitor, alerting (Slack/email).

## Core workflow
1. Annotate drop date; compare GSC vs GA4
2. Segment by page group, query type, device, country
3. Match with deploys and algorithm updates
4. Pick cause before changing things

## Decision rules and checks
- Date of change vs releases/updates
- Segment by page/query/device
- Pick cause before acting

## Edge cases and failure handling
- Tracking broken -> verify GA4 tag before panic

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Traffic diagnosis memo. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Tracking broken
- Action: verify GA4 tag before panic
- Output: Traffic diagnosis memo.

## Merged from (read for deep method)
- `../../_source/seo-traffic-diagnosis/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
