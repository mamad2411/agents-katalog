---
name: ux-modern-app-feel
description: "Polish a Shopify app's task flow, responsive feedback, defaults and interaction density."
---

# Make the app feel calm and responsive

## Start here

A modern app feels predictable and fast, not overloaded with animation.

First useful outcome: Remove one unnecessary setup step and improve task feedback.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Measure the main task's friction and preserve familiar Shopify navigation.
2. Prefer useful defaults, progressive settings and clear status over extra dashboards.
3. Use optimistic feedback only when rollback is reliable; preserve keyboard behavior and reduced motion.
4. Improve one flow at a time using the actual installed design system.

## Check it worked

Test saved versus unsaved state, slow responses, keyboard and narrow screens.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not trade truthful status or accessibility for visual polish.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/app-home) before using them.

Example request: "Use ux-modern-app-feel to help me with this task. Explain each change and verify it before moving on."
