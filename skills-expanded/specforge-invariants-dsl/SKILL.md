---
name: specforge-invariants-dsl
description: "Write invariant blocks in .spec files (the invariant kind is declared by the builtin @specforge/governance extension). Each invariant declares a rule that must always hold, with a snake_case ID, a guarantee statement using RFC 2119 keywords, a risk level (critical/high/medium/low), verify obligations (with @specforge/testing) and an optional machine-checkable expression (with @specforge/formal). Use when defining what must ALWAYS be true."
---

# SpecForge Invariants DSL

> **Declared by `@specforge/governance`**, a builtin extension. The `invariant` kind exists only in a project that loads
> it: run `specforge extensions` first, and if it is not listed, do not write `invariant` blocks (add it with
> `specforge add @specforge/governance`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`; `expression` needs `@specforge/formal`. `specforge infer-guide invariant` prints the fields.

Invariants declare non-negotiable guarantees. Behaviors name the invariants they enforce; decisions, constraints and
failure modes (from `@specforge/governance`) point at the invariants they protect or threaten.

Typed edit: `specforge new invariant <id> "<title>" --in spec/<file>.spec --guarantee "…" --risk high`.

## Block Syntax

```spec
invariant data_persistence "Data Persistence" {
  guarantee """
    All committed writes MUST survive process restarts.
    No acknowledged write may be silently dropped.
  """
  risk high

  verify property "committed writes survive a simulated crash"
  verify unit     "WAL replay restores all entries"
}
```

## Fields Reference

| Field | Type | Declared by | Description |
|-------|------|-------------|-------------|
| `guarantee` | string (required) | software | What must always hold. |
| `risk` | enum `critical` `high` `medium` `low` | software | Impact if violated. |
| `description` | string | software | Human-readable summary. |
| `refs` | string list | software | Declared `ref` IDs (`gh.issue:15`). |
| `expression` | string | formal | Machine-checkable claim `specforge analyze --prove` must entail; without it, W040. |

### Verify kinds

With `@specforge/testing`: `unit`, `integration`, `property`, `performance`, `mutation` (another kind is W009).

## Relationships

An invariant lists no behaviors: the behaviors that enforce it name it in their `invariants` field (an `enforced_by`
list on the invariant is E079), and `specforge trace <invariant>` lists them.

| From | Field on the other entity | Declared by |
|------|---------------------------|-------------|
| behavior | `invariants` | software |
| decision | `invariants` | governance |
| constraint | `protects` | governance |
| failure_mode | `invariant` | governance |
| axiom | `assumes` | formal |

## Writing Rules

1. **One guarantee per invariant** -- do not combine unrelated guarantees.
2. **Falsifiable** -- a test must be able to detect a violation.
3. **Universal** -- it holds under all conditions, not just the happy path.
4. **Implementation-independent** -- describe what is true, not how it is achieved.
5. **Reference it from a behavior** -- an invariant no behavior enforces is W003.
6. **Add `verify`** -- or W004 fires (with `@specforge/testing`).

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E002 | core | Two invariants share an ID. |
| E006 | core | `guarantee` is missing. |
| E061 | core | `risk` outside its enum. |
| W003 | governance | Nothing references the invariant. |
| W004 | testing | No `verify` obligation. |
| W040 | formal | No `expression` (reported by `specforge analyze`). |

## Examples

### Simple

```spec
invariant email_uniqueness "Email Uniqueness" {
  guarantee "No two active users share the same email address."
  risk      medium

  verify property "concurrent user creation preserves email uniqueness"
}
```

### Critical, with an expression (needs `@specforge/formal`)

```spec
invariant audit_trail_integrity "Audit Trail Integrity" {
  guarantee """
    The audit log is append-only.
    No audit entry may be modified or deleted after creation.
    Every state-changing operation MUST produce an audit entry
    before returning success to the caller.
  """
  risk       critical
  expression "audit_entries_after >= audit_entries_before"

  verify property "the audit log is append-only under concurrent writes"
  verify unit     "a state-changing operation produces an audit entry"
  verify mutation "tampering with an audit entry is detected"
}
```

### Low-Risk

```spec
invariant display_name_length "Display Name Length" {
  guarantee "User display names MUST be between 1 and 100 characters."
  risk      low

  verify unit "names within bounds are accepted"
  verify unit "names outside bounds are rejected"
}
```

## What NOT to Do

- Do not use an invariant for something that is a behavior ("Users can log in" is a behavior)
- Do not use an invariant for a technology choice ("We use PostgreSQL" is a decision)
- Do not use an invariant for a quantified limit ("p99 < 200ms" is a constraint)
- Do not write a `maintains` block on an invariant -- `maintains` is a behavior field (formal)
