---
name: seo-18-multilingual
description: Multilingual content (SEO). Use when the request involves: translation, localization. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Multilingual content

ID: 18.02 | Level: child | Parent: [International SEO](../SKILL.md)

## Purpose
Multilingual content within the seo-master tree: Localization checklist.

## When to use
Triggers: translation, localization

## When NOT to use
- The topic is covered by a sibling skill: `../country-targeting`, `../hreflang`, `../international-architecture`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: hreflang validator or Screaming Frog hreflang tab, GSC international targeting data, localization team, sitemap.

## Core workflow
1. Use professional/native localization incl. keywords, currency, units
2. Translate metadata, schema, alt text, URLs where sensible
3. Avoid machine translation without review

## Decision rules and checks
- Human-quality localization
- Localized URLs, titles, schema

## Edge cases and failure handling
- Duplicate content across locales -> hreflang + unique local elements

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Localization checklist. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate content across locales
- Action: hreflang + unique local elements
- Output: Localization checklist.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
