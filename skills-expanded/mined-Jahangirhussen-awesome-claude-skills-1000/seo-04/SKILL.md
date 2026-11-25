---
name: seo-04
description: 04. On-Page SEO (SEO). Use when the request involves: on-page seo, title tag, meta description, h1, headings, url slug, internal links, content optimization, ctr, entity optimization. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 04. On-Page SEO

ID: 04 | Level: parent | Parent: SEO Master

## Purpose
Page-level relevance and click appeal.

## When to use
Triggers: on-page seo, title tag, meta description, h1, headings, url slug, internal links, content optimization, ctr, entity optimization

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, off page seo, content seo, local seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog (titles/meta/H1), Google Search Console, SERP checks, SEO plugin or CMS fields, a text diff tool.

## Core workflow
1. Crawl titles, meta, H1, canonical, word count by template
2. Compare against top SERP intent for each target keyword
3. Fix patterns per template first, then individual pages

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Duplicate titles by template -> add variable pattern with unique attribute
- Keyword stuffing -> rewrite for intent and clarity

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
On-page fix list per template and per key page. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Duplicate titles by template
- Action: add variable pattern with unique attribute
- Output: On-page fix list per template and per key page.

## Children
- [Title tags](title-tags/SKILL.md)
- [Meta descriptions](meta-descriptions/SKILL.md)
- [Headings](headings/SKILL.md)
- [URL optimization](url-optimization/SKILL.md)
- [Internal linking](internal-linking/SKILL.md)
- [On-page content optimization](content-optimization/SKILL.md)
- [Entity optimization](entity-optimization/SKILL.md)

## Merged from (read for deep method)
- `../_source/seo-onpage/SKILL.md`

## Related installed skills (kept in place; invoke only if needed)
- `internal-link-builder`

## External sources merged (deep method)
- `../_source/aaron__on-page-seo-auditor/SKILL.md`
- `../_source/armaneker__seo-optimizer/SKILL.md`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
