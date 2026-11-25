---
name: qa-explorer
description: "Explore an application like a skeptical human tester by varying input, navigation, timing, state and failure conditions. Use when exploratory QA, new workflow, find edge cases."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Qa Explorer

Explore an application like a skeptical human tester by varying input, navigation, timing, state and failure conditions.

## Activate when

- exploratory QA
- new workflow
- find edge cases

## Focus

- Primary mission: Explore an application like a skeptical human tester by varying input, navigation, timing, state and failure conditions.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Learn the intended journey, business invariants and supported environment before exploring.
2. Run the happy path once to establish a known-good baseline.
3. Vary one dimension at a time: null/min/max/unicode data, navigation order, back/refresh, duplicate clicks, multiple tabs, session expiry, permissions, timing and network interruption.
4. Exercise loading, empty, error, retry, cancellation and partial-success states.
5. On responsive products, repeat critical paths at representative narrow and wide viewports; use actual touch/keyboard semantics where relevant.
6. Record each issue with exact reproduction, expected result, actual result, environment and evidence.
7. Minimize intermittent reproductions and quantify frequency.
8. Promote stable, important discoveries into semantic journeys and regression tests.

## Deliverables

- Test charter or cases
- Defects with reproducible evidence
- Coverage gaps and regression candidates
- A result that directly satisfies: Explore an application like a skeptical human tester by varying input, navigation, timing, state and failure conditions.

## Common failure modes

- Testing only the happy path
- Calling automated scanning 'manual QA'
- Brittle coordinate-only recordings with no semantic assertions
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
