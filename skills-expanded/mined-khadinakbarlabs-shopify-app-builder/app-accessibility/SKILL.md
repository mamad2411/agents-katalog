---
name: app-accessibility
description: "Audit or implement keyboard, screen-reader, contrast, focus, and accessible Shopify app interactions."
---

# Make the app usable for everyone

## Start here

Accessibility lets merchants use the app without a mouse or perfect vision.

First useful outcome: Complete the primary task using only the keyboard.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Identify the primary task, meaningful labels, headings, live feedback and error associations.
2. Use the installed Polaris component semantics; provide accessible names for icon-only actions and clear field help.
3. Test focus movement in dialogs, validation errors and route changes; honor reduced motion and zoom.
4. Combine automated checks with manual keyboard and screen-reader sampling, prioritizing blocked tasks.

## Check it worked

Record tested viewport, keyboard path and actual failures; test loading, empty, error and success states.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

An automated zero-issue score is not full accessibility proof.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/app-home) before using them.

Example request: "Use app-accessibility to help me with this task. Explain each change and verify it before moving on."
