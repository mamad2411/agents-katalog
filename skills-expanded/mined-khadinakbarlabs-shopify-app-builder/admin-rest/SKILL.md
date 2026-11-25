---
name: admin-rest
description: "Maintain legacy Shopify REST integrations or migrate them to Admin GraphQL; not for new apps."
---

# Migrate an existing REST integration

## Start here

REST is the older API style; new work should prefer Admin GraphQL.

First useful outcome: Move an existing product reader to GraphQL without changing its result contract.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inventory the current REST calls, API versions, scopes and consumer behavior.
2. Map each operation to a current GraphQL equivalent, including pagination, money and identifier shapes.
3. Test old and new outputs with synthetic fixtures; switch one operation at a time.
4. Retain a rollback path and identify unsupported equivalents rather than inventing fields.

## Check it worked

Compare records, pagination boundaries, failure handling and throttle behavior before cutover.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not start a new public app with REST because a retained example is shorter.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/admin-rest) before using them.

Example request: "Use admin-rest to help me with this task. Explain each change and verify it before moving on."
