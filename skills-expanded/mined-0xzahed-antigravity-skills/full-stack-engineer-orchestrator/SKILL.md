---
name: full-stack-engineer-orchestrator
description: Orchestrate a full-stack implementation across frontend, backend,
  data, and ops. Use to coordinate the whole build.
metadata:
  tags: full, stack, engineer, orchestrator
---

# Full-Stack Engineering Orchestration

## Use this skill when
- Planning and coordinating a full-stack feature
- Sequencing work across layers correctly
- Reviewing a feature end to end

## Do not use this skill when
- Single-layer tasks (use the specific skill)
- Reviewing without being asked to coordinate

## Instructions
1. Define the feature end to end: API shape, data model, UI, ops.
2. Sequence: contract first, then data, services, API, UI, tests.
3. Enforce the contract at every seam (types, schemas, openapi).
4. Coordinate tests at each layer and integration tests across.
5. Review as an owner: correctness, security, perf, observability.
6. Delegate narrow areas to the matching skills.
7. Finish with verification: tests, deploy, monitoring.

## Checklist
- Contract defined before layers
- Every layer tested
- Feature verifiable end to end

## Output Format
- Plan | contract | layer work | tests | verification

## Common Mistakes
- Bottom-up guessy building
- Forgetting the contract is the glue
- Testing only the happy path
