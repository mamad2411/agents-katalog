---
name: systematic-debugging
description: "Debug through evidence, narrowing boundaries and hypothesis testing before attempting fixes. Use when confusing failure, intermittent bug, multiple failed fixes."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "delivery"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Systematic Debugging

Debug through evidence, narrowing boundaries and hypothesis testing before attempting fixes.

## Activate when

- confusing failure
- intermittent bug
- multiple failed fixes

## Focus

- Primary mission: Debug through evidence, narrowing boundaries and hypothesis testing before attempting fixes.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Capture exact symptom, environment, frequency and the last known-good behavior.
2. Reproduce the failure or establish a deterministic failing signal before changing production code whenever practical.
3. Narrow the failing boundary and trace data/control flow backwards to the earliest state that diverges from expectation.
4. List hypotheses ranked by likelihood and by cheapness to falsify.
5. Change one variable at a time; record evidence from each experiment.
6. Do not patch until the causal mechanism is understood well enough to predict why the proposed change will fix it.
7. After the fix, rerun the original reproduction and nearby counterexamples that could disprove the root-cause story.
8. Add regression coverage for the invariant, not merely the exact accidental symptom.

## Deliverables

- Minimal code/config change
- Appropriate regression or preservation tests
- Fresh verification evidence
- A result that directly satisfies: Debug through evidence, narrowing boundaries and hypothesis testing before attempting fixes.

## Common failure modes

- Fixing symptoms without understanding the failing mechanism
- Mixing unrelated cleanup into a targeted change
- Claiming tests passed from stale or partial output
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
