---
name: app-niche-finder
description: "Identify Shopify app niches and prioritize merchant problems using evidence rather than guessed market demand."
---

# Find a merchant problem worth solving

## Start here

A niche is a specific merchant group with a recurring problem.

First useful outcome: Shortlist one merchant segment and one high-friction task.
Ask only for missing information that changes this task. Inspect the existing project and use synthetic data before touching a merchant store. Explain the next action and its expected result in plain language; offer a recommended default with its tradeoff.

## Guided workflow

1. Identify merchant type, repeated workflow, urgency and existing workaround.
2. Use app-market-research for optional competitor/review data; otherwise use public pages and interviews.
3. Separate observed complaints from hypotheses and compare saturation, implementation difficulty and customer access.
4. Pick a small validation experiment before recommending a large build.

## Check it worked

Produce a problem brief with source dates, competitor gaps, uncertainties and a next validation step.
Report what was changed, what was tested, and what still needs account access or live verification. Do not claim production readiness or approval from generated code alone.

## If you get stuck

Sparse reviews or few results do not prove low competition or a profitable market.
Give one safe next step and a redacted error example, not a list of speculative fixes.

## Safety and optional depth

Use only the user's selected project/accounts. Never read credential caches or request secrets in chat; the operator configures the application's approved secret store. Ask before live deployment, store mutations, billing, publication or paid runs unless that exact action is already authorized. No MCP service is required by this plugin.

For concrete examples in an existing project, read only the relevant section of [technical-guide.md](references/technical-guide.md). These retained v1.x examples are version-sensitive, not the default template. Verify SDKs, schema fields, CLI flags and platform rules with [official documentation](https://shopify.dev/docs/apps) before using them.

Example request: "Use app-niche-finder to help me with this task. Explain each change and verify it before moving on."
