---
name: seo-27
description: 27. Schema / Structured Data (SEO). Use when the request involves: schema, json-ld, structured data, rich results, schema validation. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 27. Schema / Structured Data

ID: 27 | Level: parent | Parent: SEO Master

## Purpose
JSON-LD for rich results and entity clarity.

## When to use
Triggers: schema, json-ld, structured data, rich results, schema validation

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Rich Results Test, Schema Markup Validator (validator.schema.org), GSC Enhancements, JSON-LD generator or code.

## Core workflow
1. Pick types matching visible content
2. Write JSON-LD in one source of truth
3. Validate in Rich Results Test and Schema.org validator
4. Monitor GSC Enhancements

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Markup for hidden content -> remove
- Duplicate sources -> keep one

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Schema plan per template. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Markup for hidden content
- Action: remove
- Output: Schema plan per template.

## Children
- [Organization](organization/SKILL.md)
- [LocalBusiness](local-business/SKILL.md)
- [Product and Offer](product/SKILL.md)
- [Article / BlogPosting](article/SKILL.md)
- [FAQPage](faq/SKILL.md)
- [BreadcrumbList](breadcrumb/SKILL.md)
- [Review and AggregateRating](review/SKILL.md)
- [Schema validation](schema-validation/SKILL.md)

## Topics handled here (no separate child)
- Rules: JSON-LD, mark up visible content only, no fake ratings, one source per page

## Merged from (read for deep method)
- `../_source/schema-markup/SKILL.md`

## External sources merged (deep method)
- `../_source/borghei__schema-markup/SKILL.md`
- `../_source/aaron__schema-markup-generator/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
