---
name: seo-08-product-seo
description: Product SEO (SEO). Use when the request involves: product page seo, product title, product description. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Product SEO

ID: 08.01 | Level: child | Parent: [E-commerce SEO](../SKILL.md)

## Purpose
Product SEO within the seo-master tree: Product template spec.

## When to use
Triggers: product page seo, product title, product description

## When NOT to use
- The topic is covered by a sibling skill: `../category-seo`, `../ecommerce-content`, `../faceted-navigation`, `../merchant-center`, `../product-schema`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: Screaming Frog, Google Search Console, Merchant Center, Rich Results Test, platform admin, feed validator.

## Core workflow
1. Unique title: product name + key attribute + brand
2. Unique description with benefits, specs, FAQs; avoid supplier copy
3. High-quality images with alt text; reviews on page
4. Product + Offer schema; breadcrumbs; related products links

## Decision rules and checks
- Unique title/description
- Primary image + alt
- Reviews + specs + FAQ
- Product schema

## Edge cases and failure handling
- Variants as separate thin URLs -> canonicalize to parent or make unique
- Out-of-stock -> keep page, show alternatives; 301 only if permanently gone

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Product template spec. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Variants as separate thin URLs
- Action: canonicalize to parent or make unique
- Output: Product template spec.

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
