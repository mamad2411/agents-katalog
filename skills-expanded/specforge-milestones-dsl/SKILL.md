---
name: specforge-milestones-dsl
description: "Write milestone blocks in .spec files (the milestone kind is declared by the builtin @specforge/product extension). Each milestone declares a planning phase with a snake_case ID, a status lifecycle, the features it must deliver, exit criteria, dates, blockers and dependencies on other milestones. Use when defining when things ship and what must be true before a phase is complete, for any kind of project."
---

# SpecForge Milestones DSL

> **Declared by `@specforge/product`**, a builtin extension. The `milestone` kind exists only in a project that loads
> it: run `specforge extensions` first, and if it is not listed, do not write `milestone` blocks (add it with
> `specforge add @specforge/product`, or write the kinds the project's own extensions declare).
> `specforge infer-guide milestone` prints the fields.

Milestones give the plan its time dimension, with exit criteria that say when a phase is done.

## Block Syntax

```spec
milestone mvp "Phase 1: Core" {
  status        in_progress
  owner         "product-team"
  features      [user_management, password_authentication]
  start_date    2026-04-01
  target_date   2026-06-30
  exit_criteria [
    "Every MVP feature is done",
    "specforge check --strict passes",
  ]
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum `planned` `in_progress` `completed` `blocked` | Lifecycle; absent means `planned`. |
| `features` | reference list -> feature | Features this phase must deliver. Missing: W049. |
| `modules` | reference list -> module | Modules scoped to this phase. |
| `depends_on` | reference list -> milestone | Phases that must complete first (a cycle is E015). |
| `exit_criteria` | string list | How completion is verified (a `completed` milestone without them is W057). |
| `start_date` / `target_date` | date | A bare calendar day, `2026-06-30` (another value is E061). |
| `blockers` | string list | What blocks progress (a `blocked` milestone without them is I060). |
| `priority` | enum `critical` `high` `medium` `low` | Importance. |
| `owner` | string | Person or team responsible (otherwise I080). |
| `contributors` | string list | Others contributing. |
| `reason` | string | Why the status is what it is. |
| `description` | string | Summary. |
| `refs` | string list | Declared `ref` IDs. |
| `tags` | string list | Lowercase-hyphenated labels. |

With `@specforge/software` loaded, a milestone also takes `behaviors` (reference list -> behavior).

## Relationships

| Field | Target |
|-------|--------|
| `features` | feature |
| `modules` | module |
| `depends_on` | milestone |
| `behaviors` | behavior (software) |
| a deliverable's `milestones`, a release's `milestones` | this milestone |

## Writing Rules

1. **Verifiable criteria** -- "specforge check --strict passes", "coverage >= 90%", not vague goals.
2. **Progressive phases** -- each phase builds on the previous ones through `depends_on`.
3. **A blocked milestone says why** -- `blockers`, plus `depends_on` when it waits for another phase.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E061 | core | `status`, `priority` or a date outside its form. |
| E015 | product | `depends_on` cycle. |
| W049 | product | No `features`. |
| W057 | product | `completed` without `exit_criteria`. |
| W154 | product | `completed` while a feature it names is not done or deprecated. |
| I057 | product | `blocked` without `depends_on`. |
| I060 | product | `blocked` without `blockers`. |
| I064 | product | Due before a milestone it depends on. |
| I080 | product | No `owner`. |

## Examples

### Planned Phase

```spec
milestone search_analytics "Search and Analytics" {
  status        planned
  owner         "search-team"
  depends_on    [mvp]
  features      [full_text_search]
  target_date   2026-09-30

  exit_criteria [
    "Full-text search returns results in < 200ms",
    "The analytics dashboard renders within 3 seconds",
  ]
}
```

### Blocked Phase

```spec
milestone external_integration "External Integration" {
  status     blocked
  owner      "platform-team"
  depends_on [mvp]
  features   [third_party_sync]
  blockers   ["Partner API credentials not issued yet"]
  reason     "Waiting on the partner's security review"
}
```

## What NOT to Do

- Do not set vague criteria like "the system is ready" -- use measurable, automatable checks
- Do not use status values outside the enum (`active`, `done` are E061)
- Do not quote dates -- write them bare (`2026-06-30`)
