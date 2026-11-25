---
name: seo-18-country-targeting
description: Country targeting (SEO). Use when the request involves: geo targeting, cctld. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Country targeting

ID: 18.03 | Level: child | Parent: [International SEO](../SKILL.md)

## Purpose
Country targeting within the seo-master tree: Targeting matrix.

## When to use
Triggers: geo targeting, cctld

## When NOT to use
- The topic is covered by a sibling skill: `../hreflang`, `../international-architecture`, `../multilingual`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: hreflang validator or Screaming Frog hreflang tab, GSC international targeting data, localization team, sitemap.

## Core workflow
1. Choose structure to match business (ccTLD strongest signal)
2. Add local signals: currency, address, phone, local links
3. Use GSC where relevant

## Decision rules and checks
- ccTLD vs subfolder vs subdomain
- Local signals: currency, address, links

## Edge cases and failure handling
- Same content for multiple countries -> hreflang with regional variants

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Targeting matrix. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Same content for multiple countries
- Action: hreflang with regional variants
- Output: Targeting matrix.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
