# Service Boundary Definition

## Purpose
Defines clear boundaries for what each service owns and explicitly does not own, preventing cross-service data coupling.

## Role
Solution Architect

## Phase
Planning (Stage 3)

## Triggered By
`technical-assessment` identifies services affected.

## Inputs
- Affected services list from `technical-assessment`

## Key Rules
- Two services must NEVER own the same entity.
- `*-subgraph` must NEVER access a database directly.
- Services communicate: gRPC (internal), GraphQL (external), Kafka (async).
- Each `*-grpc` service owns its own PostgreSQL + Redis + Debezium.

## Process
1. For each affected service, define:
   - Entity ownership (what data does this service own exclusively?)
   - Responsibilities (what operations does this service perform?)
   - Non-responsibilities (what is explicitly NOT this service's concern?)
   - Communication contracts (how does it talk to other services?)
2. Verify no entity ownership overlap between services.
3. Document boundaries in PRD technical requirements section.
4. Flag any proposed violations to PM for escalation.

## Outputs
Entity ownership and responsibility boundaries per affected service, documented in the PRD.

## Quality Gates
- [ ] Entity ownership defined for all affected services
- [ ] No ownership overlaps
- [ ] Communication protocols specified per service interaction
- [ ] *-subgraph confirmed to have no direct database access

## References
- `.claude/skills/solution-architect/technical-assessment/SKILL.md`
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
