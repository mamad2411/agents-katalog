---
name: seo-31-url-migration
description: URL migration (SEO). Use when the request involves: url structure change, redirect mapping, http to https. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# URL migration

ID: 31.03 | Level: child | Parent: [SEO Migration](../SKILL.md)

## Purpose
URL migration within the seo-master tree: Redirect map.

## When to use
Triggers: url structure change, redirect mapping, http to https

## When NOT to use
- The topic is covered by a sibling skill: `../domain-migration`, `../migration-monitoring`, `../platform-migration`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (before/after crawls), redirect mapping sheet, GSC Change of Address, server config, log analysis.

## Core workflow
1. Build mapping file (old, new, status)
2. Single-hop 301; update internal links/sitemaps
3. Avoid chains; handle query strings

## Decision rules and checks
- Mapping file
- Chain-free redirects
- Update internal links

## Edge cases and failure handling
- Mass redirect to homepage -> map to relevant pages

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Redirect map. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Mass redirect to homepage
- Action: map to relevant pages
- Output: Redirect map.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
