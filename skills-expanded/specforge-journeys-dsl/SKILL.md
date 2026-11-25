---
name: specforge-journeys-dsl
description: "Write journey blocks in .spec files (the journey kind is declared by the builtin @specforge/product extension). Each journey declares a user flow with a snake_case ID, the persona who takes it, the channels it happens through, the features it exercises and an ordered step-by-step flow. Use when describing how a specific kind of user experiences a product -- software, a clinic visit, a course enrollment or a customer purchase."
---

# SpecForge Journeys DSL

> **Declared by `@specforge/product`**, a builtin extension. The `journey` kind (and the `persona`, `channel` and
> `feature` kinds it points at) exists only in a project that loads it: run `specforge extensions` first, and if it is
> not listed, do not write `journey` blocks (add it with `specforge add @specforge/product`, or write the kinds the
> project's own extensions declare). `specforge infer-guide journey` prints the fields.

Journeys describe what a real person does, step by step. A journey points at a `persona` entity and at `channel`
entities, both declared as blocks of their own (not inside the `spec` block).

## Block Syntax

```spec
persona admin "Administrator" {
  description     "Manages user accounts for the organisation"
  technical_level intermediate
}

channel web "Web App" {
  description       "The browser application"
  interaction_model request_response
}

journey create_new_user "Create a New User" {
  persona  admin
  channels [web]
  features [user_management]
  priority high

  flow [
    "Admin opens the user management page",
    "Clicks \"New User\"",
    "Fills the form (name, email, role)",
    "Submits -- the system checks the email is unique",
    "Success: the user appears in the list",
    "Failure: an inline error on the email field",
  ]
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `flow` | string list (required) | Ordered steps: user actions and system responses. Empty: I050. |
| `persona` | reference -> persona | Who takes the journey. Missing: I054. |
| `channels` | reference list -> channel | Where it happens. Missing or empty: I055. |
| `features` | reference list -> feature | Features exercised. |
| `priority` | enum `critical` `high` `medium` `low` | Importance. |
| `description` | string | Summary. |
| `tags` | string list | Lowercase-hyphenated labels. |

`persona` declares `description` (required), `technical_level` (`expert` `advanced` `intermediate` `beginner`
`non_technical`), `goals`, `pain_points`, `status` (`active` `deprecated`), `reason`, `key_features`.
`channel` declares `description` (required), `interaction_model` (identifier: one word, e.g. `request_response` `event_driven` `batch`
`streaming` `bidirectional` `manual` `in_person` `self_service` `broadcast`; any word is accepted), `url`, `status`, `reason`.

## Relationships

| Field | Target |
|-------|--------|
| `persona` | persona |
| `channels` | channel |
| `features` | feature |
| a deliverable's `journeys` | this journey |

## Writing Rules

1. **Name as user actions** -- "Create a New User", not "User Creation".
2. **One step per item, in order** -- alternate user actions and system responses.
3. **Include success and failure paths.**
4. **One journey per persona and goal** -- different personas doing the same thing are different journeys.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E003 / E022 | core | `persona`, `channels` or `features` names nothing, or an entity of another kind. |
| E006 | core | `flow` is missing. |
| W042 | product | No deliverable references the journey. |
| I050 | product | `flow []`. |
| I054 | product | No `persona`. |
| I055 | product | No `channels`. |
| I046 / I047 | product | A persona / channel no journey references. |

## Examples

### API Journey

```spec
journey create_user_via_api "Create User via API" {
  persona  api_consumer
  channels [public_api]
  features [user_management]

  flow [
    "Consumer sends POST /api/v1/users with a JSON body",
    "The system validates the request body",
    "The system checks the email is unique",
    "Success: 201 Created with the user object",
    "Duplicate email: 409 Conflict",
  ]
}
```

### Healthcare Journey

```spec
persona patient "Patient" {
  description     "Books and attends appointments"
  technical_level non_technical
}

channel phone "Phone" {
  description       "Calls to the clinic front desk"
  interaction_model manual
}

journey schedule_appointment "Schedule a Doctor Appointment" {
  persona  patient
  channels [phone, web]
  features [appointment_scheduling]

  flow [
    "Patient calls the clinic or opens the web portal",
    "Selects a doctor and an available time slot",
    "The system checks the doctor's availability",
    "Patient confirms the appointment details",
    "Success: a confirmation is sent by SMS and email",
    "Conflict: alternative slots are suggested",
  ]
}
```

## What NOT to Do

- Do not declare personas or channels inside the `spec` block -- they are `persona` and `channel` entities
- Do not write `refs` on a journey -- the kind does not declare it (W020)
- Do not confuse journeys (a user's path) with features (units of value)
- Do not omit failure paths from the flow
