---
name: shopify-functions
description: "Build and test Shopify Functions after checking extension target, input schema and store eligibility."
---

# Customize commerce logic with Functions

## Start here

Functions are Shopify-run logic, with constrained inputs and execution limits.

First useful outcome: Generate one supported Function and test a synthetic input locally.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Confirm function target, merchant plan and distribution eligibility using current docs.
2. Use the project's CLI generator, current target schema and language/runtime rather than guessing payload fields.
3. Implement deterministic bounded logic; treat absent/invalid data safely and do not assume network access.
4. Generate types, run/build with version-supported CLI commands, then test in an authorized dev store.

## Check it worked

Test no-op, valid case, boundaries, malformed input and applicable execution limits before release.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

A local build does not prove the Function is enabled or compatible on a merchant's store.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/functions) before using them.

Example request: "Use shopify-functions to help me with this task. Explain each change and verify it before moving on."
