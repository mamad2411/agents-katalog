---
name: storefront-api
description: "Implement Shopify Storefront API product, collection, cart and checkout flows."
---

# Build public shopping experiences safely

## Start here

The Storefront API serves shopping experiences; it is not the Admin API.

First useful outcome: Read products and complete a cart flow using supported API fields.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Confirm public versus server-only access, API version, headless requirements and approved configuration.
2. Use variables, cursor pagination and framework clients; keep private configuration out of browser bundles.
3. Implement contextual pricing/currency, cart errors, quantity boundaries and checkout handoff.
4. Handle missing products, unavailable variants, throttling and stale carts without hiding errors.

## Check it worked

Test empty catalogs, pagination, unavailable items, locale/currency and checkout transition on a dev storefront.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not use an Admin token in storefront/browser code.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/storefront) before using them.

Example request: "Use storefront-api to help me with this task. Explain each change and verify it before moving on."
