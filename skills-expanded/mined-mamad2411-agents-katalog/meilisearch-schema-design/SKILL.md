# Meilisearch Schema Design

## Purpose
Designs TypeScript index schemas for Meilisearch search indexes.

## Role
Data Engineer

## Phase
Planning (Stage 3)

## Triggered By
Story requires search functionality.

## Inputs
- Search requirements from the story
- `service-boundary-definition` alignment

## Location
`contracts/meilisearch/{index-name}.ts`

## Process
Define the schema and settings:
```typescript
export interface {IndexName}Document {
  id: string // always required, used as primary key
  // searchable fields
  // filterable fields
  // sortable fields
}

export const {indexName}Settings = {
  searchableAttributes: ['field1', 'field2'],
  filterableAttributes: ['status', 'category'],
  sortableAttributes: ['createdAt', 'score'],
  rankingRules: ['words', 'typo', 'proximity', 'attribute', 'sort', 'exactness'],
  synonyms: {},
  stopWords: [],
}
```

### Design Considerations
- `searchableAttributes`: fields users search on (ordered by importance)
- `filterableAttributes`: fields used in faceted search/filtering
- `sortableAttributes`: fields users can sort results by

## Outputs
Meilisearch index schema in `contracts/meilisearch/{index-name}.ts`.

## Quality Gates
- [ ] id field always present as primary key
- [ ] searchableAttributes ordered by importance
- [ ] Settings exported alongside document interface
- [ ] Architect reviewed for alignment with service-boundary-definition

## References
- `.claude/skills/solution-architect/service-boundary-definition/SKILL.md`
- `.claude/skills/data-engineer/meilisearch-index-management/SKILL.md`
