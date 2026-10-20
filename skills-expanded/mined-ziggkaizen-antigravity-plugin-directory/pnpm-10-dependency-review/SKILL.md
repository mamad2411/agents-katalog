---
name: pnpm-10-dependency-review
description: Reviews and manages dependencies in pnpm 10 projects. Use when adding, removing, updating, auditing, approving build scripts, reviewing critical dependency ranges, or assessing package supply-chain risk in repositories that use pnpm 10.x.
license: MIT
compatibility: Requires a repository using pnpm 10.x.
---


# pnpm 10 Dependency Review

Use this skill for dependency mutations and supply-chain review in pnpm 10 repositories.

## Initial Checks

1. Confirm `package.json` declares `packageManager` as `pnpm@10...`.
2. Confirm `pnpm-lock.yaml` exists.
3. Check whether `pnpm-workspace.yaml` exists.
4. Read script help before using helpers.

## Preferred Commands

- `pnpm add <package>@<range>`
- `pnpm add -D <package>@<range>`
- `pnpm --filter <package> add <package>@<range>`
- `pnpm remove <package>`
- `pnpm update <package>`
- `pnpm why <package>`
- `pnpm audit --audit-level high`

## Critical Dependency Range Review

Avoid `*`, `latest`, `next`, broad `x` ranges, and unreviewed branch references for critical dependencies.

## Build-Script Review

Use `pnpm ignored-builds` and `pnpm approve-builds` for blocked scripts. For pnpm 10.26.0+, prefer `allowBuilds`. Never set `dangerouslyAllowAllBuilds: true` without explicit approval.

## Workflows

- [dependency-review-workflow](workflows/dependency-review-workflow.md)
- [dependency-security-review-workflow](workflows/dependency-security-review-workflow.md)

## Resources and Examples

- [Dependency review checklist](resources/dependency-review-checklist.md)
- [Security-focused workspace example](examples/pnpm-workspace-security.yaml)

