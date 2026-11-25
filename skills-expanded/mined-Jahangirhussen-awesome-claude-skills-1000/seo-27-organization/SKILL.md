---
name: seo-27-organization
description: Organization (SEO). Use when the request involves: organization schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Organization

ID: 27.01 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
Organization within the seo-master tree: Organization JSON-LD.

## When to use
Triggers: organization schema

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../breadcrumb`, `../faq`, `../local-business`, `../product`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Organization: name, url, logo, sameAs, contactPoint, foundingDate
2. Place once site-wide (homepage or global)
3. Link Person authors via @id

## Decision rules and checks
- name, url, logo, sameAs, contactPoint

## Edge cases and failure handling
- Logo size/format invalid -> use clear PNG/SVG

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Organization JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Logo size/format invalid
- Action: use clear PNG/SVG
- Output: Organization JSON-LD.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
