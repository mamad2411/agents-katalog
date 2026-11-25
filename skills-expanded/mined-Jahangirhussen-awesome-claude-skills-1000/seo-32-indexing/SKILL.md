---
name: seo-32-indexing
description: Indexing monitoring (SEO). Use when the request involves: index monitoring. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Indexing monitoring

ID: 32.02 | Level: child | Parent: [SEO Monitoring](../SKILL.md)

## Purpose
Indexing monitoring within the seo-master tree: Indexing log.

## When to use
Triggers: index monitoring

## When NOT to use
- The topic is covered by a sibling skill: `../alerts`, `../rankings`, `../technical-errors`, `../traffic`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC, GA4, rank tracker, scheduled crawler, uptime monitor, alerting (Slack/email).

## Core workflow
1. Track GSC indexed pages vs sitemap
2. Alert on spikes in 'excluded' or 'not indexed'
3. Spot-check with URL Inspection

## Decision rules and checks
- GSC indexed count vs sitemap
- Alert on spikes in excluded

## Edge cases and failure handling
- Sudden deindex -> check noindex/robots/server

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Indexing log. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Sudden deindex
- Action: check noindex/robots/server
- Output: Indexing log.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
