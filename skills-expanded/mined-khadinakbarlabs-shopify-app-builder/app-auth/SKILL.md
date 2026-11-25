---
name: app-auth
description: "Implement or debug Shopify app installation, server-side authentication, sessions, and authorization."
---

# Install and authenticate an app safely

## Start here

Authentication proves who is calling; authorization limits what that caller can do.

First useful outcome: Get a clean development-store install and one authenticated read working.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inspect the installed Shopify framework and use its supported authentication flow; do not hand-roll OAuth or token verification.
2. Authenticate every protected loader/action before store access; for compatible React Router projects use await authenticate.admin(request).
3. Validate shop identity, bind stored sessions and data to that shop, minimize scopes and keep secrets in the application's approved server-side configuration.
4. Cover install, expiry, uninstall/reinstall, revoked permissions and background access; separate Admin, Storefront and Customer Account auth.

## Check it worked

Test forged requests, expired sessions and cross-shop data access; verify install and reinstall in the authorized dev store. Customer Account code must use context.customerAccount.query where that integration applies.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never inspect CLI credential caches, dump sessions, decode a JWT without verification, or ask for tokens in chat.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/authentication-authorization) before using them.

Example request: "Use app-auth to help me with this task. Explain each change and verify it before moving on."
