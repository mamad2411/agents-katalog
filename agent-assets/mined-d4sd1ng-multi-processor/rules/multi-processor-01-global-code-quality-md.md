---
name: Global Code Quality
alwaysApply: true
description: General code quality rules for all projects.
---

# Global Code Quality

## Code changes

- Keep changes minimal and localized.
- Prefer readable code over clever code.
- Preserve existing naming conventions.
- Preserve existing file structure unless clearly wrong.
- Do not introduce unnecessary dependencies.
- Do not duplicate logic.
- Do not leave dead code.
- Do not leave commented-out experimental code.
- Do not hide errors silently.

## Architecture

- Reuse existing services, repositories, clients, schemas and utilities.
- Add new modules only when there is no suitable existing place.
- Keep boundaries clear:
  - storage code does storage
  - API code exposes data/actions
  - UI code renders and calls API
  - business logic stays out of UI
- Do not mix unrelated responsibilities.

## Error handling

- Use explicit error messages.
- Preserve structured error responses where they exist.
- Fail safely rather than silently continuing with invalid data.
- Do not convert real failures into fake success states.

## Data integrity

- Do not invent missing data.
- Do not create fake placeholders unless the user explicitly asks for mock data.
- Validate IDs and references when connecting objects.
- Preserve source references and provenance when present.
