---
name: seo-33
description: 33. SEO Automation (SEO). Use when the request involves: automate seo, automated audit, automated reporting, seo workflow, seo agent, bulk metadata. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 33. SEO Automation

ID: 33 | Level: parent | Parent: SEO Master

## Purpose
Automate proven manual work.

## When to use
Triggers: automate seo, automated audit, automated reporting, seo workflow, seo agent, bulk metadata

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Python/Node scripts, cron or CI, GSC/GA4 APIs, Screaming Frog CLI, Slack/email webhooks, version control.

## Core workflow
1. Automate only proven manual steps
2. Read-only first; writes need approval and logging
3. Version outputs; allow rollback

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Automation breaking sites -> staging and dry-run

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Automation plan with guardrails. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Automation breaking sites
- Action: staging and dry-run
- Output: Automation plan with guardrails.

## Children
- [Automated audits](automated-audits/SKILL.md)
- [Automated reporting](automated-reporting/SKILL.md)
- [Automated monitoring](automated-monitoring/SKILL.md)
- [Workflow automation](workflow-automation/SKILL.md)
- [SEO agents](seo-agents/SKILL.md)

## Topics handled here (no separate child)
- Automate only after the manual process works; human review for generated metadata; log changes with rollback

## Related installed skills (kept in place; invoke only if needed)
- `workflow-builder`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
