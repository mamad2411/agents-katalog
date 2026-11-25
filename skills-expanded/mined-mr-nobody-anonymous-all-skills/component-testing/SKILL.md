---
name: component-testing
description: "Test UI components as users use them: Testing Library queries, behaviour over implementation, network mocking, and a strategy that survives refactors."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - react testing library
  - component test strategy
  - mock fetch in component test
  - testing library query priority
  - flaky component test
aliases:
  - rtl
keywords:
  - component-testing
  - testing-library
  - jest
  - vitest
  - user-event
  - msw
mcp_servers:
  - playwright
  - filesystem
source: custom
enabled: true
---

# Component Testing

## Purpose

Test UI components as users use them: Testing Library queries, behaviour over implementation, network mocking, and a strategy that survives refactors.

## When to Use

- A component has logic that must not regress: state, validation, conditional rendering.
- Tests break on every refactor because they assert implementation details.
- A network-dependent component needs deterministic tests.

## When NOT to Use

- The behaviour spans multiple pages or a real backend — use end-to-end tests.
- The code is a pure function; a unit test is cheaper and clearer.
- The only thing to verify is visual appearance.

## Capabilities

- Query by role and accessible name so tests double as a11y checks.
- Drive interaction with `user-event` rather than firing synthetic events.
- Mock the network at the boundary with MSW instead of stubbing modules.
- Assert user-visible outcomes, never internal state.
- Keep the suite fast enough to run on every commit.

## Inputs

- The user-facing behaviour the component must guarantee.
- The API responses it depends on, including error and empty states.
- The test runner and environment already in the repo.

## Workflow

1. Write the test from the user's point of view: what do they see and do?
2. Query by role/name/text; reach for `data-testid` only as a last resort.
3. Mock the network with MSW handlers per test, including a failure case.
4. Assert the outcome and the accessible state, not the className.
5. Cover empty, error and loading states explicitly — they are where bugs live.
6. Run the suite against a refactor of the component to confirm it still passes.

## Tools

- vitest
- jest
- testing-library
- msw
- playwright

## Examples

- ``getByRole('button', {name: /save/i})` survives a CSS rewrite that breaks `getByTestId('btn-save')`.`
- `An MSW handler returning 500 proves the error branch renders, which a happy-path stub never will.`

## Safety

- Do not snapshot entire component trees; they churn and hide intent.
- Never assert on internal component state — that is the refactor tax.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `playwright` | stdio | standard | medium | — |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/testing/component-testing`). First-party skill, maintained in this repository.

## Notes

- If a test needs five mocks, the component has too many responsibilities.
- Coverage of branches beats coverage of lines.
- Pairs with: `visual-regression-testing`, `typescript-advanced`.
