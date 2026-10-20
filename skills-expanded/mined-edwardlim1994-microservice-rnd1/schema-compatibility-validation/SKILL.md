# Schema Compatibility Validation

## Purpose
Validates that schema changes are backward compatible before they are committed and registered in Apicurio.

## Role
Data Engineer

## Phase
Development (BEFORE raising PR on `api/` branch)

## Triggered By
Any change to `contracts/` directory.

## Inputs
- Schema changes on the current `api/` branch

## Tools
- `buf breaking`: validates proto backward compatibility
- Apicurio compatibility API: validates against registered schema

## Process

### Proto Validation
Run: `buf breaking --against .git#branch=main contracts/`. This compares current changes against main branch. Breaking changes detected → must use deprecation flow instead of deletion.

### Apicurio Validation (for new schema versions)
Test: `POST /apis/ccompat/v7/compatibility/subjects/{subject}/versions/latest`. Response: `is_compatible: true | false`.

### Breaking Change Classification
- SAFE: adding optional field, adding new message type
- BREAKING: removing field, changing field type, renaming field
- For breaking changes: must use `api-deprecation-management` flow (minimum 2 sprints)

### CI Gate
`buf breaking` runs automatically on any PR touching `contracts/`. If it fails: PR is blocked. Data Engineer must either use the deprecation flow (preferred) or get explicit Architect sign-off that the breaking change is intentional.

## Outputs
Validation pass/fail result; escalation to Architect if breaking.

## Quality Gates
- [ ] buf breaking passes before PR raised
- [ ] Apicurio compatibility API tested for new versions
- [ ] Breaking changes escalated to Architect
- [ ] CI gate will catch any missed validations

## References
- `.claude/skills/data-engineer/schema-implementation/SKILL.md`
- `.claude/skills/solution-architect/api-deprecation-management/SKILL.md`
