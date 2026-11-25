---
name: seo-14
description: 14. POS SEO (SEO). Use when the request involves: pos seo, point of sale, restaurant pos, grocery pos, pharmacy pos, retail pos, multi-branch pos, pos hardware. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 14. POS SEO

ID: 14 | Level: parent | Parent: SEO Master

## Purpose
Use 12-saas-seo children with POS matrix: industry x feature x hardware x comparison.

## When to use
Triggers: pos seo, point of sale, restaurant pos, grocery pos, pharmacy pos, retail pos, multi-branch pos, pos hardware

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Keyword tools by industry, GSC, GBP for local variants, competitor pages, hardware spec sheets.

## Core workflow
1. Create industry pages: grocery, restaurant, pharmacy, fashion, electronics, furniture
2. Create feature, hardware, pricing, multi-branch, integration pages
3. Add comparison/alternative pages
4. Add local variants where relevant (see local SEO)

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Hardware and software mixed -> separate pages with clear intent
- Pricing hidden -> add clear pricing page

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
POS page matrix: industry x feature. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Hardware and software mixed
- Action: separate pages with clear intent
- Output: POS page matrix: industry x feature.

## Topics handled here (no separate child)
- Industries: grocery, restaurant, pharmacy, fashion, electronics, furniture - one page each
- Hardware pages + compatibility
- Multi-branch + pricing pages indexable and clear
- Local variants: see 07-local-seo

## Related installed skills (kept in place; invoke only if needed)
- `competitor-alternatives`
- `programmatic-seo`
- `local-seo-manager`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
