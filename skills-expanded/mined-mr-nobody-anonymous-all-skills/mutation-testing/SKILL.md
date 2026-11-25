---
name: mutation-testing
description: "Measure test-suite strength with mutation testing: pick operators, scope runs, read survivors and raise the mutation score without chasing 100%."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - mutation testing setup
  - mutation score low
  - stryker js
  - pitest java
  - are my tests actually strong
aliases:
  - mutation
  - stryker
keywords:
  - mutation-testing
  - stryker
  - pitest
  - mutants
  - test-strength
  - coverage
mcp_servers:
  - github
  - filesystem
source: custom
enabled: true
---

# Mutation Testing

## Purpose

Measure test-suite strength with mutation testing: pick operators, scope runs, read survivors and raise the mutation score without chasing 100%.

## When to Use

- Coverage is high but defects keep escaping.
- You need evidence that tests assert behaviour rather than execute lines.
- A critical module deserves stronger verification than line coverage shows.

## When NOT to Use

- The suite is slow and unstable; stabilize first.
- The code is generated or trivial getters.
- A full-repo run would take hours; scope it instead of skipping it.

## Capabilities

- Run mutation testing on changed files and critical modules only.
- Configure operators and timeouts that produce signal, not noise.
- Triage survivors: equivalent mutants versus missing assertions.
- Raise the score by strengthening assertions, not by deleting tests.
- Track the score as a trend per module.

## Inputs

- A green test suite with a measured runtime.
- The modules that carry business risk.
- The CI time budget for the mutation job.

## Workflow

1. Baseline the mutation score on one representative module.
2. Shortlist surviving mutants and read each one.
3. Add or tighten assertions where the mutant is a real behaviour.
4. Mark equivalent mutants with a documented suppression.
5. Run on changed files in CI and full runs nightly.
6. Track the trend; a sudden drop means a test was weakened.

## Tools

- stryker
- pitest
- mutmut
- cosmic-ray

## Examples

- `A mutant that flips `>` to `>=` surviving means no test covers the boundary.`
- `Chasing 100% usually means writing tests for equivalent mutants, which is pure cost.`

## Safety

- Never weaken or delete tests to raise the mutation score.
- Suppressions need a reason and a reviewer.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `github` | http | standard | medium | `GITHUB_PERSONAL_ACCESS_TOKEN` |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/testing/mutation-testing`). First-party skill, maintained in this repository.

## Notes

- Mutation testing finds the assertions you forgot, faster than reading coverage reports.
- Start with the domain layer, not with controllers.
- Pairs with: `contract-testing`, `component-testing`.
