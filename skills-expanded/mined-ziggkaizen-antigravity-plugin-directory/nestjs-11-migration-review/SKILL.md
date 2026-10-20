---
name: nestjs-11-migration-review
description: Reviews NestJS 10 to NestJS 11 migrations, package compatibility, Express v5 and Fastify v5 adapter changes, route patterns, lifecycle behavior, and migration risk. Use when upgrading, auditing, or debugging a NestJS 11 migration.
license: MIT
compatibility: "For projects migrating to or maintaining NestJS 11.x."
---

# NestJS 11 Migration Review

This skill guides migration review for NestJS 11, especially from NestJS 10.

## When to Use This Skill

Use this skill when:

- Upgrading `@nestjs/*` packages to 11.x.
- Reviewing a migration PR.
- Debugging route behavior after upgrading.
- Investigating adapter changes with Express or Fastify.
- Auditing lifecycle hooks, cache, config, or middleware behavior after a migration.

## Required Context

Inspect:

1. `package.json` and lockfile.
2. `src/main.ts`.
3. `nest-cli.json`.
4. Platform adapter packages.
5. Routes with wildcards, optional params, or regexp-like patterns.
6. Middleware registration.
7. Lifecycle hooks.
8. Cache and config module usage.
9. Existing e2e tests for affected routes.

## Workflow References

Use these workflows:

- `workflows/v10-to-v11-migration-workflow.md`
- `workflows/route-compatibility-review-workflow.md`

## Resource References

Use these resources:

- `resources/v11-migration-checklist.md`
- `resources/express-fastify-route-matrix.md`

## Example References

- `examples/express-v5-route-refactor-example.md`

## Migration Principles

- Upgrade deliberately. Do not mix unrelated dependency upgrades into the NestJS migration unless necessary.
- Keep exact version choices explicit.
- Verify adapter route behavior with tests, not visual inspection alone.
- Preserve public API compatibility unless the migration intentionally changes it.
- Document every behavior change that affects clients, middleware, lifecycle hooks, caching, configuration, or startup.
