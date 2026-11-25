---
name: nestjs-11-service-design
description: Designs NestJS 11 services, providers, modules, dependency injection boundaries, and provider ownership. Use when creating service layers, splitting modules, reviewing dependency graphs, or deciding where business logic belongs.
license: MIT
compatibility: "For NestJS 11.x TypeScript projects using standard provider and module patterns."
---

# NestJS 11 Service Design

This skill helps agents design testable NestJS 11 services and module boundaries without coupling controllers, domain logic, and infrastructure details.

## When to Use This Skill

Use this skill when:

- Creating or refactoring services and providers.
- Deciding which module owns a provider.
- Splitting a large service or module.
- Introducing provider tokens, ports, adapters, or dependency inversion.
- Reviewing dependency injection wiring.
- Removing controller business logic.

## Do Not Use This Skill For

- Database-specific schema or migration design.
- Cloud deployment architecture.
- Queue, cache, or ORM-specific patterns unless already present in the repository.
- Domain-specific policies that are not general NestJS concerns.

## Workflow References

- `workflows/service-boundary-design-workflow.md` for designing or splitting service responsibilities.
- `workflows/provider-dependency-review-workflow.md` for reviewing provider imports, exports, tokens, and mocks.

## Resource References

- `resources/service-design-checklist.md`
- `resources/dependency-boundary-decision-tree.md`

## Example References

- `examples/provider-port-adapter-example.md`

## Operating Guidance

1. Start from the use case and API contract, not from file layout.
2. Identify the owning module.
3. Keep controllers thin and services testable.
4. Inject external dependencies through provider boundaries.
5. Prefer explicit provider tokens for swappable infrastructure.
6. Avoid circular dependencies and global modules unless the project already has a justified pattern.
7. Add tests around provider behavior and module compilation.
