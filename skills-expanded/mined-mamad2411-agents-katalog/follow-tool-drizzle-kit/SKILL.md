---
name: follow-tool-drizzle-kit
description: Use drizzle-kit for migrations — generate, migrate, push, studio
argument-hint: "[target-or-scope]"
related:
  - follow-lib-drizzle
  - run-verify
  - run-test
  - run-drizzle-studio

---

## Goal

Use drizzle-kit to manage migrations — generate, migrate, push, studio

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (drizzle kit tool)

- Boundary: this skill covers the `drizzle-kit` CLI only (generate/migrate/push/pull/check/studio) — for `drizzle-orm` schema/query APIs use `/follow-lib-drizzle`
- Latest: `drizzle-kit@0.31.11` (pairs with `drizzle-orm@0.45.3`) (verified 2026-09-26)
- Note: v1.0.0 is in the beta/rc channel (`beta` dist-tag, latest 1.0.0-rc.x) — has breaking changes (casing API, removes RQB v1 `db._query`); production still uses stable 0.31.x
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### 1. Pick Workflow

> Goal: dispatch specialized work to the appropriate workflow

| Topic | Workflow |-------|----------| `drizzle.config.ts` — dialect, schema, `out`, dbCredentials | `workflows/config-drizzle-kit/SKILL.md` | generate/push/migrate commands, workflow, rollback | `workflows/migrate-schema/SKILL.md` 
### 2. Setup And Usage

> Goal: use it correctly per official docs

1. Install `bun add -D drizzle-kit` (requires `drizzle-orm` + a database driver as peers — see `references/apis.md`)
1. `drizzle-kit generate` creates SQL migrations from schema diff (`--name`, `--custom`, `--breakpoints`)
1. `drizzle-kit migrate` applies migrations; `push` is for dev prototyping (`--force`, `--strict`)
1. `drizzle-kit pull` introspects the DB → drizzle schema; `check` detects migration collisions; `up` upgrades snapshots; `export` converts schema to SQL DDL
1. Set `drizzle.config.ts`: schema path, dialect, dbCredentials (multiple configs → select with `--config=<path>`)
1. Use `drizzle-kit studio` or `/run-drizzle-studio` for data browsing

### 3. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (drizzle kit tool)

## Rules

- production always uses `migrate` — `push` is dev-only
- review generated SQL before commit — rename detection is incomplete
- always keep migrations in version control
- never edit an applied migration — create a new migration

- Use `/follow-lib-drizzle` for `drizzle-orm` schema/query APIs
- Use `/run-drizzle-studio` for the data browsing UI
- Use `/run-verify` to verify lint + typecheck
- Use `/run-test` for related tests

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (drizzle kit tool)
- No known security/performance pitfalls (drizzle kit tool)
- Lint, typecheck, tests pass
