---
name: specforge-decisions-dsl
description: "Write decision (ADR) blocks in .spec files (the decision kind is declared by the builtin @specforge/governance extension). Each decision records a significant choice with a snake_case ID, a status lifecycle, context/decision/consequences, alternatives, deciders, and links to the invariants it protects, the constraints it imposes and the features it affects. Use when documenting why something is done a certain way -- an architecture choice, a process rule, a policy."
---

# SpecForge Decisions DSL

> **Declared by `@specforge/governance`**, a builtin extension. The `decision` kind exists only in a project that
> loads it: run `specforge extensions` first, and if it is not listed, do not write `decision` blocks (add it with
> `specforge add @specforge/governance`, or write the kinds the project's own extensions declare).
> `specforge infer-guide decision` prints the fields.

Decisions capture the *why* behind choices that would be expensive to reverse.

## Block Syntax

```spec
decision postgres_over_mongodb "PostgreSQL over MongoDB" {
  status   accepted
  date     2025-03-01
  deciders ["CTO", "Lead backend engineer"]

  context """
    We need a primary datastore. The team has SQL expertise.
    The data is relational; a document model is not needed.
  """

  decision "Use PostgreSQL with typed schemas."

  consequences [
    "Migrations required for schema changes",
    "Strong ACID guarantees",
  ]

  alternatives ["MongoDB", "DynamoDB"]
  invariants   [data_persistence]
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum (required) `proposed` `accepted` `deprecated` `superseded` | Lifecycle. |
| `context` | string (required) | What prompted the decision. |
| `decision` | string (required) | What was chosen. |
| `consequences` | string list | Outcomes and trade-offs, good and bad. |
| `alternatives` | string list | Options considered. |
| `reason` | string | Why this option over the alternatives. |
| `date` | date | A bare calendar day, `2026-03-01` (another value is E061). |
| `authors` / `deciders` | string list | Who wrote it / who signed off. |
| `superseded_by` | reference -> decision | The decision that replaces this one. |
| `invariants` | reference list -> invariant | Invariants it protects. |
| `constraints` | reference list -> constraint | Constraints it imposes. |
| `affects_features` | reference list -> feature | Features it affects (needs `@specforge/product`). |
| `description` | string | Summary. |
| `tags` | string list | Labels. |
| `refs` | string list | Declared `ref` IDs. |

## Writing Rules

1. **Context explains the forces** -- the problem, constraints and trade-offs.
2. **Decision is the choice** -- the rationale lives in context, consequences and `reason`.
3. **Consequences include negatives.**
4. **Supersede, do not delete** -- set `status superseded` and `superseded_by` to the new decision.

## Validation Rules

`@specforge/governance` declares no validation rules of its own; the core checks apply.

| Code | Owner | Rule |
|------|-------|------|
| E006 | core | `status`, `context` or `decision` is missing. |
| E061 | core | `status` outside its enum, or `date` not a calendar day. |
| E003 / E022 | core | A reference names nothing, or an entity of another kind. |

## Examples

### Architectural Pattern

```spec
decision event_sourcing_for_audit "Event Sourcing for Audit Trail" {
  status accepted
  date   2025-06-15

  context """
    Regulatory requirements demand a complete, immutable audit trail.
    An update-in-place model would need separate audit logging
    that can drift from the data.
  """

  decision """
    Use event sourcing for the billing domain.
    Store every state change in an append-only event log.
  """

  consequences [
    "Complete audit trail by construction",
    "Event replay enables point-in-time recovery",
    "Increased storage requirements",
  ]

  invariants [audit_trail_integrity]
}
```

### Proposed, Outside Software

```spec
decision two_person_release_signoff "Two-Person Sign-off for Batch Release" {
  status proposed
  date   2026-02-15

  context "A single reviewer released a batch with an unrecorded deviation last quarter."

  decision "Every batch release needs the signatures of two qualified persons."

  consequences [
    "Release takes longer on night shifts",
    "Each release has an independent second check",
  ]
}
```

### Superseded

```spec
decision rest_for_internal_calls "REST for Internal Service Calls" {
  status        superseded
  superseded_by grpc_for_internal_calls
  context       "Internal services needed a shared protocol."
  decision      "Use REST/JSON between internal services."
}

decision grpc_for_internal_calls "gRPC for Internal Service Calls" {
  status   accepted
  context  "Serialization overhead of REST/JSON is measurable at current scale."
  decision "Use gRPC with Protocol Buffers between internal services."
}
```

## What NOT to Do

- Do not write ADRs for trivial, easily reversible choices
- Do not omit consequences, especially the negative ones
- Do not quote the date -- write it bare (`2026-02-15`)
