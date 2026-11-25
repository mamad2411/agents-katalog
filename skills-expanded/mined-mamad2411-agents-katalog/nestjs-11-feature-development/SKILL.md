---
name: nestjs-11-feature-development
description: Guides implementation and refactoring of NestJS 11 modules, controllers, providers, DTOs, pipes, guards, interceptors, and API features. Use when adding backend features, changing API contracts, or reorganizing NestJS application structure.
license: MIT
compatibility: "For NestJS 11.x TypeScript projects using standard Nest CLI or compatible tooling."
---

# NestJS 11 Feature Development

This skill helps an agent implement NestJS 11 features without breaking module boundaries, dependency injection, validation, routing, or API contracts.

## When to Use This Skill

Use this skill when the task involves:

- Adding or changing a controller, provider, module, DTO, pipe, guard, interceptor, or exception filter.
- Designing a new HTTP endpoint or refactoring an existing endpoint.
- Reorganizing modules or provider ownership.
- Adding framework-level validation, configuration, logging, or error handling.

Do not use this skill as the main guide for ORM schemas, database migrations, queue workers, cloud deployment, GraphQL schema design, or CI/CD. Those should be covered by separate plugins when needed.

## Required Context

Before editing, inspect:

1. `package.json` for exact NestJS and tooling versions.
2. `src/main.ts` for global pipes, filters, interceptors, CORS, logger, adapter, and prefix.
3. The relevant module file and any imported modules.
4. Existing DTO, provider, controller, and test patterns.
5. Existing error and response conventions.

## Development Principles

- Keep controllers transport-focused.
- Put business logic in injectable providers.
- Put infrastructure integration behind explicit provider boundaries.
- Validate external input before business logic.
- Keep DTOs and public API contracts intentional.
- Prefer narrow module exports. Do not export providers only because tests are hard.
- Avoid circular dependencies. If one appears, reassess ownership before using `forwardRef`.
- Prefer explicit exceptions and response mapping over leaking implementation details.

## Workflow References

Use these workflows from this skill:

- `workflows/api-feature-workflow.md` when adding or changing an API feature.
- `workflows/module-refactor-workflow.md` when reorganizing modules, providers, or dependency boundaries.

## Resource References

Read these resources when needed:

- `resources/nestjs-11-architecture-checklist.md`
- `resources/nestjs-11-api-patterns.md`

## Example References

Use these examples as patterns, not as mandatory templates:

- `examples/validated-controller-example.md`
- `examples/provider-boundary-example.md`

## Task Checklist

1. Confirm the feature belongs in the current module or identify the correct owning module.
2. Define the external contract first: route, params, query, body, status, response, errors.
3. Add DTOs and validation decorators when payloads are structured.
4. Add provider methods with explicit inputs and outputs.
5. Wire dependencies through module providers/imports/exports.
6. Add or update tests at the lowest useful level.
7. Run targeted checks, then broader quality checks if the change is complete.
8. Summarize compatibility, security, and testing impacts.
