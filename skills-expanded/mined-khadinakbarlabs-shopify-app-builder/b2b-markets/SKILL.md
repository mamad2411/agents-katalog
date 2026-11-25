---
name: b2b-markets
description: "Build or audit Shopify B2B and Markets features after checking store eligibility and API availability."
---

# Support the right B2B and international workflows

## Start here

B2B serves business buyers; Markets manages selling across regions.

First useful outcome: Verify store eligibility and one supported buyer/market flow.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Confirm merchant plan, company/catalog needs, regions and current feature access before choosing APIs.
2. Use current stable-schema company, catalog and contextual pricing data with minimal scopes.
3. Model currency, language, tax and buyer permissions explicitly; avoid leaking one company's pricing to another.
4. Implement the narrow workflow and test unsupported-plan behavior gracefully.

## Check it worked

Test eligible and ineligible shops, buyer isolation, currency and locale switching, and permission failures.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not assume every Shopify store has every B2B/Markets capability.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/b2b) before using them.

Example request: "Use b2b-markets to help me with this task. Explain each change and verify it before moving on."
