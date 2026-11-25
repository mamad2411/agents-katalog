---
name: ux-onboarding
description: "Design Shopify app first-run setup, sample data, activation and contextual help."
---

# Guide a merchant to their first useful result

## Start here

Activation is the first time a merchant gets the benefit they installed for.

First useful outcome: Define a short path from install to one useful outcome.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Identify the first-value task and only the permissions/settings needed for it.
2. Offer sensible defaults, a reversible sample or preview and a clear next action.
3. Explain optional integrations and pricing separately; save progress through retries and navigation.
4. Test first install, returning merchant, reinstall, missing permission and skipped setup.

## Check it worked

Measure observed task completion and show unfinished steps without fabricated progress.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not force advanced setup, account creation or paid research when the basic task can work without it.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/app-home) before using them.

Example request: "Use ux-onboarding to help me with this task. Explain each change and verify it before moving on."
