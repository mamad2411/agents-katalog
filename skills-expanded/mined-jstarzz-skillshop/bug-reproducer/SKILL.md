---
name: bug-reproducer
description: "Turn vague or intermittent defect reports into minimal reliable reproductions with evidence and regression candidates. Use when sometimes bug, vague report, timing bug."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Bug Reproducer

Turn vague or intermittent defect reports into minimal reliable reproductions with evidence and regression candidates.

## Activate when

- sometimes bug
- vague report
- timing bug

## Focus

- Primary mission: Turn vague or intermittent defect reports into minimal reliable reproductions with evidence and regression candidates.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Parse the report into actor, environment, data state, action, expected behavior and observed behavior.
2. Attempt the literal report first and record every attempt rather than mentally averaging results.
3. Vary one dimension at a time: timing, concurrency, retry, network, navigation, account state, data state and device/browser.
4. Once it reproduces, remove steps and variables until the smallest reliable trigger remains.
5. Quantify reproduction frequency for intermittent bugs.
6. Capture logs/network/state at the earliest divergence from expected behavior.
7. Persist the minimal sequence as a semantic journey or test fixture.
8. Hand the evidence to `systematic-debugging` and create a regression test once the invariant is understood.

## Deliverables

- Test charter or cases
- Defects with reproducible evidence
- Coverage gaps and regression candidates
- A result that directly satisfies: Turn vague or intermittent defect reports into minimal reliable reproductions with evidence and regression candidates.

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
