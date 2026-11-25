---
name: data-integrity-tester
description: "Verify persisted data stays internally consistent across success, failure, retry, cancellation and migration paths. Use when data corruption, transaction QA, migration integrity."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Data Integrity Tester

Verify persisted data stays internally consistent across success, failure, retry, cancellation and migration paths.

## Activate when

- data corruption
- transaction QA
- migration integrity

## Focus

- Primary mission: Verify persisted data stays internally consistent across success, failure, retry, cancellation and migration paths.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Start from intended behavior, business invariants, supported environments, and the risk of failure.
2. Establish the happy path once, then deliberately vary input, state, ordering, navigation, permissions, timing, and failure conditions.
3. Capture exact environment, data, actions, expected result, actual result, and evidence for every defect.
4. Prefer semantic actions and business assertions over brittle implementation details such as coordinates or nth-child selectors.
5. Classify discovered behavior into defect, UX issue, requirement ambiguity, environmental issue, or expected behavior.
6. Promote stable high-value discoveries into regression coverage at the cheapest reliable test layer.
7. Finish with explicit coverage gaps and what remains unverified rather than implying exhaustive testing.

## Deliverables

- Test charter or cases
- Defects with reproducible evidence
- Coverage gaps and regression candidates
- A result that directly satisfies: Verify persisted data stays internally consistent across success, failure, retry, cancellation and migration paths.

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
