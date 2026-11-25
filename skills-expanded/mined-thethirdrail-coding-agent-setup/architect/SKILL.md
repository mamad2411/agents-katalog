---
name: architect
description: |
  Plan projects, architecture, APIs, frontend/backend boundaries, database design, and setup decisions.
  Use when planning, designing, scoping, setting up a project, creating architecture docs, designing APIs, or choosing frontend/backend/data patterns.
---
# Architect

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| End-to-end architecture planning | `architect.md` | Read when the user needs a full plan or ambiguous requirements clarified. |
| Architecture docs and diagrams | `architecture-planner.md` | Read when diagrams, ADRs, or system documentation are requested. |
| Backend systems | `backend-architect.md` | Read for API/service/data/security architecture tradeoffs. |
| Frontend systems | `frontend-architect.md` | Read for UI component boundaries, state, accessibility, or responsive design. |
| API interface design | `api-builder.md` | Read when designing REST, GraphQL, validation, auth, or OpenAPI surfaces. |
| Database design and optimization | `database-optimizer.md` | Read for schemas, indexes, query plans, or data modeling. |
| Initial project setup | `project-setup.md` | Read when turning an approved plan into repo structure/config/docs. |
| Workspace rules bootstrap | `workspace-rules-bootstrapper.md` | Read when initializing workspace rules or policy modules. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `architect`, `architecture-planner`, `backend-architect`, `frontend-architect`, `api-builder`, `database-optimizer`, `project-setup`, `workspace-rules-bootstrapper`.

Related routers: `research-docs`, `code`, `quality-repair`.
