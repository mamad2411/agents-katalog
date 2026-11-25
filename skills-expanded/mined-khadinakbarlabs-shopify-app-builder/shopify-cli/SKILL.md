---
name: shopify-cli
description: "Scaffold, link, run, configure or release Shopify apps using verified Shopify CLI commands."
---

# Set up the app step by step

## Start here

The CLI connects local code with an app in Shopify's Dev Dashboard.

First useful outcome: Run a scaffolded app inside an authorized development store.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inspect existing files and non-secret CLI/Node versions first; read shopify-connections for account setup.
2. For a new app use the current shopify app init flow and template; explain browser sign-in and org/dev-store selection before proceeding.
3. For an existing app inspect app info before config link, which can overwrite local config; preserve a copy and confirm the target.
4. Run shopify app dev and verify installation. Keep backend hosting, Shopify config/extension deployment and App Store submission as separate steps.

## Check it worked

Confirm the correct org/app/dev store and one working embedded page; run installed help before version-specific flags.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never print app env output or CLI credential files. app deploy does not host your application server.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/shopify-cli) before using them.

Example request: "Use shopify-cli to help me with this task. Explain each change and verify it before moving on."
