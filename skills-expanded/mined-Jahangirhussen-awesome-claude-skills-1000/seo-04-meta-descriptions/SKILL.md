---
name: seo-04-meta-descriptions
description: Meta descriptions (SEO). Use when the request involves: meta description, snippet. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Meta descriptions

ID: 04.02 | Level: child | Parent: [On-Page SEO](../SKILL.md)

## Purpose
Meta descriptions within the seo-master tree: Meta table: URL, current, proposed.

## When to use
Triggers: meta description, snippet

## When NOT to use
- The topic is covered by a sibling skill: `../content-optimization`, `../entity-optimization`, `../headings`, `../internal-linking`, `../title-tags`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Write unique descriptions ~140-160 chars with benefit + CTA
2. Include primary term naturally; match the query intent
3. For templates, build patterns with product/location variables

## Decision rules and checks
- ~140-160 chars, benefit + CTA
- Unique per URL; Google may rewrite
- Include primary term naturally

## Edge cases and failure handling
- Description ignored by Google -> it may rewrite; keep it accurate
- Duplicate descriptions -> unique or omit

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Meta table: URL, current, proposed. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Description ignored by Google
- Action: it may rewrite; keep it accurate
- Output: Meta table: URL, current, proposed.

## External sources merged (deep method)
- `../../_source/aaron__meta-tags-optimizer/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
