---
name: polaris-ui
description: "Create Shopify embedded app pages with current Polaris patterns or maintain existing Polaris React UI."
---

# Build a familiar Shopify interface

## Start here

Polaris is Shopify's design system; match the actual installed component generation.

First useful outcome: Build a page with one primary action and complete loading/error states.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. For a new app follow current App Home/Polaris web components and scaffold wiring; inspect an existing app before any migration.
2. Start with the merchant task, page hierarchy, meaningful fields, default state and clear help text.
3. Use supported component props and tokens; keep validation, save/discard and status feedback understandable.
4. Test keyboard, narrow screens, translated/long text and empty/error states before adding decoration.

## Check it worked

Verify the real embedded page and persisted action; do not mix React-only props with web components.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Retained React examples are for compatible existing projects, not the default for a new app.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/app-home) before using them.

Example request: "Use polaris-ui to help me with this task. Explain each change and verify it before moving on."
