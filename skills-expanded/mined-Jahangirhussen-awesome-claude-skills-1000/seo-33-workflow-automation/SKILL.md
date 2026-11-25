---
name: seo-33-workflow-automation
description: Workflow automation (SEO). Use when the request involves: bulk metadata, internal link automation, schema generation, sitemap automation. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Workflow automation

ID: 33.04 | Level: child | Parent: [SEO Automation](../SKILL.md)

## Purpose
Workflow automation within the seo-master tree: Automation scripts spec.

## When to use
Triggers: bulk metadata, internal link automation, schema generation, sitemap automation

## When NOT to use
- The topic is covered by a sibling skill: `../automated-audits`, `../automated-monitoring`, `../automated-reporting`, `../seo-agents`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Python/Node scripts, cron or CI, GSC/GA4 APIs, Screaming Frog CLI, Slack/email webhooks, version control.

## Core workflow
1. Template-based metadata with variables and human review
2. Schema generator validated before publish
3. Sitemap rebuild on publish; internal link suggestions
4. Log every change

## Decision rules and checks
- Template-based metadata with review
- Schema generator validated
- Sitemap rebuild on publish

## Edge cases and failure handling
- Duplicate generated metadata -> add unique attributes

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Automation scripts spec. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate generated metadata
- Action: add unique attributes
- Output: Automation scripts spec.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
