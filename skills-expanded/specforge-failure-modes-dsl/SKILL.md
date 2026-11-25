---
name: specforge-failure-modes-dsl
description: "Write failure_mode blocks in .spec files (the failure_mode kind is declared by the builtin @specforge/governance extension). Each failure_mode is an FMEA entry with a snake_case ID, a cause and an effect, severity/occurrence/detection ratings before and after mitigation, a mitigation, and links to the invariant it threatens, the behaviors it affects and the features it threatens. Use when analysing what can go wrong and how bad it would be, in software or in a regulated process."
---

# SpecForge Failure Modes DSL

> **Declared by `@specforge/governance`**, a builtin extension. The `failure_mode` kind exists only in a project that
> loads it: run `specforge extensions` first, and if it is not listed, do not write `failure_mode` blocks (add it with
> `specforge add @specforge/governance`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`. `specforge infer-guide failure_mode` prints the fields.

Failure modes are FMEA (Failure Mode and Effects Analysis) entries: one way something can break, how bad it is, and
what is done about it.

## Block Syntax

```spec
failure_mode write_acknowledged_but_lost "Write Acknowledged but Lost" {
  invariant  data_persistence
  severity   high
  occurrence unlikely
  detection  moderate

  cause      "Crash between ACK and fsync"
  effect     "Silent data loss -- the user believes the write succeeded"
  mitigation "Write-ahead log with fsync before ACK"

  post_severity   high
  post_occurrence rare
  post_detection  likely

  verify integration "a crash injected after ACK loses no acknowledged write"
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `severity` | enum (required) `critical` `high` `medium` `low` | Impact before mitigation. |
| `cause` | string (required) | Root cause or trigger. |
| `effect` | string (required) | What happens when it occurs. |
| `occurrence` | enum `certain` `likely` `occasional` `unlikely` `rare` | Likelihood before mitigation. |
| `detection` | enum `certain` `likely` `moderate` `unlikely` `undetectable` | Likelihood of catching it before harm. |
| `mitigation` | string | What reduces the risk. |
| `post_severity` / `post_occurrence` / `post_detection` | the same enums | Ratings after mitigation. |
| `post_mitigation` | block | Residual risk written as a block, if you prefer it to the `post_*` fields. |
| `rpn` | integer | Risk Priority Number, if your method computes one. |
| `risk` | string | Overall risk assessment in words. |
| `invariant` | reference -> invariant | The invariant it threatens. |
| `affected_behaviors` | reference list -> behavior | Behaviors that are failure vectors. |
| `threatens_features` | reference list -> feature | Features it threatens (needs `@specforge/product`). |
| `description` | string | Summary. |
| `refs` | string list | Declared `ref` IDs. |

The ratings are words, not 1-10 numbers: a number in `severity`, `occurrence` or `detection` is E061. No check
recomputes `rpn`.

### Verify kinds

With `@specforge/testing`: `unit`, `integration`, `property` (another kind is W009).

## Writing Rules

1. **One failure mode per way of breaking.**
2. **Cause -> effect -> mitigation** -- tell the whole story.
3. **Reassess after mitigation** -- severity rarely changes; occurrence and detection should improve.

## Validation Rules

`@specforge/governance` declares no validation rules of its own; the core and testing checks apply.

| Code | Owner | Rule |
|------|-------|------|
| E006 | core | `severity`, `cause` or `effect` is missing. |
| E061 | core | A rating outside its enum (a number, for instance). |
| E003 / E022 | core | A reference names nothing, or an entity of another kind. |
| W009 | testing | A `verify` kind outside the allowed set. |

## Examples

### Security

```spec
failure_mode email_uniqueness_bypass "Email Uniqueness Bypass via Race Condition" {
  invariant          email_uniqueness
  affected_behaviors [create_user]
  severity           medium
  occurrence         occasional
  detection          unlikely

  cause      "Two concurrent requests create users with the same email"
  effect     "Two active users share an email -- login is ambiguous"
  mitigation "Database UNIQUE constraint plus serializable isolation"

  post_occurrence rare
  post_detection  certain
}
```

### Regulated Process (pharma)

```spec
failure_mode unrecorded_deviation "Deviation Not Recorded in the Batch Record" {
  severity   critical
  occurrence occasional
  detection  unlikely

  cause      "An operator corrects a step on paper and does not open a deviation"
  effect     "A batch is released with an undocumented departure from procedure"
  mitigation "Electronic batch record blocks step sign-off until any correction has a deviation ID"

  post_occurrence rare
  post_detection  likely
}
```

## What NOT to Do

- Do not rate with numbers (`severity 8` is E061) -- use the declared words
- Do not change `post_severity` without a reason -- the impact is usually inherent
- Do not skip the after-mitigation ratings -- they show what the mitigation buys
