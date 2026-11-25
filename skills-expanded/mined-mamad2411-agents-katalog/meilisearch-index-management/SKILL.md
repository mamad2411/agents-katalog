# Meilisearch Index Management

## Purpose
Creates and updates Meilisearch search indexes from TypeScript schema definitions.

## Role
Data Engineer

## Phase
Development

## Triggered By
New or modified Meilisearch schema in `contracts/meilisearch/`.

## Inputs
- `meilisearch-schema-design` output

## Process

### Meilisearch Index Operations
- Create index: `POST /indexes`
- Update settings: `PATCH /indexes/{uid}/settings`
- Swap indexes (zero-downtime schema update):
  1. Create new index with new settings
  2. Populate new index (background task)
  3. Swap indexes atomically
  4. Delete old index

### Zero-Downtime Update Process (for production)
1. Create new index: `{original-name}_new`.
2. Re-index all documents into new index.
3. `POST /swap-indexes`: `[{"indexes": ["{original}", "{original}_new"]}]`.
4. Delete `{original}_new` (old index now has new name).

Local development: directly update index settings (no downtime concern).

## Outputs
Created/updated Meilisearch index matching schema.

## Quality Gates
- [ ] Index created from TypeScript schema in contracts/meilisearch/
- [ ] All settings applied (searchable, filterable, sortable attributes)
- [ ] Zero-downtime swap process documented if schema change is breaking
- [ ] Index functional verified (run a test query)

## References
- `.claude/skills/data-engineer/meilisearch-schema-design/SKILL.md`
