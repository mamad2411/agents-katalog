---
name: seo-27-review
description: Review and AggregateRating (SEO). Use when the request involves: review schema, rating. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Review and AggregateRating

ID: 27.07 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
Review and AggregateRating within the seo-master tree: Review JSON-LD rules.

## When to use
Triggers: review schema, rating

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../breadcrumb`, `../faq`, `../local-business`, `../organization`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Review/AggregateRating only for real, visible reviews
2. No self-serving reviews of your own organization
3. Include itemReviewed

## Decision rules and checks
- Real, visible reviews only
- No self-serving ratings for Organization

## Edge cases and failure handling
- Fake or copied ratings -> remove

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Review JSON-LD rules. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Fake or copied ratings
- Action: remove
- Output: Review JSON-LD rules.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
