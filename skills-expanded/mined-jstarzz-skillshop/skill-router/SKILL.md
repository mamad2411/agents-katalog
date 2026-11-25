---
name: skill-router
description: "Select and sequence the smallest useful set of specialist skills for the current task. Use when multi-domain engineering task, unclear specialist, compose several skills."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "meta"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Skill Router

Select and sequence the smallest useful set of specialist skills for the current task.

## Activate when

- multi-domain engineering task
- unclear specialist
- compose several skills

## Focus

- Primary mission: Select and sequence the smallest useful set of specialist skills for the current task.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Read the task and inspect project signals before selecting anything.
2. Classify the task by lifecycle phase, surface area, risk, evidence needed, and whether execution or review is requested.
3. Rank candidate skills by direct relevance. Prefer 1-4 primary skills; do not load a giant bundle because tags happen to match.
4. Add support skills only if they close a concrete gap, such as verification, security, load, migration, or accessibility.
5. Resolve deliberate tensions explicitly: `caveman` minimizes complexity while `future-proof` protects only justified extension points; `cheap-ass` minimizes cost while `production-readiness` protects launch requirements.
6. Sequence discovery/review before implementation and verification after change.
7. Re-route when new evidence changes the shape of the problem instead of stubbornly finishing the original skill plan.
8. State selected skills, why each is needed, execution order, and notable skills intentionally not selected.

## Deliverables

- Evidence-based output for the skill's mission
- Explicit assumptions and unknowns
- Clear downstream actions
- A result that directly satisfies: Select and sequence the smallest useful set of specialist skills for the current task.

## Common failure modes

- Loading every available skill 'just in case'
- Replacing evidence with conversational confidence
- Producing a giant narrative when a compact reusable artifact would do
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
