---
name: requirements-to-tasks
description: "Convert messy product or client requirements into testable acceptance criteria and implementable vertical tasks. Use when client notes to tickets, ambiguous feature, acceptance criteria needed."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "planning"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Requirements To Tasks

Convert messy product or client requirements into testable acceptance criteria and implementable vertical tasks.

## Activate when

- client notes to tickets
- ambiguous feature
- acceptance criteria needed

## Focus

- Primary mission: Convert messy product or client requirements into testable acceptance criteria and implementable vertical tasks.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Establish the authoritative goal, actors, constraints, non-goals, and current context.
2. Find ambiguities or decisions that materially change implementation; resolve from evidence when possible and surface the rest explicitly.
3. Break the problem into observable behaviors and engineering constraints rather than file-level tasks.
4. Compare credible options when there is a real design choice; do not manufacture fake alternatives.
5. Identify high-risk assumptions and the cheapest experiment or inspection that could invalidate them.
6. Define acceptance or decision criteria before recommending execution.
7. Produce a durable plan that another engineer can follow without reconstructing hidden reasoning.

## Deliverables

- Decision/plan artifact
- Acceptance or decision criteria
- Open risks and assumptions
- A result that directly satisfies: Convert messy product or client requirements into testable acceptance criteria and implementable vertical tasks.

## Common failure modes

- Turning assumptions into requirements without marking them
- File-by-file task lists with no acceptance criteria
- Choosing architecture before identifying the risky unknowns
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
