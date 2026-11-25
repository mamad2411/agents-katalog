---
name: seo-18-international-architecture
description: International architecture (SEO). Use when the request involves: international site structure. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# International architecture

ID: 18.04 | Level: child | Parent: [International SEO](../SKILL.md)

## Purpose
International architecture within the seo-master tree: Architecture diagram.

## When to use
Triggers: international site structure

## When NOT to use
- The topic is covered by a sibling skill: `../country-targeting`, `../hreflang`, `../multilingual`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: hreflang validator or Screaming Frog hreflang tab, GSC international targeting data, localization team, sitemap.

## Core workflow
1. Prefer subfolders (/de/) for shared authority
2. Language switcher with crawlable links
3. Keep consistent URL patterns
4. Separate sitemaps per locale optional

## Decision rules and checks
- Prefer subfolders unless strong reason
- Language switcher crawlable
- No auto-redirect by IP for bots

## Edge cases and failure handling
- Mixed structures -> unify
- Missing x-default -> add

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Architecture diagram. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Mixed structures
- Action: unify
- Output: Architecture diagram.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
