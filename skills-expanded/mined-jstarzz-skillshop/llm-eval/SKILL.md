---
name: llm-eval
description: "Design repeatable evaluations for LLM features using representative cases, rubrics, failure taxonomies and regression baselines. Use when LLM eval, prompt regression, AI quality."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "qa"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Llm Eval

Design repeatable evaluations for LLM features using representative cases, rubrics, failure taxonomies and regression baselines.

## Activate when

- LLM eval
- prompt regression
- AI quality

## Focus

- Primary mission: Design repeatable evaluations for LLM features using representative cases, rubrics, failure taxonomies and regression baselines.
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
- A result that directly satisfies: Design repeatable evaluations for LLM features using representative cases, rubrics, failure taxonomies and regression baselines.

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
