---
name: merchant-pain-prevention
description: "Audit merchant-impact risks, installation friction, destructive actions, data lifecycle and safe recovery."
---

# Protect merchant data and trust

## Start here

A safe app makes the impact of a change visible and offers a recovery path.

First useful outcome: Review the most consequential merchant action before launch.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Map actions that modify catalog, inventory, themes, orders, billing or stored data.
2. Add clear previews, explicit confirmation for meaningful impact, bounded batches and idempotent retries.
3. Keep shops isolated, retain only necessary data, and implement uninstall and applicable privacy cleanup.
4. Design support diagnostics and recovery without exposing customer data or secrets.

## Check it worked

Test interrupted work, duplicate events, wrong-shop requests, uninstall and rollback/recovery.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not collect extra merchant/customer data merely because a scope makes it available.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/launch/protected-customer-data) before using them.

Example request: "Use merchant-pain-prevention to help me with this task. Explain each change and verify it before moving on."
