---
name: app-validation
description: "Plan merchant interviews and small experiments to validate a Shopify app idea or pivot."
---

# Validate the idea before a large build

## Start here

Validation means testing a business assumption with real evidence.

First useful outcome: Write a problem hypothesis and a low-cost test.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Describe the merchant, recurring task, current workaround and expected measurable improvement.
2. Combine public app-market-research with direct interviews; keep qualitative complaints separate from conversion evidence.
3. Define the riskiest assumption, experiment, success threshold and stop/pivot criterion before running it.
4. Build only the smallest useful prototype after reviewing evidence; preserve negative findings.

## Check it worked

Return evidence, sample limitations, decision and next experiment instead of a fabricated market score.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not treat a survey intention or a competitor review as willingness to pay.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps) before using them.

Example request: "Use app-validation to help me with this task. Explain each change and verify it before moving on."
