---
name: wp-divi-5-woocommerce-compatibility-audit
description: Audits a Divi 5 and WooCommerce 10 storefront before launch or after updates across product templates, catalog queries, cart, checkout, gateways, shipping, taxes, extensions, caching, responsive behavior, accessibility, and frontend parity.
---

# wp-divi-5-woocommerce-compatibility-audit

Use this skill before launch, before a production update, after a compatibility incident, or after material template and checkout changes.

## Required Inputs

- Exact software and infrastructure versions.
- Active plugins, child theme, gateway, shipping, tax, cache, and commerce extensions.
- Current backups, staging environment, rollback method, and maintenance window.
- Critical products, catalog paths, cart states, checkout configurations, and customer modes.
- Known prior incidents and existing baselines.
- Approved test payment and order cleanup procedures.

## Core Principles

- Audit the intersection, not products in isolation.
- Use representative product and customer states.
- Separate Visual Builder evidence from frontend evidence.
- Include success, failure, empty, and edge states.
- Verify personalized cache exclusions.
- Preserve order, stock, and payment integrity.
- Record reproducible evidence.

## Workflow

Use [`workflows/audit-divi-woocommerce-site-workflow.md`](workflows/audit-divi-woocommerce-site-workflow.md).

## Resource

Use [`resources/compatibility-test-matrix.md`](resources/compatibility-test-matrix.md).

## Completion Evidence

Record versions, matrix coverage, defects, severity, reproduction steps, screenshots or logs, cache state, staged order evidence, rollback readiness, retest results, accepted risks, and launch/update decision.
