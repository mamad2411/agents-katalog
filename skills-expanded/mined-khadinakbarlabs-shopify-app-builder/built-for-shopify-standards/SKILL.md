---
name: built-for-shopify-standards
description: "Audit a Shopify app against current Built for Shopify criteria, separate from App Store approval."
---

# Prepare a rigorous quality review

## Start here

Built for Shopify is a reviewed quality designation, not something the plugin can award.

First useful outcome: Create a blocker-first evidence checklist for the current app.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Read current program criteria and record the date; inspect install, embedded UX and core task paths.
2. Review accessibility, performance, billing clarity, support, privacy and uninstall behavior.
3. Map each criterion to observed evidence, a failure or an untested condition; avoid fixed obsolete thresholds.
4. Recommend scoped remediation, then re-run the affected journeys.

## Check it worked

Deliver criterion, evidence, priority, owner and retest steps; distinguish App Store readiness from designation eligibility.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Never state that a badge or approval is guaranteed.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps/launch/built-for-shopify) before using them.

Example request: "Use built-for-shopify-standards to help me with this task. Explain each change and verify it before moving on."
