---
name: wp-woocommerce-10-checkout-and-api
description: Designs and tests WooCommerce 10.x cart, checkout, Store API, REST API, payment, shipping, tax, coupon, and order-processing changes. Use when customer-facing commerce flows or external API integrations are affected.
---

# WooCommerce 10 Checkout and APIs

Use this skill for transaction-sensitive customer and integration paths.

## Identify the surface

- Cart and Checkout blocks versus legacy shortcode templates.
- Store API versus authenticated WC REST API.
- Guest versus authenticated customer.
- Payment gateway, shipping method, tax engine, coupons, subscriptions, or other extensions.
- Browser, server, webhook, CLI, or MCP caller.
- Session, nonce, authentication, and permission model.

Read:

- `resources/checkout-test-matrix.md`
- `resources/store-api-rest-api-matrix.md`
- `workflows/test-checkout-change-workflow.md`

## Rules

- Do not assume classic checkout hooks execute in Cart/Checkout blocks.
- Use documented block extensibility for block checkout.
- Keep WC REST API keys server-side and least-privileged.
- Do not add privileged data to the public Store API.
- Use sandbox gateways and safe email handling in development.
- Test duplicate submissions, retries, external timeouts, webhook delay, and idempotency.
- Verify totals, taxes, shipping, coupons, stock, payment status, order notes, and emails.
- Avoid real customer data in fixtures.
- Redact secrets and PII from logs and test output.

## 10.9-specific awareness

WooCommerce 10.9 changed when new checkout sessions persist draft orders and reduced repeated saves/lookups. Do not build logic that depends on an early persisted draft order without verifying current Store API behavior.

## Output expected from the agent

- API/checkout surface classification.
- Security and data boundary.
- Supported extension point.
- Test matrix with expected state transitions.
- Observability, deployment, and rollback plan.
