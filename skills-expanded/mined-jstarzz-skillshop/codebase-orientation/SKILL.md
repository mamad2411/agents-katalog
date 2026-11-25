---
name: codebase-orientation
description: "Teach a new developer or agent how a repository works quickly enough to make safe changes. Use when new contributor, unfamiliar codebase, handoff."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "meta"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Codebase Orientation

Teach a new developer or agent how a repository works quickly enough to make safe changes.

## Activate when

- new contributor
- unfamiliar codebase
- handoff

## Focus

- Primary mission: Teach a new developer or agent how a repository works quickly enough to make safe changes.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Inspect the task, repository instructions, available evidence, and current state before deciding what to do.
2. Separate facts, inferences, assumptions, and unresolved unknowns; do not silently promote guesses into facts.
3. Choose the smallest scope that satisfies the skill's mission and the user's actual goal.
4. Use repository/runtime evidence to make the result project-specific rather than a generic checklist.
5. Identify what downstream skill, engineer, or verification step should consume this output.
6. Keep the artifact concise enough to be reused by another agent or teammate.
7. Before finishing, verify that the output is internally consistent and does not claim evidence that was never obtained.

## Deliverables

- Evidence-based output for the skill's mission
- Explicit assumptions and unknowns
- Clear downstream actions
- A result that directly satisfies: Teach a new developer or agent how a repository works quickly enough to make safe changes.

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
