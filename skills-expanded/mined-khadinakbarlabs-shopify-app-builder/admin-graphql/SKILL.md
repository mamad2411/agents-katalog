---
name: admin-graphql
description: "Implement or debug Shopify Admin GraphQL operations, pagination, throttling, and mutations."
---

# Read and update store data safely

## Start here

GraphQL asks Shopify for specific data; a mutation changes it.

First useful outcome: List products with pagination before adding any write operation.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inspect the app's API version and required scopes; start with a read-only query and synthetic fixtures.
2. Use variables and server-side authenticated clients; handle transport errors, GraphQL errors and mutation userErrors separately.
3. Paginate with cursors, budget query cost, retry throttling with bounded backoff and preserve per-shop isolation.
4. For writes, preview affected records, obtain scope/operation approval, and design idempotency plus recovery.

## Check it worked

Test empty pages, multiple pages, access denial, throttling and partial mutation failure; HTTP 200 alone is not success.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

If a field fails, check that exact stable-version schema before expanding scopes.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/admin-graphql) before using them.

Example request: "Use admin-graphql to help me with this task. Explain each change and verify it before moving on."
