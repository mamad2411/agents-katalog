---
name: seo-33-automated-audits
description: Automated audits (SEO). Use when the request involves: scheduled audit. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Automated audits

ID: 33.01 | Level: child | Parent: [SEO Automation](../SKILL.md)

## Purpose
Automated audits within the seo-master tree: Scheduled audit job.

## When to use
Triggers: scheduled audit

## When NOT to use
- The topic is covered by a sibling skill: `../automated-monitoring`, `../automated-reporting`, `../seo-agents`, `../workflow-automation`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Python/Node scripts, cron or CI, GSC/GA4 APIs, Screaming Frog CLI, Slack/email webhooks, version control.

## Core workflow
1. Schedule crawls (weekly) and diff against previous
2. Fail CI on regressions: noindex, canonical, status
3. Send summary to owner

## Decision rules and checks
- Scheduled crawl + diff
- Fail on regressions

## Edge cases and failure handling
- Flaky checks -> pin crawl settings

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Scheduled audit job. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Flaky checks
- Action: pin crawl settings
- Output: Scheduled audit job.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
