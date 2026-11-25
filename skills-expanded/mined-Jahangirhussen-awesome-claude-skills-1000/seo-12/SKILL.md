---
name: seo-12
description: 12. SaaS SEO (SEO). Use when the request involves: saas seo, landing page, feature page, use case page, integration page, comparison page, alternative page, free tool, docs seo, product-led seo. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# 12. SaaS SEO

ID: 12 | Level: parent | Parent: SEO Master

## Purpose
SaaS acquisition via bottom-funnel and product-led pages. ERP (13) and POS (14) reuse these children.

## When to use
Triggers: saas seo, landing page, feature page, use case page, integration page, comparison page, alternative page, free tool, docs seo, product-led seo

## When NOT to use
- The request belongs to another SEO category (see `../ROUTER.md`): e.g. core seo, google seo, technical seo, on page seo, off page seo, content seo.
- A more specific child skill already covers it: open that child instead of repeating its work.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Ahrefs/Semrush competitor tools, GSC, analytics funnels, CMS, screenshot tools, schema validator.

## Core workflow
1. Map product to jobs-to-be-done and buyer stages
2. Prioritize bottom-funnel pages (alternatives, comparisons, integrations) then solutions/features
3. Ensure fast, clear landing pages with CTA
4. Build docs, templates, free tools for product-led traffic

## Decision rules
- Use evidence (crawl, GSC, rendered HTML, validators), not assumptions.
- Fix the highest-impact, lowest-risk items first; change only what the task needs.
- If a platform skill (WordPress, WooCommerce, Shopify) applies, its guidance overrides generic advice.

## Edge cases and failure handling
- Blog-only strategy -> add commercial pages
- Feature list copy -> write for outcomes

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
SaaS SEO page map. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Blog-only strategy
- Action: add commercial pages
- Output: SaaS SEO page map.

## Children
- [Landing pages](landing-pages/SKILL.md)
- [Feature pages](feature-pages/SKILL.md)
- [Comparison and alternative pages](comparison-pages/SKILL.md)
- [Integration pages](integration-pages/SKILL.md)
- [Programmatic SaaS pages](programmatic-saas/SKILL.md)

## Topics handled here (no separate child)
- Docs SEO: crawlable, versioned, canonical to latest
- Free tools/templates: one intent each, embeddable value, link to product
- Conversion SEO: clear CTA, social proof, fast pages

## Related installed skills (kept in place; invoke only if needed)
- `competitor-alternatives`
- `programmatic-seo`
- `landing-page-copy`
- `page-cro`
- `free-tool-strategy`

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
