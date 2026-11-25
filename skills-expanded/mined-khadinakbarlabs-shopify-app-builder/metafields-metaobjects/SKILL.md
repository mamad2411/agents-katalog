---
name: metafields-metaobjects
description: "Design and implement Shopify metafield and metaobject definitions, validation and migrations."
---

# Store custom data with a clear schema

## Start here

Metafields attach structured fields to resources; metaobjects represent reusable structured records.

First useful outcome: Define one custom field with its owner, type and validation.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Identify the resource, ownership/access model and merchant-facing edit experience.
2. Check current definition types, capabilities and access rules before choosing namespace/key and validation.
3. Use authenticated GraphQL with explicit variables, handle userErrors and migrate existing values carefully.
4. Make reads resilient to missing or old data and define removal/retention behavior.

## Check it worked

Test invalid values, absent definitions, permission failures, migrations and storefront visibility.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not put secrets or private customer data in publicly exposed custom-data fields.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/custom-data) before using them.

Example request: "Use metafields-metaobjects to help me with this task. Explain each change and verify it before moving on."
