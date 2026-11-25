---
name: seo-33-automated-reporting
description: Automated reporting (SEO). Use when the request involves: automated seo report. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Automated reporting

ID: 33.02 | Level: child | Parent: [SEO Automation](../SKILL.md)

## Purpose
Automated reporting within the seo-master tree: Report pipeline.

## When to use
Triggers: automated seo report

## When NOT to use
- The topic is covered by a sibling skill: `../automated-audits`, `../automated-monitoring`, `../seo-agents`, `../workflow-automation`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Python/Node scripts, cron or CI, GSC/GA4 APIs, Screaming Frog CLI, Slack/email webhooks, version control.

## Core workflow
1. Pull GSC/GA4 via API on schedule
2. Render report template; highlight changes
3. Store history

## Decision rules and checks
- GSC/GA4 pull -> report template

## Edge cases and failure handling
- API limits -> incremental pulls

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Report pipeline. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: API limits
- Action: incremental pulls
- Output: Report pipeline.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
