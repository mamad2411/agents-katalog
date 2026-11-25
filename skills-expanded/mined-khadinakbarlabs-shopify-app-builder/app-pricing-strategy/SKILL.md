---
name: app-pricing-strategy
description: "Design Shopify app plans, value metrics, trials, and transparent pricing from research."
---

# Choose a price merchants can understand

## Start here

A value metric is the measurable benefit or usage that a plan is priced around.

First useful outcome: Draft one simple plan structure with explicit assumptions.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Estimate the value of the solved task and marginal hosting/support costs.
2. Use current competitor observations from app-market-research; do not infer revenue from ratings.
3. Compare free trial, tiered and usage-based options with a transparent cap and cancellation story.
4. Hand the approved plan to app-billing; keep price experiments separate from live charges.

## Check it worked

State currency, assumptions, gross-margin risks and how a merchant sees/approves every charge.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not hard-code competitor prices from retained reference tables or imply guaranteed revenue.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/launch/billing) before using them.

Example request: "Use app-pricing-strategy to help me with this task. Explain each change and verify it before moving on."
