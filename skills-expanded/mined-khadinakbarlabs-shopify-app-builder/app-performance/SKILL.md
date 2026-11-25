---
name: app-performance
description: "Measure and improve Shopify app latency, frontend loading, API efficiency, and background-job reliability."
---

# Keep the app fast and reliable

## Start here

Performance is how quickly a real merchant can complete a task.

First useful outcome: Measure one slow task before changing it.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Record environment, dataset size, device and baseline user-visible timing.
2. Inspect server/API waits, repeated requests, pagination, bundle and rendering costs; optimize the measured bottleneck.
3. Use appropriate caching without crossing shop boundaries; move long work to durable jobs with bounded retries.
4. Re-measure the same task and test error paths; distinguish local results from production performance.

## Check it worked

Show before/after evidence and check correct data, cache isolation and retry behavior.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not promise Built for Shopify performance approval from a local benchmark.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/performance) before using them.

Example request: "Use app-performance to help me with this task. Explain each change and verify it before moving on."
