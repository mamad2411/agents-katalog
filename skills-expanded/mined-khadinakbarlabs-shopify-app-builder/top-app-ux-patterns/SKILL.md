---
name: top-app-ux-patterns
description: "Evaluate merchant workflow patterns from Shopify apps and adapt evidence-backed UX ideas."
---

# Learn useful patterns without cloning apps

## Start here

A pattern is a reusable interaction, not permission to copy a competitor's brand or assets.

First useful outcome: Compare the same merchant task across a few relevant apps.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Choose the user task and current public examples or authorized trials.
2. Record observable interactions separately from inferred conversion or revenue claims.
3. Adapt useful hierarchy, feedback, setup and recovery patterns to installed Polaris components.
4. Test your own implementation with novice and experienced merchant journeys.

## Check it worked

Explain why each chosen pattern improves a specific task; verify it works in this app.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Top-rated does not prove a UX pattern causes growth; do not clone proprietary screens/assets.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/app-home) before using them.

Example request: "Use top-app-ux-patterns to help me with this task. Explain each change and verify it before moving on."
