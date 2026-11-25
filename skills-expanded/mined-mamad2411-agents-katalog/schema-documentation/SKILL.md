# Schema Documentation

## Purpose
Documents schema fields with business meaning, alongside the PR that introduces or changes them.

## Role
Technical Writer

## Phase
Development (alongside PR — triggered when PR touches `contracts/`)

## Triggered By
PR touching `contracts/`.

## Inputs
- Schema files from `contracts/` (source material only — never modified)

## Rule
Writes ONLY to `apps/docs/`. Reads FROM `openspec/`, `contracts/`, `apps/servers/` as source material only. NEVER writes to `openspec/`, `contracts/`, `.claude/skills/`.

## Process
Document per field:
- Purpose (business meaning — not just data type)
- Type and format
- Required vs optional
- Valid values or ranges
- Example values
- Deprecation notices (if `@deprecated`)

Location matches schema type:
- Proto event schemas → `schemas/kafka/{service}-events.md`
- Meilisearch schemas → `schemas/search/{index}.md`
- ClickHouse schemas → `schemas/analytics/{table}.md`

## Outputs
Location: `apps/docs/src/content/internal/latest/schemas/`

## Quality Gates
- [ ] Every field documents purpose, type, required/optional, valid values, examples
- [ ] Deprecated fields clearly marked
- [ ] File placed in correct schema-type subfolder
- [ ] contracts/ source files never modified by this skill

## References
- `.claude/skills/data-engineer/schema-implementation/SKILL.md`
- `.claude/skills/technical-writer/docs-site-management/SKILL.md`
