---
name: nestjs-11-api-endpoint-review
description: Reviews NestJS 11 API endpoints, controllers, DTOs, pipes, guards, status codes, error mapping, and validation coverage. Use when checking endpoint correctness, security, route compatibility, or request/response contracts.
license: MIT
compatibility: "For NestJS 11.x HTTP APIs using Express or Fastify adapters."
---

# NestJS 11 API Endpoint Review

This skill helps an agent review API endpoints before or after implementation.

## When to Use This Skill

Use this skill when:

- Reviewing a controller or endpoint PR.
- Adding route-level validation.
- Auditing DTOs and `ValidationPipe` behavior.
- Checking error responses and status codes.
- Reviewing NestJS 11 route compatibility for Express v5 or Fastify v5.
- Preparing API changes for client-facing release notes.

## Workflow References

- `workflows/endpoint-contract-review-workflow.md`
- `workflows/dto-validation-review-workflow.md`

## Resource References

- `resources/endpoint-review-checklist.md`
- `resources/dto-validation-boundary-checklist.md`

## Example References

- `examples/endpoint-review-notes-example.md`

## Review Guidance

1. Identify all external inputs.
2. Verify DTOs and pipes for each structured input.
3. Confirm route patterns are compatible with the active adapter.
4. Check guards and authorization assumptions.
5. Check success and error response behavior.
6. Verify tests cover important paths.
7. Report actionable findings with file paths and risk levels.
