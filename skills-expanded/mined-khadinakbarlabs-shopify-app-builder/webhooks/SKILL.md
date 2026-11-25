---
name: webhooks
description: "Implement and test authenticated Shopify webhooks, durable processing, retries and privacy lifecycle handlers."
---

# Handle Shopify events reliably

## Start here

A webhook is Shopify notifying your app about an event.

First useful outcome: Receive a valid event and reject an invalid signature in tests.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Check current topic, API version and config; use the framework's supported webhook authentication over custom verification where available.
2. For custom verification, authenticate the raw body with constant-time HMAC comparison before trusting parsed content; never log secret/payload data.
3. Durably enqueue accepted work before acknowledgement, isolate shops, deduplicate event IDs and bound retries.
4. Implement uninstall and applicable compliance topics with real export/deletion behavior, retention policy and tests.

## Check it worked

Test invalid signature, altered body, duplicates, delayed/out-of-order delivery, queue failure and cleanup; a CLI sample alone may not verify real subscription delivery.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not acknowledge work that can be lost immediately after response or return success for a failed cleanup.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/webhooks) before using them.

Example request: "Use webhooks to help me with this task. Explain each change and verify it before moving on."
