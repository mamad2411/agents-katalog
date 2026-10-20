# Proto Contract Design

## Purpose
Defines or modifies gRPC service contracts in `contracts/proto/services/` as the source of truth for internal service communication.

## Role
Solution Architect

## Phase
Planning (Stage 3)

## Triggered By
New or modified gRPC service identified in `technical-assessment`.

## Inputs
- `service-boundary-definition` output for the affected service

## Location
`contracts/proto/services/{service-name}/` — Architect raises PR. Data Engineer reviews for schema correctness + compatibility.

## Conventions
- Proto3 only
- snake_case field names
- PascalCase message names
- Every service file: `{service_name}.proto`
- Include `field_mask` for partial updates where applicable
- Never remove a field — deprecate first (see `api-deprecation-management`)
- `@deprecated` fields include: `option (gogoproto.moretags) = "deprecated:\"true\""`

### Anti-Pattern
Never define proto schema inside a service directory. Services reference `contracts/proto/services/` only. Generated types: `packages/api/src/generated/{service}/proto/` — NEVER edit.

## Process
1. Design proto contract based on `service-boundary-definition`.
2. Write proto file to `contracts/proto/services/{service-name}/`.
3. Raise PR: branch `api/{KAN-N}` from `feat/{KAN-N}`.
4. Request Data Engineer review for compatibility.
5. After approval: Data Engineer runs `api-type-generation`.

## Outputs
Proto contract PR on `api/{KAN-N}` branch.

## Quality Gates
- [ ] Proto3 syntax used
- [ ] Naming conventions followed
- [ ] No fields removed from existing proto (deprecated instead)
- [ ] Data Engineer has reviewed for compatibility

## References
- `.claude/skills/solution-architect/service-boundary-definition/SKILL.md`
- `.claude/skills/solution-architect/api-deprecation-management/SKILL.md`
- Data Engineer `api-type-generation`
