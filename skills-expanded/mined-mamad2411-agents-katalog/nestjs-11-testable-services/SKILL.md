---
name: nestjs-11-testable-services
description: Refactors NestJS 11 services toward testable provider design, explicit dependency boundaries, provider tokens, focused unit tests, and reliable TestingModule setup. Use when services are hard to test, tightly coupled, or missing provider tests.
license: MIT
compatibility: "For NestJS 11.x projects using @nestjs/testing or compatible test tooling."
---

# NestJS 11 Testable Services

This skill helps agents improve services so they can be tested without starting the full application or contacting real external systems.

## When to Use This Skill

Use this skill when:

- A service test is hard to write because dependencies are hidden or constructed manually.
- A service calls external systems directly.
- A controller contains logic that belongs in a service.
- Tests require too many unrelated modules.
- A provider needs mockable boundaries.

## Workflow References

- `workflows/service-testability-refactor-workflow.md`
- `workflows/provider-test-workflow.md`

## Resource References

- `resources/testable-service-checklist.md`
- `resources/mock-boundary-patterns.md`

## Example References

- `examples/service-refactor-before-after.md`

## Guidance

1. Prefer constructor injection for all collaborators.
2. Keep service methods deterministic where possible.
3. Use provider tokens for external systems or swappable behavior.
4. Keep tests focused on provider behavior.
5. Override external providers in `TestingModule`.
6. Do not connect to real services from unit tests.
