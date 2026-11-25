---
name: seo-32
description: 32. SEO Monitoring (SEO). Use when the request involves: seo monitoring, rank tracking, traffic drop, indexing monitoring, technical errors, alerts, seo drift. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 32. SEO Monitoring

ID: 32 | Level: parent | Parent: SEO Master

## Purpose
Detect and diagnose change.

## When to use
Triggers: seo monitoring, rank tracking, traffic drop, indexing monitoring, technical errors, alerts, seo drift

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: GSC, GA4, rank tracker, scheduled crawler, uptime monitor, alerting (Slack/email).

## Core workflow
1. Baseline metrics; define thresholds
2. Monitor rankings, indexing, traffic, CWV, errors, backlinks, AI visibility
3. Diagnose cause before acting

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Alert fatigue -> tune thresholds

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Monitoring setup and alert rules. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Alert fatigue
- Action: tune thresholds
- Output: Monitoring setup and alert rules.

## Children
- [Rank tracking](rankings/SKILL.md)
- [Indexing monitoring](indexing/SKILL.md)
- [Traffic diagnosis](traffic/SKILL.md)
- [Technical error monitoring](technical-errors/SKILL.md)
- [Alerts](alerts/SKILL.md)

## Related installed skills (kept in place; invoke only if needed)
- `monitoring-and-alerting`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
