---
name: seo-32-technical-errors
description: Technical error monitoring (SEO). Use when the request involves: 5xx, 404 spike, cwv regression. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Technical error monitoring

ID: 32.04 | Level: child | Parent: [SEO Monitoring](../SKILL.md)

## Purpose
Technical error monitoring within the seo-master tree: Error dashboard.

## When to use
Triggers: 5xx, 404 spike, cwv regression

## When NOT to use
- The topic is covered by a sibling skill: `../alerts`, `../indexing`, `../rankings`, `../traffic`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC, GA4, rank tracker, scheduled crawler, uptime monitor, alerting (Slack/email).

## Core workflow
1. Scheduled crawl + status code diff
2. Alert on 5xx/404 spikes, CWV regressions, robots/noindex changes

## Decision rules and checks
- Crawl diff
- Status code and CWV regression alerts

## Edge cases and failure handling
- Deploy regressions -> add SEO checks to CI

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Error dashboard. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Deploy regressions
- Action: add SEO checks to CI
- Output: Error dashboard.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
