---
name: shopify-app-store-ads
description: "Research or plan Shopify App Store advertising with current eligibility, measurement and spending approval."
---

# Plan ads after proving the product

## Start here

Paid acquisition is an experiment with a budget, not proof of demand.

First useful outcome: Review listing conversion and activation before drafting an ad experiment.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Verify current advertising eligibility and terms with the relevant dashboard/docs.
2. Define target query, value proposition, landing listing and activation measurement.
3. Recommend a bounded experiment with currency, maximum spend and stop criterion; require explicit authorization before enabling it.
4. Evaluate observed impressions, clicks, installs and retained activation without guaranteeing results.

## Check it worked

Report actual spend and conversion evidence separately from the plan; pause if tracking is missing.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never enable a campaign or increase a budget from a general growth request.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://help.shopify.com/en/partners) before using them.

Example request: "Use shopify-app-store-ads to help me with this task. Explain each change and verify it before moving on."
