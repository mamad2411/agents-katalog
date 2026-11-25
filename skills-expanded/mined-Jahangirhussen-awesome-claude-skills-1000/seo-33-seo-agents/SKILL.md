---
name: seo-33-seo-agents
description: SEO agents (SEO). Use when the request involves: seo agent. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# SEO agents

ID: 33.05 | Level: child | Parent: [SEO Automation](../SKILL.md)

## Purpose
SEO agents within the seo-master tree: Agent spec.

## When to use
Triggers: seo agent

## When NOT to use
- The topic is covered by a sibling skill: `../automated-audits`, `../automated-monitoring`, `../automated-reporting`, `../workflow-automation`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Python/Node scripts, cron or CI, GSC/GA4 APIs, Screaming Frog CLI, Slack/email webhooks, version control.

## Core workflow
1. Define scope, tools, and guardrails (read-only by default)
2. Require approval for writes; keep action log
3. Evaluate on a sample before scaling

## Decision rules and checks
- Scope + guardrails
- Read-only by default; write with approval log

## Edge cases and failure handling
- Agent edits unrelated areas -> restrict paths

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Agent spec. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Agent edits unrelated areas
- Action: restrict paths
- Output: Agent spec.

## External sources merged (deep method)
- `../../_source/aaron__memory-management/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
