---
name: seo-33-automated-monitoring
description: Automated monitoring (SEO). Use when the request involves: automated monitoring. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Automated monitoring

ID: 33.03 | Level: child | Parent: [SEO Automation](../SKILL.md)

## Purpose
Automated monitoring within the seo-master tree: Monitoring job.

## When to use
Triggers: automated monitoring

## When NOT to use
- The topic is covered by a sibling skill: `../automated-audits`, `../automated-reporting`, `../seo-agents`, `../workflow-automation`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Python/Node scripts, cron or CI, GSC/GA4 APIs, Screaming Frog CLI, Slack/email webhooks, version control.

## Core workflow
1. Use alert rules from 32
2. Integrate with Slack/email
3. Include runbook links

## Decision rules and checks
- Alerts from 32-seo-monitoring

## Edge cases and failure handling
- Alert noise -> tune

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Monitoring job. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Alert noise
- Action: tune
- Output: Monitoring job.

## Dependencies (load only if needed)
- 32-seo-monitoring

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
