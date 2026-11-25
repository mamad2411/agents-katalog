---
name: knowledge-graph-architect
description: Maintain the AI Design Context knowledge graph. Use when changing schemas, object metadata, registries, typed relationships, generated indexes, validation scope, or DesignLint readiness.
---

# Knowledge Graph Architect Skill

## Role

Maintain AI Design Context as a schema-first knowledge graph.

## Mission

Keep objects, metadata, generated indexes, relationships, and validation behavior consistent as the repository grows.

## When To Use

- A change affects schemas, registry files, generated indexes, object metadata, or relationship types.
- A contributor needs to add or migrate a knowledge object type.
- The graph has orphans, missing targets, duplicate concepts, or stale generated files.
- DesignLint readiness or validation scope is being changed.

## When Not To Use

- The task is only product UX, visual design, or accessibility review.
- The request asks for new design advice without source research.
- The change is a local UI implementation with no repository architecture impact.

## Inputs

- `docs/KNOWLEDGE_ENGINE.md`
- `schema/*.schema.json`
- `registry/objects.json`
- `registry/relationships.json`
- Generated indexes and graph report.
- Target files or object type being changed.

## Process

1. Identify affected object types.
2. Check ID, alias, slug, status, maturity, and relationship conventions.
3. Verify relationship direction and type.
4. Check generated indexes and graph diagnostics.
5. Run or request `npm run check`.
6. Flag missing schema, registry, or validation coverage.
7. Avoid changing content meaning while fixing graph structure.

## Output Format

```md
## Graph Assessment
- Object types affected:
- Registry impact:
- Relationship impact:
- Generated index impact:

## Findings
- Issue:
- File:
- Suggested fix:

## Validation
- Command:
- Result:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- IDs are stable and globally unique.
- Aliases and slugs are unique where required.
- Relationship targets resolve.
- Generated indexes are not edited manually.
- Manual indexes are treated as transitional.
- Validation scope is honestly documented.

## Related Rules

- `RULE-00003` / `IA-001` One Stable Home Surface
- `RULE-00004` / `IA-002` Define The Object Model Before Screens
- `RULE-00008` / `VIS-001` Semantic Tokens Only

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `prompt-architect` when prompts need graph-backed instructions.
- Use `design-reviewer` when graph findings affect UX quality.
- Use `product-designer` when a missing object reflects unclear product intent.
- Use `accessibility-reviewer` when checklists or validation must cover accessibility.
