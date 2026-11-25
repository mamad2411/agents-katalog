# Schema Implementation

## Purpose
Writes actual schema files in `contracts/` based on designs from the planning phase.

## Role
Data Engineer

## Phase
Development

## Triggered By
`/schema KAN-{N}` command or feature branch needs types.

## Inputs
- Planning-phase schema designs (Kafka event, Meilisearch, ClickHouse)

## Branching
`api/{KAN-N}` from `feat/{KAN-N}`. This branch MUST merge FIRST before `task/` branches can start.

## Ownership

### Files Data Engineer Writes to contracts/
- `contracts/proto/events/` ← Kafka event schemas
- `contracts/meilisearch/` ← search index schemas
- `contracts/clickhouse/` ← table definitions + migrations

### Files Data Engineer NEVER Writes to contracts/ (Architect owns)
- `contracts/proto/services/` ← gRPC service contracts
- `contracts/graphql/` ← GraphQL SDL

Data Engineer reviews ALL proto PRs raised by Architect for: schema correctness (types, field names, conventions), backward compatibility (no breaking changes without deprecation), Apicurio compatibility (can this schema be registered?).

## Process
1. Create branch: `api/{KAN-N}` from `feat/{KAN-N}`.
2. Write schema files based on planning designs.
3. Run `schema-compatibility-validation` before committing.
4. Raise PR: `api/{KAN-N}` → `feat/{KAN-N}`.
5. Gate: `buf lint` + `buf breaking` + type generation must pass.
6. After merge: trigger `api-type-generation`.

## Outputs
Schema files committed to `contracts/`, PR merged into `feat/{KAN-N}`.

## Quality Gates
- [ ] Branched from feat/ (not us/ or release/)
- [ ] Only writes to correct contracts/ subdirectories
- [ ] schema-compatibility-validation run before PR
- [ ] PR merged before any task/ branches start work

## References
- `.claude/skills/data-engineer/schema-compatibility-validation/SKILL.md`
- `.claude/skills/data-engineer/api-type-generation/SKILL.md`
- `.claude/skills/solution-architect/proto-contract-design/SKILL.md`
