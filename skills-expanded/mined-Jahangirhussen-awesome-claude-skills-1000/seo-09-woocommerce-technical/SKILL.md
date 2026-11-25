---
name: seo-09-woocommerce-technical
description: Woo technical (SEO). Use when the request involves: woocommerce sitemap, woo speed, woo permalink. Not for topics owned by sibling SEO skills or other categories; routed by seo-master.
---

# Woo technical

ID: 09.06 | Level: child | Parent: [WooCommerce SEO](../SKILL.md)

## Purpose
Woo technical within the seo-master tree: Technical fix list.

## When to use
Triggers: woocommerce sitemap, woo speed, woo permalink

## When NOT to use
- The topic is covered by a sibling skill: `../attributes`, `../categories`, `../filters`, `../product-schema`, `../products`.
- The task is outside this SEO category; see `ROUTER.md` at the seo-master root.

## Inputs
- Target site/URL(s) or project files, platform (CMS/framework), and goal.
- Data access as available: WooCommerce admin, Yoast/Rank Math, Query Monitor, Screaming Frog, WP-CLI, Rich Results Test.

## Core workflow
1. Noindex cart, checkout, my-account, wishlist, compare
2. Sitemap: products, categories only; exclude tags/attributes if thin
3. Speed: object cache, page cache excluding cart, optimized images, remove unused scripts (wc-cart-fragments where possible)
4. Check canonical and hreflang with multilingual plugins

## Decision rules and checks
- noindex cart/checkout/account
- Sitemap hygiene
- Speed and image sizes

## Edge cases and failure handling
- Cart fragments slowing pages -> restrict to cart pages
- Session cookies breaking cache -> exclude only needed endpoints

## Validation
- Re-fetch or re-crawl changed URLs; confirm the fix is live (status, rendered HTML, canonical, schema validator, GSC URL Inspection as relevant).
- Compare with the baseline recorded before the change; check for regressions on neighbouring templates.

## Output requirements
Technical fix list. Report as a short DONE: what changed, evidence, remaining issues.

## Example
- Input/symptom: Cart fragments slowing pages
- Action: restrict to cart pages
- Output: Technical fix list.

## Dependencies (load only if needed)
- 03-technical-seo

## References
`references/playbook.md`: detailed how-to, common problems and fixes, tools, verify steps. Read when executing.
