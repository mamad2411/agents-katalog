---
name: hydrogen-storefront
description: "Build or maintain Shopify Hydrogen storefronts and customer-account flows; not ordinary embedded app UI."
---

# Build a headless storefront intentionally

## Start here

Headless means the storefront frontend is separate from the Shopify theme.

First useful outcome: Confirm Hydrogen is required before scaffolding a storefront.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inspect the installed Hydrogen framework, Storefront API version and deployment choice.
2. Use framework-managed storefront/customer-account clients; customer-account queries should use context.customerAccount.query.
3. Keep server-only credentials out of browser code; model cart, checkout, localization and caching with explicit boundaries.
4. Implement one real shopping journey before expanding the storefront.

## Check it worked

Test product to cart to checkout, authenticated account access, cache separation, locale and empty/error states.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not add Hydrogen to an embedded app that does not need a separate storefront.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/storefronts/headless/hydrogen) before using them.

Example request: "Use hydrogen-storefront to help me with this task. Explain each change and verify it before moving on."
