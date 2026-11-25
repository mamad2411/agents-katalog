---
name: feature-spec-templates
description: Feature specification structure, API contract patterns, and state definition templates. Use when writing implementation-ready feature specs that development agents can execute without ambiguity.
---

# Feature Spec Templates

A feature spec translates a PRD from "what to build" into "exactly how it should behave." Its primary reader is the Development agent — so if a spec leaves room for interpretation, the interpretation will happen during implementation, not during planning. This skill covers the structure and patterns for writing unambiguous feature specs.

## When to Use This Skill

- Writing a feature spec from a PRD and journey maps
- Specifying API contracts for backend features
- Documenting all UI states for a new or changed screen
- Reviewing a spec for gaps that would require clarification during development
- Creating a spec that will be handed off to a design team

## Core Concepts

### 1. Spec the States, Not Just the Flow

The most common spec gap is specifying the happy path flow but not the states. Every screen element has states:
- **Default / initial state** — what does a first-time user see?
- **Loading state** — what appears while data is fetching?
- **Empty state** — what appears when there's no data?
- **Populated state** — what appears with data?
- **Error state** — what appears when something fails?
- **Disabled state** — what appears when the action isn't available?

### 2. Spec the Boundaries

For every input field, list:
- Minimum and maximum length
- Allowed characters / format
- What happens at the boundary (trim? truncate? reject?)
- What happens when empty and the user tries to proceed

### 3. Explicit Out-of-Scope Section

Every spec must say what it does NOT cover. This prevents scope creep and sets Development's expectations.

## Full Feature Spec Template

```markdown
# Feature Spec: [Feature Name]

**PRD reference:** [Link or section]
**Author:** [Name]
**Status:** Draft / In Review / Approved
**Last updated:** [Date]

---

## Overview

[1-3 sentences describing what this feature does and why.]

## Out of Scope

The following are explicitly NOT part of this spec:
- [Item 1]
- [Item 2]

---

## UI Specification

### Screen: [Screen Name]

**Entry:** [How does the user get here?]

#### States

**Default / Initial State**
[Describe what the user sees when they first land on this screen]

**Loading State**
[What appears while content is loading? Skeleton screens? Spinners? Disabled inputs?]

**Populated State**
[What appears when content is loaded successfully?]

**Empty State**
[What appears when there's no content to show?]
- Headline: "[Copy]"
- Body: "[Copy]"
- CTA (if any): "[Label]" → [Action]

**Error State**
[What appears when loading fails?]
- Error message: "[User-facing copy]"
- Recovery action: [What can the user do?]

#### Components

**[Component Name]**
- Type: [Button / Input / List / Card / etc.]
- Label: "[Copy]"
- Behavior: [What happens when interacted with]
- Disabled condition: [When is this disabled, if ever]
- Validation: [Input rules if applicable]

---

## Backend Specification

### API Endpoints

#### [Method] /api/[path]

**Purpose:** [What this endpoint does]

**Authentication:** Required / Optional / None

**Request:**
```json
{
  "field_name": "type — description",
  "field_name": "type — required — constraints"
}
```

**Validation rules:**
- `field_name`: [min/max length, format, required/optional]

**Response — Success (200):**
```json
{
  "field_name": "type — description"
}
```

**Response — Errors:**
| Status Code | Condition | Response Body |
|-------------|-----------|---------------|
| 400 | [Invalid input condition] | `{"error": "...", "field": "..."}` |
| 401 | [Unauthenticated] | `{"error": "Authentication required"}` |
| 404 | [Resource not found] | `{"error": "Resource not found"}` |
| 422 | [Validation failure] | `{"error": "...", "details": [...]}` |
| 500 | [Server error] | `{"error": "Internal server error"}` |

**Performance requirements:**
- P50 response time: < [Xms]
- P95 response time: < [Xms]
- Rate limit: [X requests per minute per user]

---

### Business Logic Rules

#### Rule: [Rule Name]
```
Condition: [When this rule applies]
Action: [What the system does]
Example: [Concrete example]
```

#### Rule: [Rule Name]
[Same structure]

---

### Data Model Changes

#### [Table / Collection Name]

New fields:
| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| [field] | [type] | [Y/N] | [value] | [description] |

---

## Integration Points

| External System | Interaction | Failure Behavior |
|----------------|------------|-----------------|
| [Service name] | [What we call it for] | [What we do if it's down or slow] |

---

## Definition of Done

- [ ] [Specific AC 1]
- [ ] [Specific AC 2]
- [ ] [Performance criterion]
- [ ] [Accessibility criterion]
```

## API Contract Patterns

### REST Endpoint Naming

```
# Collections
GET    /api/orders          # List orders
POST   /api/orders          # Create order
GET    /api/orders/{id}     # Get specific order
PATCH  /api/orders/{id}     # Partial update
DELETE /api/orders/{id}     # Delete

# Nested resources
GET    /api/orders/{id}/items        # List items in order
POST   /api/orders/{id}/items        # Add item to order

# Actions (when CRUD doesn't fit)
POST   /api/orders/{id}/cancel       # Cancel order
POST   /api/orders/{id}/refund       # Issue refund
```

### Pagination Pattern

```json
{
  "data": [...],
  "pagination": {
    "total": 1250,
    "page": 1,
    "per_page": 20,
    "next_cursor": "eyJpZCI6IDEyM30="
  }
}
```

Use cursor-based pagination for real-time data; offset-based for static datasets.

### Error Response Standard

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

## State Definition Checklist

For every UI component, verify the spec covers:

- [ ] Default/initial state
- [ ] Loading state (if data is fetched)
- [ ] Empty state (if content can be absent)
- [ ] Populated state
- [ ] Error state
- [ ] Disabled state (if the action can be unavailable)
- [ ] Focused state (for form inputs)
- [ ] Validation error state (for form inputs)
- [ ] Success state (after form submission or action)

## Best Practices

1. **Write for a developer who has never seen the product** — don't assume context
2. **Use concrete examples** — abstract descriptions invite misinterpretation
3. **Never write "as needed" or "if appropriate"** — define the condition explicitly
4. **Spec the copy** — placeholder text, error messages, and labels must be in the spec
5. **Distinguish UI behavior from backend logic** — a spec that mixes them is hard to review and hard to implement
6. **Out-of-scope section is not optional** — what you don't specify, someone will assume
