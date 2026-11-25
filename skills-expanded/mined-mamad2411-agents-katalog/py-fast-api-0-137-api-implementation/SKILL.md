---
name: py-fast-api-0-137-api-implementation
description: Implements and refactors FastAPI 0.137.x API endpoints, routers, dependencies, request models, response models, and OpenAPI metadata. Use when adding routes, changing APIRouter structure, or designing Python API behavior.
license: MIT
---

# FastAPI 0.137.x API Implementation Skill

Use this skill for FastAPI `0.137.x` route implementation and route refactoring.

## Version Boundary

This skill is scoped to FastAPI `0.137.x`. Do not generalize its router guidance to other FastAPI minor lines without checking that line's release notes.

## When to Use

- Adding a new path operation.
- Refactoring route modules or `APIRouter` usage.
- Introducing request or response models.
- Adding dependencies for auth, tenant scoping, pagination, filtering, or service access.
- Reviewing OpenAPI metadata for an endpoint.

## How to Work

1. Read the relevant route, schema, dependency, and test files.
2. Check `resources/route-design-checklist.md` before designing the change.
3. Use `examples/route-module-example.md` as a pattern only when it matches the repository architecture.
4. Keep route functions thin; push business logic into services or domain modules.
5. Use `typing.Annotated` with `Depends`, `Path`, `Query`, `Header`, or `Body` for clear dependency and parameter declarations.
6. Define explicit request and response models for non-trivial endpoints.
7. Keep router prefixes, tags, and dependencies consistent.
8. Do not inspect or mutate `router.routes` as part of route registration logic in `0.137.x`.
9. Add tests through the testing skill when behavior changes.

## Workflow

Use `workflows/implement-endpoint-workflow.md` when the task is more than a one-line route edit.
