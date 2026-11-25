---
name: accessibility-automation
description: "Automate accessibility verification: axe in component and E2E tests, keyboard and focus checks, CI gates, and the issues automation cannot catch."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - axe accessibility test ci
  - automate wcag checks
  - keyboard navigation test
  - accessibility regression gate
  - screen reader test automation
aliases:
  - a11y-automation
keywords:
  - accessibility
  - a11y
  - axe
  - wcag
  - keyboard
  - focus
  - aria
mcp_servers:
  - playwright
  - github
  - chrome-devtools
source: custom
enabled: true
---

# Accessibility Automation

## Purpose

Automate accessibility verification: axe in component and E2E tests, keyboard and focus checks, CI gates, and the issues automation cannot catch.

## When to Use

- Accessibility must be enforced continuously, not audited once.
- A component library needs a guard against regressions.
- Compliance requires evidence of testing, not just intent.

## When NOT to Use

- A third-party widget cannot be instrumented.
- The requirement is a manual audit by a specialist for certification.
- Automation is being proposed as a substitute for usability testing.

## Capabilities

- Run axe on rendered components and pages in CI.
- Assert keyboard reachability and visible focus order.
- Check contrast at the token level and in real rendering.
- Gate merges on new violations only, so legacy debt does not block work.
- Document what automation cannot detect and schedule manual checks.

## Inputs

- The pages and components in scope, and their states.
- The target conformance level (AA is the common baseline).
- A baseline of existing violations to ratchet down.

## Workflow

1. Add axe to component tests for the primitives first.
2. Run it on key pages in E2E across desktop and mobile viewports.
3. Write explicit keyboard tests: tab order, focus trap, escape from modals.
4. Snapshot the current violation count and fail only on regressions.
5. Schedule manual screen-reader passes for flows automation cannot judge.
6. Ratchet the baseline down every cycle.

## Tools

- axe-core
- playwright
- pa11y
- lighthouse

## Examples

- `axe catches missing labels and contrast but cannot tell you the reading order is nonsense.`
- `A focus trap that axe passes can still strand keyboard users — test Escape explicitly.`

## Safety

- Never suppress a violation without a tracked issue and an owner.
- Automated passes do not certify conformance.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `playwright` | stdio | standard | medium | — |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `chrome-devtools` | stdio | standard | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/testing/accessibility-automation`). First-party skill, maintained in this repository.

## Notes

- Test with the keyboard only for a day; it finds more than the scanner.
- Design tokens are the cheapest place to fix contrast.
- Pairs with: `visual-regression-testing`, `component-testing`.
