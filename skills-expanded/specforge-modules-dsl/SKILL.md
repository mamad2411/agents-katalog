---
name: specforge-modules-dsl
description: "Write module blocks in .spec files (the module kind is declared by the builtin @specforge/product extension). Each module declares a structural component -- a package, a subsystem, a workstream or a program area -- with a snake_case ID, a family, the features it contains and a dependency graph between modules. Use when making explicit which component delivers which features, in software or any other organisation."
---

# SpecForge Modules DSL

> **Declared by `@specforge/product`**, a builtin extension. The `module` kind exists only in a project that loads
> it: run `specforge extensions` first, and if it is not listed, do not write `module` blocks (add it with
> `specforge add @specforge/product`, or write the kinds the project's own extensions declare).
> `specforge infer-guide module` prints the fields.

Modules group features into components and form a dependency graph the checks keep acyclic.

## Block Syntax

```spec
module core_mod "@myservice/core" {
  family      core
  features    [user_management, password_authentication]
  depends_on  [crypto_mod]
  description "Core domain logic and user management"
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `features` | reference list -> feature | Features the module contains. Missing or empty: I067. |
| `depends_on` | reference list -> module | Modules this one depends on (a cycle is E007). |
| `family` | identifier | Grouping: `core`, `platform`, `extension`, `integration`, `advisory`, `workstream` are suggestions; any word is accepted. |
| `description` | string | Purpose. |
| `reason` | string | Why the module exists or is grouped this way. |
| `tags` | string list | Lowercase-hyphenated labels. |

With `@specforge/software` loaded, a module also takes `ports` (ports it consumes) and `ports_defined` (ports it
defines), both reference lists -> port.

## Relationships

| Field | Target |
|-------|--------|
| `features` | feature |
| `depends_on` | module |
| a deliverable's or milestone's `modules`, a term's `module` | this module |

## Writing Rules

1. **Maps to a structural component** -- a package, subsystem, workstream or program area.
2. **`depends_on` forms a DAG** -- a cycle is E007.
3. **Reference it** -- a module no deliverable or milestone names is W044.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E007 | product | `depends_on` cycle. |
| W044 | product | No deliverable or milestone references the module. |
| I067 | product | No `features`. |

## Examples

### Hardware Subsystem

```spec
module power_subsystem "Power Distribution Unit" {
  family      platform
  features    [power_regulation, thermal_protection]
  depends_on  [sensor_array]
  description "Manages power distribution and voltage regulation across all subsystems"
}
```

### Consulting Workstream

```spec
module market_analysis "Market Analysis Workstream" {
  family      advisory
  features    [competitive_landscape, market_sizing]
  description "Research and analysis of target market segments"
}
```

### Minimal Module

```spec
module search_mod "@myservice/search" {
  features [full_text_search]
}
```

## What NOT to Do

- Do not write `refs` on a module -- the kind does not declare it (W020)
- Do not create circular dependencies between modules (E007)
- Do not confuse modules (structural components) with deliverables (shippable artifacts)
