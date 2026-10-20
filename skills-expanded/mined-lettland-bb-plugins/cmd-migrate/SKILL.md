---
name: cmd-migrate
description: Command — Guided code migration (language version, framework version, library, runtime).
---

# /migrate

Drives a guided migration: discover all sites touching the legacy thing, plan the change site-by-site, apply with tests at each step.

Argument: short description of the migration (`bun-to-pnpm`, `react-17-to-19`, `python-3.11-to-3.13`, `node-to-bun`).

Process:

1. Discovery: `grep -r <pattern> --include=<glob>` (use a per-language glob like `--include="*.py"` to avoid binary files and slow scans).
2. Group by file/module.
3. For each group: edit → run tests → commit.
4. Invoke the appropriate expert agent — `Agent(devkit:python-expert)`, `Agent(devkit:go-expert)`, `Agent(devkit:typescript-expert)`, `Agent(devkit:rust-expert)`, `Agent(devkit:react-expert)`, `Agent(devkit:gdscript-expert)`, or `Agent(devkit:postgres-expert)` (match the target stack).

For DB migrations specifically, invoke `Skill(migrations-overview)` for the tool-comparison matrix and migration-strategy guidance (covers alembic, sqlx, atlas, goose, drizzle, prisma).

## Arguments

`[from-X to-Y]`
