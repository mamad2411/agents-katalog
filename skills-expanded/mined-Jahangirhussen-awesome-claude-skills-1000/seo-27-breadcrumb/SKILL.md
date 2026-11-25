---
name: seo-27-breadcrumb
description: BreadcrumbList (SEO). Use when the request involves: breadcrumb schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# BreadcrumbList

ID: 27.06 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
BreadcrumbList within the seo-master tree: Breadcrumb JSON-LD.

## When to use
Triggers: breadcrumb schema

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../faq`, `../local-business`, `../organization`, `../product`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. BreadcrumbList with ListItem position, name, item
2. Match visible breadcrumb trail

## Decision rules and checks
- Match visible breadcrumb trail

## Edge cases and failure handling
- Trail differs from UI -> align

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Breadcrumb JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Trail differs from UI
- Action: align
- Output: Breadcrumb JSON-LD.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
