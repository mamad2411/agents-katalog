---
name: liquid-themes
description: "Implement Shopify Liquid, theme app extensions, blocks and embeds with safe preview and removal."
---

# Add theme features without breaking a store

## Start here

A theme app extension adds storefront UI without editing unrelated merchant theme files.

First useful outcome: Preview one app block in an authorized development theme.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Confirm theme feature versus embedded app; inspect theme compatibility and current extension schema.
2. Use supported app blocks/embeds and validated settings; escape untrusted output and minimize storefront script cost.
3. Explain activation in the theme editor and provide sensible defaults, accessible markup and an empty state.
4. Preview before publication and preserve existing theme customization; document clean disable/uninstall behavior.

## Check it worked

Test activation, mobile layout, missing data, multiple blocks and removal without leftover broken markup.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never publish a live theme or inject irreversible code just to test a feature.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/build/online-store/theme-app-extensions) before using them.

Example request: "Use liquid-themes to help me with this task. Explain each change and verify it before moving on."
