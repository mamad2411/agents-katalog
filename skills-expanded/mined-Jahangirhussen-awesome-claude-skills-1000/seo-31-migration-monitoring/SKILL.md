---
name: seo-31-migration-monitoring
description: Migration monitoring (SEO). Use when the request involves: post migration, ranking recovery. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Migration monitoring

ID: 31.04 | Level: child | Parent: [SEO Migration](../SKILL.md)

## Purpose
Migration monitoring within the seo-master tree: Post-launch monitoring log.

## When to use
Triggers: post migration, ranking recovery

## When NOT to use
- The topic is covered by a sibling skill: `../domain-migration`, `../platform-migration`, `../url-migration`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (before/after crawls), redirect mapping sheet, GSC Change of Address, server config, log analysis.

## Core workflow
1. Daily GSC for 30 days: indexing, errors, crawl stats
2. Compare crawl to baseline; fix 404s and redirect gaps
3. Track rankings and traffic by segment
4. Expect temporary fluctuation

## Decision rules and checks
- Daily GSC for 30 days
- Compare crawl to baseline
- Fix 404s/redirect gaps fast

## Edge cases and failure handling
- Persistent drop -> check canonical/robots/noindex first

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Post-launch monitoring log. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Persistent drop
- Action: check canonical/robots/noindex first
- Output: Post-launch monitoring log.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
