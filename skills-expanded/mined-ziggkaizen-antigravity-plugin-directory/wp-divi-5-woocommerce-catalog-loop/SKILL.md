---
name: wp-divi-5-woocommerce-catalog-loop
description: Builds and reviews Divi 5 WooCommerce product grids, shop and taxonomy templates, related products, upsells, cross-sells, and Loop Builder output with explicit query context, pagination, visibility, empty states, and performance limits.
---

# wp-divi-5-woocommerce-catalog-loop

Use this skill when a page or template repeats products or represents a WooCommerce archive.

## Required Inputs

- Intended source: current archive, category, featured, sale, latest, best-selling, top-rated, related, upsell, cross-sell, or custom product set.
- Required ordering, count, columns, pagination, offset, and filters.
- Catalog visibility and stock rules.
- Product-card information and actions.
- Representative full and empty result sets.
- Performance and cache constraints.

## Core Principles

- Choose the simplest module that preserves the intended WooCommerce query.
- Keep archive-aware templates tied to the current archive.
- Use Loop Builder only when the fixed Woo Products structure is insufficient.
- Preserve loop-product context in every repeated item.
- Keep pagination and no-results behavior explicit.
- Bound product counts and duplicate queries.
- Verify logged-out frontend output with real catalog states.

## Workflow

Use [`workflows/build-divi-woocommerce-catalog-workflow.md`](workflows/build-divi-woocommerce-catalog-workflow.md).

## Resource

Use [`resources/catalog-query-context-matrix.md`](resources/catalog-query-context-matrix.md).

## Completion Evidence

Record source context, module choice, query controls, card fields, visibility behavior, pagination, no-results state, product states tested, breakpoints, query-heavy sections, and frontend URLs.
