---
name: nextjs-16-quality-and-migration
description: Audits, verifies, and migrates Next.js 16 applications. Use for quality gates, package scripts, next.config review, deprecated API detection, Next.js 15-to-16 upgrades, dependency checks, build failures, and final release verification.
license: MIT
compatibility: Requires Node.js 20.9.0+ for Next.js 16 projects. Shell scripts assume a POSIX shell.
---

# Next.js 16 Quality and Migration

Use this skill for audits, verification, upgrades, and final checks in a Next.js 16 repository.

## When to Use

- Reviewing `next.config.*`, `package.json`, lockfiles, App Router files, or migration changes.
- Running lint, type checks, tests, builds, and dependency checks.
- Migrating from Next.js 15 to 16.
- Removing deprecated or removed Next.js APIs.
- Investigating build failures, hydration errors, route errors, or cache issues.
- Preparing a final handoff after code changes.

## Workflows

- `workflows/quality-gate-workflow.md`: Use before final handoff or when validating a change.
- `workflows/upgrade-to-nextjs-16-workflow.md`: Use when planning or performing a Next.js 16 migration.

## Resources

- `resources/nextjs-16-breaking-change-matrix.md`: Common removed, renamed, deprecated, and behavior-changed items to inspect.

## Scripts

Run scripts with `--help` before use.

- `scripts/nextjs-16-config-audit.mjs`: Static audit for incompatible or risky Next.js 16 config patterns.
- `scripts/nextjs-16-quality-gate.sh`: Package-manager-aware lint/typecheck/test/build helper.
- `scripts/nextjs-16-dangerous-command-guard.sh`: Hook helper for risky command review.

## Examples

- `examples/safe-next-config.md`: Conservative `next.config.ts` baseline for a TypeScript Next.js 16 project.

## Operating Guidance

1. Prefer repository-defined scripts over invented commands.
2. Detect the package manager from lockfiles.
3. Run the fastest relevant checks first, then build confidence.
4. Do not run framework upgrades, codemods, or lockfile rewrites without explicit user approval.
5. Do not make verification pass by weakening TypeScript, lint, tests, or build checks.
6. Treat config changes as production-affecting changes.
7. When exact behavior cannot be verified locally, say what remains unverified.
