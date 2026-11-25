# Technical Assessment

## Purpose
Assesses technical implications of a user story during Stage 3 of planning — identifies affected services, risks, and driver requirements.

## Role
Solution Architect

## Phase
Planning (Stage 3)

## Triggered By
Stage 2 complete, AC finalised.

## Inputs
- Finalised AC from Stage 2
- Current `system-architecture-diagram`
- PRD draft

## Process
1. Read `system-architecture-diagram` to understand current system state.
2. Analyse User Story and PRD draft.
3. Identify which existing services are affected.
4. Determine if a new service is needed (and which type: grpc/subgraph/cron).
5. Identify which drivers needed: `GrpcDriver`, `ApolloDriver`, `KafkaDriver`, `CronDriver`.
6. Determine if `packages/server` framework covers the need or requires extension.
7. Identify technical risks (complexity, unknown patterns, performance).
8. Document findings for PM to include in PRD.
9. Trigger `service-boundary-definition` and `dependency-mapping`.

## Outputs
Technical findings for PRD Stage 5 (affected services, new-service determination, risks).

## Quality Gates
- [ ] All affected services identified
- [ ] New service need assessed
- [ ] Technical risks documented
- [ ] Findings ready for PRD Stage 5

## References
- `.claude/skills/solution-architect/system-architecture-diagram/SKILL.md`
- `.claude/skills/solution-architect/service-boundary-definition/SKILL.md`
- `.claude/skills/solution-architect/dependency-mapping/SKILL.md`
- `.claude/skills/pm/prd-writing/SKILL.md`
