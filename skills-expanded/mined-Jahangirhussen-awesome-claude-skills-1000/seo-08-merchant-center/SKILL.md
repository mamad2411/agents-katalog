---
name: seo-08-merchant-center
description: Merchant Center and Shopping (SEO). Use when the request involves: merchant center, google shopping, product feed. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Merchant Center and Shopping

ID: 08.05 | Level: child | Parent: [E-commerce SEO](../SKILL.md)

## Purpose
Merchant Center and Shopping within the seo-master tree: Feed spec and error fixes.

## When to use
Triggers: merchant center, google shopping, product feed

## When NOT to use
- The topic is covered by a sibling skill: `../category-seo`, `../ecommerce-content`, `../faceted-navigation`, `../product-schema`, `../product-seo`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. Create feed with required attributes; match page price/stock
2. Fix disapprovals (images, GTIN, policy)
3. Enable free listings; optimize titles with brand + attributes
4. Monitor diagnostics weekly

## Decision rules and checks
- Feed matches page price/stock
- GTIN/brand/identifiers
- Fix disapprovals

## Edge cases and failure handling
- Feed price differs from site -> schedule sync
- Missing GTIN -> add or mark identifier_exists properly

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Feed spec and error fixes. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Feed price differs from site
- Action: schedule sync
- Output: Feed spec and error fixes.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
