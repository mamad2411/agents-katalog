---
name: journey-compiler
description: "Compile a semantic journey into manual cases, browser E2E, API sequences and load scenarios without brittle coordinate coupling. Use when recording to tests, compile journey, Playwright API load."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Journey Compiler

Compile a semantic journey into manual cases, browser E2E, API sequences and load scenarios without brittle coordinate coupling.

## Activate when

- recording to tests
- compile journey
- Playwright API load

## Focus

- Primary mission: Compile a semantic journey into manual cases, browser E2E, API sequences and load scenarios without brittle coordinate coupling.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Read the semantic journey goal, actor, preconditions, actions, dynamic values and assertions.
2. Preserve domain intent while stripping incidental implementation detail from the recording.
3. For manual output, produce concise semantic steps, test data, expected checkpoints and cleanup.
4. For browser E2E, prefer role/label/stable-test-id selectors and state assertions; avoid coordinates and nth-child selectors.
5. For API output, collapse incidental browser/background requests and keep the business request sequence, auth/session semantics and dynamic extraction.
6. For load output, remove static assets and UI-only noise while retaining auth, correlation values, data cardinality and realistic think time.
7. Attach the source journey ID/version to generated artifacts so drift can be detected.
8. Do not automatically overwrite hand-maintained tests when regeneration would destroy meaningful assertions.

## Deliverables

- Test charter or cases
- Defects with reproducible evidence
- Coverage gaps and regression candidates
- A result that directly satisfies: Compile a semantic journey into manual cases, browser E2E, API sequences and load scenarios without brittle coordinate coupling.

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
