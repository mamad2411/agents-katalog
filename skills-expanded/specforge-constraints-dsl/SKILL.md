---
name: specforge-constraints-dsl
description: "Write constraint blocks in .spec files (the constraint kind is declared by the builtin @specforge/governance extension). Each constraint declares a measurable limit or requirement -- performance, security, regulatory, compatibility -- with a snake_case ID, a description, a category, a priority (critical/high/medium/low), a metric and threshold, and links to the behaviors it constrains, the invariants it protects and the features it governs. Use when defining quality attributes or rules with thresholds."
---

# SpecForge Constraints DSL

> **Declared by `@specforge/governance`**, a builtin extension. The `constraint` kind exists only in a project that
> loads it: run `specforge extensions` first, and if it is not listed, do not write `constraint` blocks (add it with
> `specforge add @specforge/governance`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`. `specforge infer-guide constraint` prints the fields.

Constraints declare quantified limits: a metric, a threshold, and what they apply to. For rules about state that are
either kept or broken, use an invariant instead.

## Block Syntax

```spec
constraint api_latency_under_load "API Latency Under Load" {
  description "The user API stays fast under peak load."
  category    performance
  priority    critical
  metric      "response time p99"
  threshold   "< 200ms at 1000 concurrent users for 5 minutes"
  constrains  [create_user, read_user_by_id]

  verify load "a k6 run with 1000 virtual users keeps p99 under 200ms"
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `description` | string (required) | The requirement in words. |
| `category` | identifier | e.g. `performance`, `security`, `regulatory`, `compatibility`, `reliability`. |
| `priority` | enum `critical` `high` `medium` `low` | Importance. |
| `metric` | string | The measured quantity. |
| `threshold` | string | The acceptable limit. |
| `scope` | string | Where it applies (system-wide, per module, per request). |
| `constrains` | reference list -> behavior | Behaviors it limits (needs `@specforge/software`). |
| `enforced_by` | reference list -> behavior | Behaviors that enforce it at runtime. |
| `protects` | reference list -> invariant | Invariants it helps protect. |
| `governs_features` | reference list -> feature | Features it governs (needs `@specforge/product`). |
| `refs` | string list | Declared `ref` IDs. |

### Verify kinds

With `@specforge/testing`: `unit`, `integration`, `property`, `load`, `contract` (another kind is W009).

## Writing Rules

1. **Measurable** -- "p99 < 200ms", not "the system is fast".
2. **Scope it** -- name the behaviors or features it applies to.
3. **Add `verify`** -- describe how a test shows the threshold holds.

## Validation Rules

`@specforge/governance` declares no validation rules of its own; the core and testing checks apply.

| Code | Owner | Rule |
|------|-------|------|
| E006 | core | `description` is missing. |
| E061 | core | `priority` outside its enum. |
| E003 / E022 | core | A reference names nothing, or an entity of another kind. |
| W009 | testing | A `verify` kind outside the allowed set. |

## Examples

### Security

```spec
constraint pii_encryption_at_rest "PII Encryption at Rest" {
  description "Every personal data field is encrypted at rest."
  category    security
  priority    critical
  threshold   "AES-256 for every PII column"
  protects    [pii_encryption]
  constrains  [create_user, update_user_email]

  verify integration "a database column inspection finds no plaintext PII"
}
```

### Regulatory

```spec
constraint gdpr_data_residency "GDPR Data Residency" {
  description "EU user data stays in the EU."
  category    regulatory
  priority    critical
  scope       "all stores holding EU personal data"
  threshold   "0 replicas of EU personal data outside eu-west-1"
  protects    [data_residency]
}
```

### Compatibility

```spec
constraint runtime_compatibility "Runtime Compatibility" {
  description "The CLI runs on Node.js 18+, Bun 1.0+ and Deno 2.0+."
  category    compatibility
  priority    high

  verify integration "the CI matrix passes on every supported runtime"
}
```

## What NOT to Do

- Do not use `must`/`should`/`may` as a priority -- the enum is `critical`, `high`, `medium`, `low` (E061)
- Do not write `affects`, `behaviors` or `invariants` -- the fields are `constrains`, `enforced_by` and `protects` (W020)
- Do not confuse constraints (graduated, measured) with invariants (kept or broken)
- Do not use vague metrics -- "fast", "secure", "reliable" are not measurable
