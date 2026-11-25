# Packages

## Purpose

- Own reusable workspace packages consumed by apps and other packages.
- Keep shared UI, database, and configuration behavior out of application folders.

## Ownership

- `packages/config/AGENTS.md` owns shared config/constants.
- `packages/db/AGENTS.md` owns database client, Drizzle schema, and migrations.
- `packages/ui/AGENTS.md` owns shared Svelte UI styles, utilities, and generated component conventions.
- Root owns workspace registration in `pnpm-workspace.yaml`, top-level Turbo tasks, and dependency manager policy.

## Local Contracts

- Package public APIs are defined by each package's `package.json` `exports`.
- Workspace consumers should import packages by package name, not by cross-package relative paths.
- Add package-local dependencies in the package that uses them.

## Work Guidance

- Keep packages focused on reusable behavior with no website-only runtime assumptions.
- Update this Child DOX Index when adding, moving, or deleting packages.

## Verification

- Use package-filtered checks, for example `pnpm --filter @repo/db check-types` or `pnpm --filter @repo/ui check`.
- Use root Turbo commands when a shared package change can affect multiple consumers.

## Child DOX Index

- `packages/config/AGENTS.md` - shared config/constants package.
- `packages/db/AGENTS.md` - Drizzle/PostgreSQL database package.
- `packages/ui/AGENTS.md` - shared Svelte UI package.
