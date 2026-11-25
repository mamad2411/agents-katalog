---
name: seo-27-article
description: Article / BlogPosting (SEO). Use when the request involves: article schema. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Article / BlogPosting

ID: 27.04 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
Article / BlogPosting within the seo-master tree: Article JSON-LD.

## When to use
Triggers: article schema

## When NOT to use
- The topic is covered by a sibling skill: `../breadcrumb`, `../faq`, `../local-business`, `../organization`, `../product`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Article/BlogPosting: headline, image, author, datePublished, dateModified, publisher
2. Author as Person with url
3. Keep dates accurate

## Decision rules and checks
- headline, author, datePublished, dateModified, image

## Edge cases and failure handling
- Missing images -> add featured image

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Article JSON-LD. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Missing images
- Action: add featured image
- Output: Article JSON-LD.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
