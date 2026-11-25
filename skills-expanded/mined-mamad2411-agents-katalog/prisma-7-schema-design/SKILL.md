---
name: prisma-7-schema-design
description: Designs and reviews Prisma ORM 7 schemas. Use when creating models, configuring prisma.config.ts, choosing driver adapters, setting generated client output, reviewing model boundaries, or repairing Prisma Client generation/import paths.
license: MIT
compatibility: Requires Prisma ORM 7 or a project being upgraded to Prisma ORM 7.
---

# Prisma ORM 7 Schema Design

Use this skill for Prisma ORM 7 schema setup, schema review, generated client configuration, driver adapter selection, and model boundary design.

## When to Use This Skill

Use this skill when:

- Creating or changing `prisma/schema.prisma`.
- Creating or changing `prisma.config.ts`.
- Choosing a Prisma ORM 7 driver adapter.
- Adding or renaming Prisma models.
- Reviewing whether a model has clear ownership and persistence boundaries.
- Repairing Prisma Client generation or import paths.

## Workflows

- `workflows/design-prisma-schema-workflow.md`: Use before adding or changing Prisma models.
- `workflows/setup-prisma-7-workflow.md`: Use when creating or repairing Prisma ORM 7 setup.

## Resources

- `resources/driver-adapter-matrix.md`: Adapter selection guidance.
- `resources/prisma-7-config-template.md`: Minimal Prisma ORM 7 config and schema template.
- `resources/schema-boundary-checklist.md`: Generic schema ownership and boundary checklist.

## Examples

- `examples/generated-client-singleton.md`: Prisma ORM 7 generated client singleton example.
- `examples/prisma-schema-pattern.md`: Domain-aligned schema example.

## Scripts

- `scripts/prisma-7-project-check.sh`: Static Prisma ORM 7 compatibility checks.
- `scripts/prisma-schema-change-review.sh`: Hook helper for schema-change prompts.

Run scripts with `--help` before using them.

## Operating Guidance

1. Use Prisma ORM 7 generator/config/client patterns.
2. Make model names durable, domain-specific, and reviewable.
3. Keep schema ownership and module boundaries explicit.
4. Avoid leaking raw Prisma model types across public API or trust boundaries.
5. Run `prisma validate`, `prisma generate`, typecheck, and tests after schema changes.
6. Escalate ambiguous ownership or privacy-sensitive modeling decisions before implementation.
