---
name: delivery-workflow-checkpoints
description: 'Checkpoint model for orchestrated delivery workflows spanning build, implementation, review, and closure. Use for progress governance and non-circular execution.'
---

# Delivery Workflow Checkpoints

Defines stable checkpoints for multi-step delivery orchestration.

## Checkpoint Sequence

1. Intake: classify request and define scope
2. Plan: propose specialist sequence
3. Confirm: obtain explicit user approval per handoff
4. Execute: run delegated specialist task
5. Validate: capture evidence (tests/build/review results)
6. Consolidate: merge outputs into a final summary
7. Close: confirm completion or queue next approved task

## Checkpoint Record Schema

Use this minimal schema in orchestration responses:

- CorrelationId
- TaskId
- CheckpointName
- AssignedSpecialist
- Status (`pending`, `approved`, `in-progress`, `completed`, `blocked`)
- Evidence
- Risks
- NextAction

## Non-Circular Rule

Before any new handoff:

- verify TaskId is not already completed,
- if repeated task is required, generate a new TaskId and document scope delta,
- include reason for re-entry in checkpoint evidence.

## Consolidation Output

Final orchestration summary should include:

1. Completed tasks and delegated specialists
2. Verification evidence collected
3. Open risks and blockers
4. Recommended next steps requiring approval
