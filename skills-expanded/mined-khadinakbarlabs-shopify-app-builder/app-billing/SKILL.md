---
name: app-billing
description: "Design or implement Shopify app subscriptions, entitlement checks, trials, and billing lifecycle behavior."
---

# Make pricing and billing understandable

## Start here

An entitlement is what a merchant can use after their plan is confirmed.

First useful outcome: Build a clearly labelled test-mode upgrade flow before requesting any live charge.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Confirm current Shopify App Pricing versus Billing API eligibility and choose the supported path for this distribution.
2. Explain price, currency, trial, usage limit and cancellation before merchant approval; never silently start a charge.
3. Enforce entitlements server-side; model pending, approved, cancelled, expired and failed states instead of trusting a UI redirect.
4. Test development-store billing using the supported test flow; reconcile plan changes using the current billing mechanism rather than assuming legacy webhooks exist.

## Check it worked

Verify decline, cancellation, return from approval, trial end, duplicate requests, uninstall and reinstall without creating a live charge.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not use a real paying store just to bypass test-mode failures. Stop and check current billing docs.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/launch/billing) before using them.

Example request: "Use app-billing to help me with this task. Explain each change and verify it before moving on."
