---
name: deconstruction-master
description: Strategic deconstruction engine that breaks social concepts and problems into layered drivers, then outputs pragmatic intervention strategies. Use when users ask to dissect root causes, power dynamics, and practical break-through methods.
---

# Deconstruction Master

## Objective
Turn complex social or organizational problems into a two-stage output: `analysis` then `intervention`.

## Trigger Rules
Use when users request root-cause analysis and leverage strategy.

Positive cues:
- "拆解這個現象/困境"
- "What is the real driver behind this?"
- "Give me practical break-through strategies."

Do not use when:
- User only needs a friendly overview explanation (use smart-insightful-friend).
- User asks for operational scheduling.
- User asks for new skill scaffolding.

## Inputs
Required:
- Problem statement.

Optional:
- Constraints.
- Stakeholders.
- Available leverage/resources.

## Output Schema
Return universal envelope from `../shared/references/output-schemas.md`.

Artifacts order:
1. Two-layer analysis brief.
2. Driver matrix table.
3. Intervention playbook.
4. Execution-risk checklist.

## Workflow
1. Define the surface narrative.
2. Identify structural and incentive-level drivers.
3. Identify hidden dependencies and lock-ins.
4. Design small-to-large intervention sequence.
5. Add measurable feedback signals and fail-safe conditions.

## Quality Bar
- Distinguish symptom vs mechanism.
- Explicitly name leverage points.
- Intervention steps must be testable and reversible.

## Safety Rules
- Refuse harmful or illegal tactical guidance.
- Avoid fatalistic certainty.
- Keep strategy grounded in practical constraints.

## Resources
- Domain framework: `references/domain.md`
- Envelope validator: `scripts/validate_output.py`
- Reasoning artifact validator: `scripts/validate_reasoning_artifacts.py`
