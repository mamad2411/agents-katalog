---
name: specforge-features-dsl
description: "Write feature blocks in .spec files (the feature kind is declared by the builtin @specforge/product extension). Each feature declares a user-facing capability with a snake_case ID, problem/solution framing, acceptance criteria, status, priority, owner and effort; the behaviors that implement it name it in their `features` field. Features take no verify statements. Use when grouping work into coherent units of value for product planning, in software or any other product."
---

# SpecForge Features DSL

> **Declared by `@specforge/product`**, a builtin extension. The `feature` kind exists only in a project that loads
> it: run `specforge extensions` first, and if it is not listed, do not write `feature` blocks (add it with
> `specforge add @specforge/product`, or write the kinds the project's own extensions declare).
> `specforge infer-guide feature` prints the fields.

Features bridge what users need (problem) and how it is delivered (solution). In a software project, behaviors (from
`@specforge/software`) name the features they implement in their own `features` field.

Features take no `verify` statements (W158): proof happens on the behaviors that implement them.

Typed edit: `specforge new feature <id> "<title>" --in spec/<file>.spec --problem "…"`.

## Block Syntax

```spec
feature user_management "User Management" {
  status   accepted
  priority high
  owner    "identity-team"
  effort   m

  problem """
    Administrators need to manage user accounts
    with guaranteed data integrity.
  """

  solution """
    Create, read, update and delete operations backed by a relational store,
    with unique email constraints and a full audit trail.
  """

  acceptance [
    "An admin can create, edit and deactivate a user",
    "A duplicate email is refused with a clear message",
  ]
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `problem` | string (required) | The user problem, from the user's perspective. |
| `solution` | string | How the feature solves it. |
| `description` | string | Human-readable summary. |
| `acceptance` | string list | Criteria that make the feature complete. Missing: I048. |
| `status` | enum `proposed` `accepted` `in_progress` `done` `deferred` `deprecated` | Lifecycle state; absent means `proposed`. |
| `priority` | enum `critical` `high` `medium` `low` | Importance. |
| `effort` | enum `xs` `s` `m` `l` `xl` | T-shirt estimate. Missing: I081. |
| `owner` | string | Person or team responsible. Missing: I080. |
| `contributors` | string list | Others contributing. |
| `reason` | string | Why the status is what it is (a `deferred` feature without one is I059). |
| `depends_on` | reference list -> feature | Features that must be done first (a cycle is W045). |
| `features` | reference list -> feature | Related features. |
| `tests` | string list | Test files that verify this feature, relative to the project root. |
| `refs` | string list | Declared `ref` IDs. |
| `tags` | string list | Lowercase-hyphenated labels (shared by every product kind; otherwise I068). |

## Relationships

A feature lists no behaviors, journeys, modules or milestones: each of those names the feature in its own field, and
`specforge trace <feature>` lists them. Writing a `behaviors` field on a feature is E079.

| From | Field on the other entity | Declared by |
|------|---------------------------|-------------|
| behavior | `features` | software |
| journey | `features` | product |
| module | `features` | product |
| milestone | `features` | product |
| persona | `key_features` | product |
| decision | `affects_features` | governance |
| constraint | `governs_features` | governance |
| failure_mode | `threatens_features` | governance |

## Writing Rules

1. **Problem is user-perspective** -- describe the pain point, not the solution.
2. **Solution is delivery-perspective** -- describe the approach at a high level.
3. **Write the relation on the other side** -- a behavior lists the features it implements; a feature never lists behaviors.
4. **Add `acceptance`** -- testable completion criteria.
5. **Features go on roadmaps, behaviors go in test suites** -- keep the distinction clear.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E006 | core | `problem` is missing. |
| E061 | core | `status`, `priority` or `effort` outside its enum. |
| E079 | core | A `behaviors` (or other inverse) field written on the feature. |
| W041 | product | No journey, milestone or module references the feature. |
| W045 | product | `depends_on` cycle. |
| W008 | software | No behavior implements the feature (with `@specforge/software`). |
| I048 / I080 / I081 | product | No acceptance criteria / no owner / no effort. |
| I059 | product | `deferred` without `reason`. |
| I063 | product | `done` while a `depends_on` feature is not done. |
| I071 | product | `done` but the recorded test report does not prove it. |

## Examples

### Software Feature

```spec
feature password_authentication "Password Authentication" {
  status   in_progress
  priority critical

  problem """
    Users need to securely authenticate to access their accounts.
    The system must prevent unauthorized access while keeping
    the login experience fast and simple.
  """

  solution """
    Password-based authentication with bcrypt hashing,
    rate-limited login attempts, and secure session tokens.
  """
}
```

### Feature with Dependencies and Refs

```spec
ref gh.issue:88 "Search is too slow for large datasets"

feature full_text_search "Full-Text Search" {
  priority   high
  depends_on [user_management]
  refs       [gh.issue:88]

  problem """
    Users with large datasets cannot find specific records quickly.
    Filtering by exact field match is insufficient for
    free-form queries across multiple fields.
  """

  solution """
    Full-text search with typo tolerance, field weighting, and faceted
    filtering. Results ranked by relevance with matched terms highlighted.
  """
}
```

### Cross-Domain Feature

```spec
feature order_checkout "Order Checkout" {
  problem """
    Customers need to complete purchases with confidence that
    their order will be fulfilled, their payment processed correctly,
    and inventory accurately reserved.
  """

  solution """
    Orchestrated checkout flow: validate inventory, reserve items,
    process payment via Stripe, create order record. Compensating
    transactions on failure release reserved inventory.
  """
}
```

### Outside Software (a marketing launch)

```spec
feature spring_campaign_landing "Spring Campaign Landing Page" {
  status   accepted
  priority high
  owner    "growth-team"
  tags     ["campaign", "q2"]

  problem "Visitors from the spring ads land on a generic page and leave."

  acceptance [
    "The page matches the ad's headline and offer",
    "The sign-up form converts at 4% or better",
  ]
}
```

## What NOT to Do

- Do not write a `behaviors` field on a feature (E079): the behaviors name the feature in their `features`
- Do not put MUST/SHOULD keywords in the problem/solution -- save those for behavior contracts
- Do not put implementation details in the `problem` field -- it should be user-perspective
- Do not add `verify` statements -- the feature kind accepts none (W158)
