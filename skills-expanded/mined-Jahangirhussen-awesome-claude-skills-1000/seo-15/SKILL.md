---
name: seo-15
description: 15. Programmatic SEO (SEO). Use when the request involves: programmatic seo, pages at scale, template pages, location pages, database pages, directory. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 15. Programmatic SEO

ID: 15 | Level: parent | Parent: SEO Master

## Purpose
Scalable templated pages with unique value.

## When to use
Triggers: programmatic seo, pages at scale, template pages, location pages, database pages, directory

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Dataset or database, template engine, Screaming Frog, GSC (indexing), sitemap generator, QA sampling script.

## Core workflow
1. Validate demand for the pattern (head term + modifier) before building
2. Ensure each page has unique value (data, insights, local info)
3. Build templates, internal links, sitemap segments; launch small batch
4. Monitor indexing and traffic; prune losers

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Mass thin pages -> manual-action risk; raise value or reduce
- Crawled not indexed -> improve uniqueness and links

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Programmatic plan: pattern, data source, template, QA gate. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Mass thin pages
- Action: manual-action risk; raise value or reduce
- Output: Programmatic plan: pattern, data source, template, QA gate.

## Children
- [Template pages](template-pages/SKILL.md)
- [Database-driven pages](database-pages/SKILL.md)
- [Location pages](location-pages/SKILL.md)
- [Programmatic comparisons](comparison-pages/SKILL.md)
- [Programmatic internal linking](programmatic-internal-linking/SKILL.md)

## Merged from (read for deep method)
- `../_source/programmatic-seo/SKILL.md`

## External sources merged (deep method)
- `../_source/borghei__programmatic-seo/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
