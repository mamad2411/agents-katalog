---
name: ux-empty-error-states
description: "Design Shopify app loading, empty, permission, error, retry and partial-success states."
---

# Help merchants recover when things go wrong

## Start here

An empty state means no relevant data; an error means the task failed.

First useful outcome: Implement both an empty result and an actual failure for the primary screen.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. List first-use, no-results, disconnected, denied, throttled, partial-success and fatal states.
2. Explain what happened, what remains saved and the safest next action without exposing internals.
3. Make retries bounded and idempotent; preserve typed work and offer support context with a non-secret reference.
4. Use accessible status announcements and meaningful inline field errors.

## Check it worked

Simulate each state and ensure a failed request never becomes fake empty success.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not tell a merchant to reinstall or contact support when an actionable recovery exists.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/app-home) before using them.

Example request: "Use ux-empty-error-states to help me with this task. Explain each change and verify it before moving on."
