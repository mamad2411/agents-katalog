---
name: specforge-terms-dsl
description: "Write term blocks in .spec files (the term kind is declared by the builtin @specforge/product extension). Each term declares a glossary entry as its own entity, with a snake_case ID, a definition, usage context, aliases, related terms and the module that owns it. Use when establishing precise vocabulary for any domain -- software, pharma, marketing, operations -- to prevent terminology drift."
---

# SpecForge Terms DSL

> **Declared by `@specforge/product`**, a builtin extension. The `term` kind exists only in a project that loads it:
> run `specforge extensions` first, and if it is not listed, do not write `term` blocks (add it with
> `specforge add @specforge/product`, or write the kinds the project's own extensions declare).
> `specforge infer-guide term` prints the fields.

Terms establish the shared language: precise definitions that two readers agree on.

## Block Syntax

```spec
term committed_write "committed write" {
  definition """
    A write operation that has been acknowledged to the caller
    AND durably persisted to the primary datastore.
  """
  context  "Used in persistence guarantees and incident reports"
  aliases  ["persisted mutation", "durable write"]
  see_also [eventual_consistency]
}

term eventual_consistency "eventual consistency" {
  definition """
    A consistency model where reads may return stale data
    for a bounded period after a write.
  """
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `definition` | string (required) | The precise meaning in this project. |
| `context` | string | Where or how the term is used. |
| `aliases` | string list | Other names for the same thing. |
| `see_also` | reference list -> term | Related **terms** (another kind is E022). |
| `module` | reference -> module | The module (bounded context) that owns the definition. |
| `tags` | string list | Lowercase-hyphenated labels. |

## Writing Rules

1. **One entity per term** -- derive the ID from the term ("committed write" -> `committed_write`).
2. **Add a term when meaning is ambiguous** -- if two people might read a word differently, define it.
3. **Definitions are self-contained.**
4. **Link it** -- a term with no edges (no `see_also`, no `module`, nothing pointing at it) is I010.
5. **Link one way** -- two terms naming each other in `see_also` is a reference cycle (W061).
6. **Skip obvious words** -- "function", "database", "email" need no entry.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E006 | core | `definition` is missing. |
| E022 | core | `see_also` names an entity that is not a term, or `module` one that is not a module. |
| I010 | product | The term has no edges. |

## Examples

### Regulated Domain (pharma)

```spec
term batch_record "batch record" {
  definition """
    The complete, signed record of how one batch of product was made,
    tested and released.
  """
  aliases  ["BMR", "batch manufacturing record"]
  see_also [deviation]
}

term deviation "deviation" {
  definition "Any departure from an approved procedure or specification."
}
```

### Owned by a Module

```spec
term result_type "Result type" {
  definition """
    A type that represents either success or failure with typed errors.
    Every port method returns one instead of throwing.
  """
  aliases ["Result monad"]
  module  core_mod
}
```

## What NOT to Do

- Do not point `see_also` at behaviors, invariants or other non-term entities -- it takes terms only (E022)
- Do not write `refs` on a term -- the kind does not declare it (W020)
- Do not add standard terms that need no clarification
