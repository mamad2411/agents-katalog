---
name: specforge-deliverables-dsl
description: "Write deliverable blocks in .spec files (the deliverable kind is declared by the builtin @specforge/product extension). Each deliverable declares a shippable artifact with a snake_case ID, an artifact type, a status, the journeys it supports, the modules it contains and the milestones it is tracked under. Use when describing what actually ships -- apps, services, CLIs, libraries, extensions, documentation."
---

# SpecForge Deliverables DSL

> **Declared by `@specforge/product`**, a builtin extension. The `deliverable` kind exists only in a project that
> loads it: run `specforge extensions` first, and if it is not listed, do not write `deliverable` blocks (add it with
> `specforge add @specforge/product`, or write the kinds the project's own extensions declare).
> `specforge infer-guide deliverable` prints the fields.

Deliverables are what ships. They bridge journeys (what users do) and modules (how the work is organised).

## Block Syntax

```spec
deliverable user_management_mvp "User Management MVP" {
  artifact_type cli
  status        in_progress
  version       "0.1.0"
  owner         "identity-team"
  journeys      [create_new_user]
  modules       [core_lib]
  milestones    [mvp]
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `artifact_type` | identifier (required) | Kind of artifact: one word, for example `cli` `web_app` `documentation` `physical_product` `media` `event` `training`; any word is accepted. |
| `status` | enum `draft` `in_progress` `shipped` `deprecated` | Lifecycle; absent means `draft`. |
| `journeys` | reference list -> journey | Journeys it supports. Missing: W043. |
| `modules` | reference list -> module | Modules it contains. Missing: W046. |
| `milestones` | reference list -> milestone | Milestones it is tracked under. |
| `depends_on` | reference list -> deliverable | Deliverables that must ship first (a cycle is E052). |
| `version` | string | Semantic version (otherwise I061). |
| `owner` | string | Person or team responsible (otherwise I080). |
| `contributors` | string list | Others contributing. |
| `reason` | string | Why the status is what it is (a `deprecated` deliverable without one is I066). |
| `description` | string | Summary. |
| `tags` | string list | Lowercase-hyphenated labels. |

## Relationships

| Field | Target |
|-------|--------|
| `journeys` | journey |
| `modules` | module |
| `milestones` | milestone |
| `depends_on` | deliverable |
| a release's `deliverables` | this deliverable |

## Writing Rules

1. **Shippable artifacts only** -- things you deploy, publish or release.
2. **Bundle journeys, not features** -- journeys trace to features.
3. **One deliverable per artifact** -- a web app and a CLI are separate deliverables.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E006 | core | `artifact_type` is missing. |
| E061 | core | `status` outside its enum. |
| E052 | product | `depends_on` cycle. |
| W043 / W046 | product | No journeys / no modules. |
| I061 | product | `version` is not semver. |
| I065 | product | `shipped` while a milestone it names is not `completed`. |
| I066 | product | `deprecated` without `reason`. |
| I080 | product | No `owner`. |

## Examples

### Web Application

```spec
deliverable web_dashboard "Web Dashboard" {
  artifact_type web_app
  status        in_progress
  owner         "web-team"
  journeys      [create_new_user, create_user_via_api]
  modules       [core_lib, web_lib]
  milestones    [mvp]
  tags          ["customer-facing"]
}
```

### Minimal

```spec
deliverable rest_api_service "REST API Service" {
  artifact_type api
  owner         "platform-team"
  journeys      [create_user_via_api]
  modules       [core_lib]
}
```

## What NOT to Do

- Do not write `personas` or `refs` on a deliverable -- the kind declares neither (W020); personas are reached through journeys
- Do not confuse deliverables (what ships) with modules (how the work is grouped)
- Do not bundle features directly -- bundle journeys, which trace to features
