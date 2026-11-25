---
name: seo-18-hreflang
description: Hreflang (SEO). Use when the request involves: hreflang, x-default. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Hreflang

ID: 18.01 | Level: child | Parent: [International SEO](../SKILL.md)

## Purpose
Hreflang within the seo-master tree: Hreflang map.

## When to use
Triggers: hreflang, x-default

## When NOT to use
- The topic is covered by a sibling skill: `../country-targeting`, `../international-architecture`, `../multilingual`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: hreflang validator or Screaming Frog hreflang tab, GSC international targeting data, localization team, sitemap.

## Core workflow
1. Use ISO 639-1 language and ISO 3166-1 region codes
2. Every page references all alternates including itself and x-default
3. Alternates must be reciprocal; canonicals self-referencing per locale
4. Implement via HTML, headers, or sitemap

## Decision rules and checks
- Reciprocal tags + x-default
- Valid language-region codes
- Self-referencing canonical per locale

## Edge cases and failure handling
- Non-reciprocal tags ignored -> fix both sides
- Wrong codes (en-uk) -> en-gb

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Hreflang map. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Non-reciprocal tags ignored
- Action: fix both sides
- Output: Hreflang map.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
