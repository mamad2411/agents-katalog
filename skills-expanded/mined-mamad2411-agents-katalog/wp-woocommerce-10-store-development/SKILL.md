---
name: wp-woocommerce-10-store-development
description: Plans and reviews WooCommerce 10.x store customizations using supported hooks, templates, blocks, data objects, and APIs. Use for site-specific product, order, catalog, account, cart, or checkout changes that are not a distributable extension.
---

# WooCommerce 10 Store Development

Use this skill to choose the smallest supported customization surface for a WooCommerce 10.x store.

## Start by identifying

- Installed WooCommerce minor and patch.
- WordPress, PHP, theme, block theme, and checkout type.
- Whether the change is site-specific or should become a distributable extension.
- Data touched: products, orders, customers, coupons, stock, taxes, shipping, payments, or sessions.
- Frontend surface: classic template, block, Cart/Checkout block, Store API, admin, REST integration, email, or CLI.
- Production constraints and rollback path.

## Decision order

1. Prefer a documented setting or existing extension when it satisfies the requirement.
2. Prefer hooks and filters for small server-side behavior changes.
3. Prefer blocks, block extensibility, or supported frontend APIs for block-based surfaces.
4. Prefer theme or child-theme overrides only for presentation and only after checking template-version maintenance cost.
5. Use a custom WordPress plugin for durable site functionality.
6. Use `wp-woocommerce-10-extension-development` for distributable extensions, gateways, shipping methods, or reusable integrations.
7. Never edit WooCommerce core files.

Read:

- `resources/customization-decision-matrix.md`
- `resources/api-selection-matrix.md`
- `workflows/plan-store-change-workflow.md`

## Implementation baseline

- Bootstrap only after WooCommerce is available.
- Prefix or namespace custom code.
- Use WooCommerce CRUD and query APIs.
- Keep order access HPOS-compatible.
- Use capability checks, validation, sanitization, prepared queries, nonces where appropriate, and late escaping.
- Keep customer-facing cart/checkout logic compatible with Store API and block checkout when those surfaces are active.
- Add tests for success, rejection, retries, duplicate requests, and degraded dependencies.
- Log operationally useful events without secrets or unnecessary PII.
- Include built assets in deployment artifacts.

## Output expected from the agent

- Chosen customization surface and why.
- Version and compatibility assumptions.
- Data and transaction risk.
- Files and hooks/APIs affected.
- Test matrix.
- Deployment and rollback steps.
- Explicit out-of-scope items.
