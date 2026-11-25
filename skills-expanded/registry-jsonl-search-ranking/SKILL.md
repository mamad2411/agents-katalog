---
name: registry-jsonl-search-ranking
description: Build and query a JSONL registry with relevance scoring, type filtering, and trigger matching.
---

# Registry Jsonl Search Ranking

Build and query a JSONL registry with relevance scoring, type filtering, and trigger matching.

## When to Use

Use this skill when:

- Working with code in `src/registry/index.ts/`
- User mentions "registry"
- User mentions "search"
- User mentions "jsonl"
- User mentions "score"
- User mentions "index"

## Patterns

- append-only JSONL entries for skills and agents
- scored search over name/description/triggers/category
- type filter (skill|agent) and result limiting
- list/get helpers for registry introspection

## Examples

```
const registry = new Registry(cwd); const results = await registry.search(query, { type, limit });
```

## Category

**quality** - Testing, validation, and code quality
