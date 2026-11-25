---
name: seo-27-faq
description: FAQPage (SEO). Use when the request involves: faq schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# FAQPage

ID: 27.05 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
FAQPage within the seo-master tree: FAQ JSON-LD.

## When to use
Triggers: faq schema

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../breadcrumb`, `../local-business`, `../organization`, `../product`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. FAQPage with Question/acceptedAnswer
2. Content must be visible on the page
3. Rich results limited to certain sites; markup still helps machines

## Decision rules and checks
- Only for visible Q&A; note Google limits rich results

## Edge cases and failure handling
- Promotional FAQs -> not eligible

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
FAQ JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Promotional FAQs
- Action: not eligible
- Output: FAQ JSON-LD.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
