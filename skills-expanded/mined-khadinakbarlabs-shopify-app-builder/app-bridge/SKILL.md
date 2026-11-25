---
name: app-bridge
description: "Implement App Bridge integration, navigation, save state, and authenticated embedded-app requests."
---

# Make the app work inside Shopify admin

## Start here

App Bridge connects your app interface to the Shopify admin shell.

First useful outcome: Show one embedded page with a working save/discard flow.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inspect the current template's AppProvider and script loading; avoid duplicate or incompatible SDK setup.
2. Use the supported App Bridge navigation, save bar and feedback patterns for the installed version.
3. Keep client requests same-origin where possible; authenticate on the server with await authenticate.admin(request) before reading store data.
4. Keep draft edits through navigation, offer discard safely and distinguish persisted changes from optimistic feedback.

## Check it worked

Test inside Shopify admin, direct entry, session expiry, dirty-form navigation and save errors; confirm saved state after reload.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never retrieve or log identity tokens manually to work around a failed server authentication boundary.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/app-bridge-library) before using them.

Example request: "Use app-bridge to help me with this task. Explain each change and verify it before moving on."
