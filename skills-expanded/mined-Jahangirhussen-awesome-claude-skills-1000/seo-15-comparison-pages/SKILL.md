---
name: seo-15-comparison-pages
description: Programmatic comparisons (SEO). Use when the request involves: comparison at scale. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Programmatic comparisons

ID: 15.04 | Level: child | Parent: [Programmatic SEO](../SKILL.md)

## Purpose
Programmatic comparisons within the seo-master tree: Comparison dataset and template.

## When to use
Triggers: comparison at scale

## When NOT to use
- The topic is covered by a sibling skill: `../database-pages`, `../location-pages`, `../programmatic-internal-linking`, `../template-pages`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Dataset or database, template engine, Screaming Frog, GSC (indexing), sitemap generator, QA sampling script.

## Core workflow
1. Use accurate data and dates
2. Focus on valuable pairs only
3. Add decision guidance

## Decision rules and checks
- Accurate data + dates
- Avoid thin permutations

## Edge cases and failure handling
- Thin permutations -> prune
- Out-of-date specs -> automate refresh

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Comparison dataset and template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Thin permutations
- Action: prune
- Output: Comparison dataset and template.

## Dependencies (load only if needed)
- 12-saas-seo/comparison-pages

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
