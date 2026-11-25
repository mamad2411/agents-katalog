---
name: dev-troubleshooting
description: "Diagnose Shopify CLI, API, auth, webhook, UI, extension, and deployment failures."
---

# Fix one problem without making a mess

## Start here

A reproduction is a reliable way to make the same failure happen again.

First useful outcome: Capture one redacted error and reproduce it safely.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Ask only for the error, where it happens and last known working state; inspect non-secret versions and config.
2. Choose the focused skill for the failing layer and test a specific hypothesis with read-only checks.
3. If fixing is requested, write a regression test, make the smallest change and preserve unrelated edits.
4. Reproduce again and report evidence; use recoverable cache backups only after proving cache involvement.

## Check it worked

State confirmed cause, exact change, regression result and anything not tested live.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never read auth caches, print .env/session tables, uninstall everything, or run guessed CLI subcommands.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/shopify-cli) before using them.

Example request: "Use dev-troubleshooting to help me with this task. Explain each change and verify it before moving on."
