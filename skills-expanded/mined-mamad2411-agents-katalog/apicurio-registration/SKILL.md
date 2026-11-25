# Apicurio Registration

## Purpose
Registers all schema types in Apicurio Registry at SIT, managing versions and compatibility rules.

## Role
Data Engineer

## Phase
Development (after `schema-implementation`)

## Triggered By
`schema-implementation` PR merged.

## Inputs
- Merged schema files (proto events, GraphQL SDL, OpenAPI)

## Registry Endpoints
- Kafka schemas (Confluent-compatible): `/apis/ccompat/v7`
- API schemas (native Apicurio): `/apis/registry/v3`

## Process

### Registration Per Schema Type
1. Proto event schemas → register in ccompat endpoint (default group):
   `curl -X POST http://{SIT_APICURIO}/apis/ccompat/v7/subjects/{topic-name}-value/versions`
2. GraphQL SDL → register in native endpoint by service group:
   `curl -X POST http://{SIT_APICURIO}/apis/registry/v3/groups/{service}/artifacts`
3. OpenAPI specs → register in native endpoint by service group.

### Compatibility Rules
- Set BACKWARD compatibility for all Kafka schemas (consumers can read old + new).
- Set FULL compatibility for critical schemas (both producers and consumers flexible).
- Test compatibility before registering new version:
  `curl -X POST .../compatibility/subjects/{subject}/versions/latest`

## Outputs
Registered schemas in Apicurio Registry with compatibility rules set.

## Quality Gates
- [ ] All schemas registered in correct endpoint
- [ ] Compatibility rules configured per schema
- [ ] New schema version tested for compatibility before registration
- [ ] Registration confirmed (HTTP 200 response)

## References
- `.claude/skills/data-engineer/schema-implementation/SKILL.md`
- `.claude/skills/data-engineer/schema-compatibility-validation/SKILL.md`
