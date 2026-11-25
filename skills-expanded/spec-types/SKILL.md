---
name: spec-types
description: "Author domain type specification files in a spec's types/ directory. Each file documents types for a domain with field tables, immutability annotations, discriminant fields, and behavior cross-references. Use when creating type specifications, auditing type completeness, or documenting domain types."
---

# Spec Types

Rules and conventions for authoring **domain type specification files** in a spec's `types/` directory. Distinct from `type-system/` which covers compile-time safety patterns.

## When to Use

- Creating type specifications for domain types
- Auditing type files for completeness (missing immutability annotations, missing discriminant fields)
- Documenting new domain types
- Checking for duplicate type definitions across files

## Directory Structure

```
types/
  index.yaml                    # Manifest of all type files
  <domain>.md                   # One file per domain
```

### index.yaml Schema

```yaml
kind: types
package: "@myproject/<name>"
entries:
  - id: TYPE-001
    file: graph.md
    title: Graph Types
    status: active              # active | draft | deprecated
    domain: graph
  - id: TYPE-002
    file: errors.md
    title: Error Types
    status: active
    domain: errors
```

**Rules:**
- Every `.md` file in `types/` MUST have a corresponding entry
- Every entry MUST have a corresponding file on disk
- No duplicate `id` values across entries
- One file per domain, not one file per type

## File Naming

- Kebab-case domain name: `graph.md`, `agent.md`, `flow.md`, `errors.md`, `ports.md`
- One file per domain, not one file per type

## File Template

```markdown
---
id: TYPE-NNN
kind: types
title: "<Domain> Types"
status: active
behaviors: [BEH-XX-NNN]
adrs: []
---

# <Domain> Types

Type definitions for the <domain> domain.

---

## <TypeName>

| Field | Type | Mutability | Constraints | Description |
|-------|------|------------|-------------|-------------|
| field_a | String | immutable | required | <purpose> |
| field_b | Integer | mutable | optional, >= 0 | <purpose> |

<Prose explaining the type's purpose, constraints, and usage context.>

---
```

### Discriminated Unions

For types that use a discriminant field to distinguish variants:

```markdown
## <UnionTypeName>

**Discriminant field:** `kind`

| Variant | Discriminant Value | Additional Fields |
|---------|-------------------|-------------------|
| VariantA | `"variant_a"` | `payload: String` |
| VariantB | `"variant_b"` | `count: Integer` |
```

## Content Rules

1. **YAML frontmatter** — Every types file MUST start with `---` frontmatter containing `id`, `kind: types`, `title`, `status`, `behaviors`, `adrs`. The `**Source behaviors:**` line is REMOVED from prose — that metadata lives in frontmatter.
2. **Immutability annotations** — All fields should declare mutability (immutable/mutable) in the field table.
3. **Unique discriminant values** — All discriminated union types have unique discriminant values per variant.
4. **Behavior cross-references** — Cross-reference behavior files that use these types.
5. **No duplicates** — No duplicate type definitions across `types/` files.
6. **Errors file** — `types/errors.md` collects all error types with their discriminant values.

## Cross-References

```markdown
# From types to behaviors:
**Source behaviors:** [BEH-XX-001-graph-ops.md](../behaviors/BEH-XX-001-graph-ops.md)

# From behaviors to types (in header):
**Types:** [types/graph.md](../types/graph.md)

# From architecture to types:
See [types/graph.md](../types/graph.md)
```
