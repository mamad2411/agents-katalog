---
name: seo-32-alerts
description: Alerts (SEO). Use when the request involves: seo alerts. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Alerts

ID: 32.05 | Level: child | Parent: [SEO Monitoring](../SKILL.md)

## Purpose
Alerts within the seo-master tree: Alert rules.

## When to use
Triggers: seo alerts

## When NOT to use
- The topic is covered by a sibling skill: `../indexing`, `../rankings`, `../technical-errors`, `../traffic`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC, GA4, rank tracker, scheduled crawler, uptime monitor, alerting (Slack/email).

## Core workflow
1. Define thresholds (clicks -20% week over week, indexed -10%, 5xx > 1%)
2. Route to owner with runbook link
3. Review monthly

## Decision rules and checks
- Thresholds on clicks, indexing, errors
- Route to owner

## Edge cases and failure handling
- Too noisy -> raise thresholds

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Alert rules. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Too noisy
- Action: raise thresholds
- Output: Alert rules.

## External sources merged (deep method)
- `../../_source/aaron__alert-manager/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
