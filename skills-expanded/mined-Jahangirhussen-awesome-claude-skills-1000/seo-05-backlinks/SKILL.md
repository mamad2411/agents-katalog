---
name: seo-05-backlinks
description: Backlink analysis (SEO). Use when the request involves: backlink profile, referring domains, anchor distribution. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Backlink analysis

ID: 05.02 | Level: child | Parent: [Off-Page SEO](../SKILL.md)

## Purpose
Backlink analysis within the seo-master tree: Backlink profile summary and reclaim list.

## When to use
Triggers: backlink profile, referring domains, anchor distribution

## When NOT to use
- The topic is covered by a sibling skill: `../brand-mentions`, `../digital-pr`, `../guest-posting`, `../link-audit`, `../link-building`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs, Semrush, Majestic, Google Search Console Links report, Google Alerts, outreach CRM or spreadsheet.

## Core workflow
1. Export referring domains and anchors
2. Segment by authority, relevance, follow/nofollow, country
3. Find top linked pages and lost/broken links to reclaim
4. Check anchor distribution is natural (mostly brand/URL)

## Decision rules and checks
- Referring domains quality/trend
- Anchor distribution natural
- Competitor link gap

## Edge cases and failure handling
- Lost valuable links -> contact site, restore page or 301
- Spammy sudden spike -> monitor, disavow only if harmful

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Backlink profile summary and reclaim list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Lost valuable links
- Action: contact site, restore page or 301
- Output: Backlink profile summary and reclaim list.

## External sources merged (deep method)
- `../../_source/aaron__domain-authority-auditor/SKILL.md`
- `../../_source/aaron__backlink-analyzer/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
