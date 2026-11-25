# API Deprecation Management

## Purpose
Manages the formal deprecation process for proto fields and GraphQL types to ensure backward compatibility during API evolution.

## Role
Solution Architect

## Phase
Planning (when breaking change needed) + Development (monitoring)

## Triggered By
Story requires removing or changing an existing API field/type.

## Inputs
- Field/type slated for removal or change

## Rule
Never remove a field — always deprecate first. Deprecation period: minimum 2 sprints before removal.

## Process
1. Mark field/endpoint as deprecated in proto/SDL:
   - Proto: add option with `deprecated: true` annotation
   - GraphQL: add `@deprecated(reason: "Use {newField} instead")`
2. Both old and new versions run simultaneously for minimum 2 sprints.
3. Create kanban tracking card:
   - type: `tech-debt`
   - title: `[Deprecation] Remove {field} from {service}`
   - body: deprecated in v{X}.{Y}.{Z}, safe to remove from v{X}.{Y}.{Z+2}
4. Consumers migrate to new version during deprecation window.
5. After deprecation period: Architect creates removal task in planning.
6. Removal task goes through normal planning + development cycle.

## Outputs
Deprecated field/type marked in contracts, kanban tracking card created.

## Quality Gates
- [ ] Deprecated fields marked with deprecation annotation
- [ ] Deprecation tracking kanban card created
- [ ] Removal date documented (minimum 2 sprints from deprecation)
- [ ] Consumer migration path documented

## References
- `.claude/skills/solution-architect/proto-contract-design/SKILL.md`
- `.claude/skills/solution-architect/graphql-schema-design/SKILL.md`
