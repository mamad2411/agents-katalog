---
name: ux-polaris-antipatterns
description: "Review Shopify app UI for task-blocking layout, forms, component misuse and accessibility problems."
---

# Fix confusing UI with focused changes

## Start here

An anti-pattern is an interaction that repeatedly creates avoidable friction.

First useful outcome: Find the three highest-impact issues in a real merchant journey.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Inspect the installed Polaris generation; distinguish existing React code from current web components.
2. Prioritize blocked tasks, unsaved-data loss, misleading status and inaccessible controls before cosmetic preferences.
3. Propose minimal fixes with correct component APIs, contextual help and clear primary actions.
4. Re-test the same journey and avoid a whole-design-system rewrite without need.

## Check it worked

Tie every issue to reproduction, merchant impact and a verified corrected state.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Do not apply old component rename tables blindly to a newer component generation.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/api/app-home) before using them.

Example request: "Use ux-polaris-antipatterns to help me with this task. Explain each change and verify it before moving on."
