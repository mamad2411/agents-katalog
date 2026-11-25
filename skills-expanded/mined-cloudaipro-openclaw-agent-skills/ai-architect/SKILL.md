---
name: ai-architect
description: Meta skill architect for designing new agent skills, drafting SKILL.md specifications, and producing implementation blueprints with trigger boundaries, resources, and validation gates. Use when users ask to create or refactor AI skills, role prompts, or agent workflows.
---

# AI Architect

## Objective
Design robust, implementation-ready skill specs that can be scaffolded into Codex/OpenClaw skill folders.

## Trigger Rules
Use when users request new skill design or skill-system architecture.

Positive cues:
- "Create a new skill for ..."
- "Draft SKILL.md for this role."
- "Design an agent workflow and folder structure."

Do not use when:
- User requests only explanation of external trends.
- User requests only root-cause social analysis.
- User asks for operational planning without skill design.

## Inputs
Required:
- Skill purpose and core task.

Optional:
- Tooling constraints.
- Permission profile.
- Output schema requirements.

## Output Schema
Return universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Skill architecture brief.
2. Trigger and resource matrix.
3. Ready-to-edit SKILL.md draft and scaffold plan.
4. Validation and rollout checklist.

## Workflow
1. Clarify scope and trigger boundaries.
2. Define input/output contract and permission model.
3. Propose folder layout with scripts/references/assets as needed.
4. Draft SKILL.md and runtime implementation notes.
5. Define validation gates and release phases.

## Quality Bar
- Trigger boundaries must be explicit and testable.
- Output contract must be schema-aligned.
- Rollout must include evaluation and rollback logic.

## Safety Rules
- Keep least-privilege defaults.
- Require explicit approval for write-side actions.
- Avoid ambiguous or non-verifiable requirements.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Reasoning artifact validator: `scripts/validate_reasoning_artifacts.py`
