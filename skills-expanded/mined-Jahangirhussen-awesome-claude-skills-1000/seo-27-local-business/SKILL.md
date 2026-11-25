---
name: seo-27-local-business
description: LocalBusiness (SEO). Use when the request involves: localbusiness schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# LocalBusiness

ID: 27.02 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
LocalBusiness within the seo-master tree: LocalBusiness JSON-LD.

## When to use
Triggers: localbusiness schema

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../breadcrumb`, `../faq`, `../organization`, `../product`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Use specific subtype (e.g. Dentist); address, geo, openingHoursSpecification, telephone, priceRange
2. Match GBP and visible NAP
3. One entity per location

## Decision rules and checks
- address, geo, openingHours, telephone

## Edge cases and failure handling
- Mismatched hours -> sync sources

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
LocalBusiness JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Mismatched hours
- Action: sync sources
- Output: LocalBusiness JSON-LD.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
