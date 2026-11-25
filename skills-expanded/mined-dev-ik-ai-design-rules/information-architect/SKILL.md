---
name: information-architect
description: Shape product object models, navigation, hierarchy, labels, and status language. Use before screen layout when users, content relationships, wayfinding, or information structure are unclear.
---

# Information Architect Skill

## Role

Define product objects, navigation structure, labels, hierarchy, and view relationships.

## Mission

Make the product understandable by grounding screens in a stable object model and clear information architecture.

## When To Use

- A product has multiple object types, views, modes, lists, or filters.
- A screen feels like unrelated panels instead of a coherent product surface.
- Navigation labels, object names, or status concepts are unclear.
- A reference project needs its domain model clarified.

## When Not To Use

- The task is only mobile reachability or visual polish.
- The product goal is still unknown.
- The request is to create a component API.

## Inputs

- Product goal and user tasks.
- Existing data model, screens, routes, navigation, and labels.
- Rules and patterns related to IA and status.
- Known permissions, privacy, ownership, and shared visibility constraints.

## Process

1. Name the core product objects.
2. Define object relationships and ownership.
3. Identify the stable home surface.
4. Separate views from duplicated data.
5. Define status, priority, ownership, and grouping language.
6. Check whether patterns depend on a clear object model.
7. Flag ambiguous labels or hidden hierarchy.
8. Hand off interaction, visual, or product gaps.

## Output Format

```md
## IA Model
- Core objects:
- Relationships:
- Home surface:
- Views:

## Navigation And Labels
- Primary sections:
- Status language:
- Ambiguous terms:

## Applied Rules And Patterns
- Rule:
- Pattern:

## Handoff
- Next skill:
- Reason:
```

## Quality Checklist

- Core objects are named before screens.
- Views do not duplicate underlying data.
- Home surface is stable.
- Status and ownership labels are concrete.
- Navigation supports return speed.
- IA choices cite existing rules or patterns.

## Related Rules

- `RULE-00003` / `IA-001` One Stable Home Surface
- `RULE-00004` / `IA-002` Define The Object Model Before Screens
- `RULE-00007` / `UX-003` Preserve Context During Inspection
- `RULE-00008` / `VIS-001` Semantic Tokens Only

## Related Patterns

- `PAT-00001` / `PAT-001` Daily Home Surface
- `PAT-00005` / `PAT-005` Context-Preserving Preview
- `PAT-00006` / `PAT-006` Object Status List

## Handoff To Other Skills

- Use `product-designer` if the product object is not tied to a user goal.
- Use `interaction-designer` to define movement between objects and views.
- Use `design-system-architect` to normalize status and semantic token naming.
- Use `design-reviewer` to validate traceability.
