---
name: visual-regression-testing
description: "Catch unintended UI change with screenshot tests: deterministic fixtures, stable rendering, thresholds, baseline management and triage of real diffs."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - visual regression testing
  - playwright screenshot test
  - flaky screenshot tests
  - storybook visual test baseline
  - percy chromatic setup
aliases:
  - vrt
keywords:
  - visual-regression
  - screenshot
  - percy
  - chromatic
  - playwright
  - baseline
mcp_servers:
  - playwright
  - github
source: custom
enabled: true
---

# Visual Regression Testing

## Purpose

Catch unintended UI change with screenshot tests: deterministic fixtures, stable rendering, thresholds, baseline management and triage of real diffs.

## When to Use

- A design system or marketing surface must not shift without review.
- CSS changes silently break layouts at other breakpoints.
- Screenshot tests exist but are so flaky nobody reads them.

## When NOT to Use

- The UI is expected to change on every commit.
- The product has no stable rendering environment for tests.
- The regression is functional, which a component test catches better.

## Capabilities

- Freeze animations, fonts and data so renders are deterministic.
- Capture at defined breakpoints and browsers, not ad hoc.
- Set a perceptual threshold that ignores antialiasing noise.
- Review diffs as design changes, with an owner and an approve step.
- Prune and re-baseline deliberately instead of accepting everything.

## Inputs

- The pages or components worth guarding, and their states.
- The fixed viewport set and browser matrix.
- A place to store baselines with review history.

## Workflow

1. Start from stable fixtures: seeded data, local fonts, animations disabled.
2. Capture one screenshot per meaningful state, not one per page.
3. Run three times on the same commit to prove the test is not flaky before trusting it.
4. Set a threshold just above measured noise, and record the measured noise.
5. Review every diff; approve only changes you can explain.
6. Delete baselines for removed components so the suite does not rot.

## Tools

- playwright
- chromatic
- percy
- backstopjs

## Examples

- `Disabling CSS animations with `* { animation: none !important }` removes most flake in one line.`
- `A 0.1% pixel threshold absorbs font antialiasing while still catching a shifted button.`

## Safety

- Baselines are code: review them like code and never auto-approve in CI.
- Do not capture screens with real customer data or secrets.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `playwright` | stdio | standard | medium | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/testing/visual-regression-testing`). First-party skill, maintained in this repository.

## Notes

- Font loading races are the top cause of false diffs; wait for `document.fonts.ready`.
- Visual tests complement behavioural tests; neither replaces the other.
- Pairs with: `component-testing`, `accessibility-automation`.
