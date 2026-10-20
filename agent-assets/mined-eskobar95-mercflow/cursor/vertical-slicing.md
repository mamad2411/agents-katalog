---
description: Task breakdown and implementation strategy for MercFlow features
globs:
alwaysApply: true
---

# Vertical Slicing — MercFlow implementation principle

## Core rule
**Never decompose work into horizontal layers. Always slice vertically.**

Each task must deliver one user-visible capability end-to-end: DB migration → service/API → UI → tests. A task is done when a user can perform a complete action in the product, not when a layer is technically complete.

## Why
- Bugs surface at the slice boundary, not in a final integration
- Each task is independently shippable and testable
- Each task fits in one agent context window (~200k tokens)
- A failing task never blocks an entire DB or API layer

## Context window budget per task
Size tasks so a single agent can complete them within ~200k tokens:
- One user-facing capability (one screen, one flow, one endpoint group)
- No more than 3–4 files changed at the schema level
- One test file covering the slice
- If a slice exceeds this, split along the user journey (list → detail → create → edit)

## Naming convention
Name tasks after the **user outcome**, not the technical layer:

```
✓  "List products by category — admin-ui + backend"
✓  "Create product with variants — content-module + admin-ui"
✗  "Create DB tables for products"
✗  "Build product API endpoints"
```

## Task structure (always include these)

```markdown
## Slice objective
[What the user can do when this task is done]

## Layers in scope
- DB: [specific tables/columns/migrations]
- API: [specific endpoints]
- UI: [specific components/pages]
- Tests: [what to test]

## Acceptance criteria
- [ ] [Specific, testable criterion]

## Out of scope for this task
[What explicitly to skip — leave for another task]
```

## Sprint ordering (default pattern)

```
Sprint 1: Foundation slices (schema + core read paths — list/view)
Sprint 2: Write paths (create, edit, delete)
Sprint 3: Polish (edge cases, loading states, error handling, a11y)
```

Adjust based on PRD requirements and dependencies.

## MercFlow packages
```
packages/admin-ui       — React admin (Vite + Medusa UI)
packages/content-module — Medusa v2 module (DB, services, routes)
packages/design-tokens  — Shared tokens
apps/backend            — Guapo-specific backend config
```

Always link a task to the correct package(s) in Notion. If a task touches multiple packages, name them all — but keep the slice focused enough that one agent can hold all the context at once.
