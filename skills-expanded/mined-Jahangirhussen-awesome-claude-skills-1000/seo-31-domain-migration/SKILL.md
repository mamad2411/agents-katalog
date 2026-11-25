---
name: seo-31-domain-migration
description: Domain migration (SEO). Use when the request involves: domain change, rebrand domain. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Domain migration

ID: 31.01 | Level: child | Parent: [SEO Migration](../SKILL.md)

## Purpose
Domain migration within the seo-master tree: Domain move runbook.

## When to use
Triggers: domain change, rebrand domain

## When NOT to use
- The topic is covered by a sibling skill: `../migration-monitoring`, `../platform-migration`, `../url-migration`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (before/after crawls), redirect mapping sheet, GSC Change of Address, server config, log analysis.

## Core workflow
1. 301 old domain to new, URL to URL
2. Use GSC Change of Address (domain properties)
3. Update canonicals, sitemap, hreflang, internal links, GBP, social, key backlinks
4. Keep old domain active and redirected for 1+ year

## Decision rules and checks
- 1:1 301 map
- GSC change of address
- Update canonicals, sitemaps, backlinks

## Edge cases and failure handling
- Dropping redirects early -> keep long term

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Domain move runbook. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Dropping redirects early
- Action: keep long term
- Output: Domain move runbook.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
