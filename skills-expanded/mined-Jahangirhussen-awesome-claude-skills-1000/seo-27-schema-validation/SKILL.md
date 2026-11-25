---
name: seo-27-schema-validation
description: Schema validation (SEO). Use when the request involves: validate schema, rich results test. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Schema validation

ID: 27.08 | Level: child | Parent: [Schema / Structured Data](../SKILL.md)

## Purpose
Schema validation within the seo-master tree: Validation report.

## When to use
Triggers: validate schema, rich results test

## When NOT to use
- The topic is covered by a sibling skill: `../article`, `../breadcrumb`, `../faq`, `../local-business`, `../organization`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Test URLs in Rich Results Test and Schema Markup Validator
2. Fix errors first, then warnings that affect eligibility
3. Check GSC Enhancements reports after deploy
4. Crawl site for schema coverage

## Decision rules and checks
- Rich Results Test + Schema.org validator
- Check GSC enhancements
- Fix warnings that block eligibility

## Edge cases and failure handling
- Valid but no rich result -> eligibility/quality, not syntax

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Validation report. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Valid but no rich result
- Action: eligibility/quality, not syntax
- Output: Validation report.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
