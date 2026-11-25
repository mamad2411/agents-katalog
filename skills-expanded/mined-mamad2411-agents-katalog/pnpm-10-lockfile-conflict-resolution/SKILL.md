---
name: pnpm-10-lockfile-conflict-resolution
description: Resolves pnpm 10 lockfile conflicts and lockfile drift. Use when pnpm-lock.yaml has merge conflicts, frozen-lockfile failures, lockfile config mismatches, or when deciding whether lockfile regeneration is safe.
license: MIT
compatibility: Requires a repository using pnpm 10.x.
---


# pnpm 10 Lockfile Conflict Resolution

Use this skill when `pnpm-lock.yaml` has merge conflicts, is out of sync with package manifests, or fails frozen-lockfile verification.

## Principles

- Treat `pnpm-lock.yaml` as generated state owned by pnpm 10.
- Resolve package manifests and `pnpm-workspace.yaml` first.
- Prefer regenerating with pnpm 10 over hand-merging large lockfile sections.
- Review lockfile diffs after repair.

## Common Commands

- `pnpm install --frozen-lockfile`
- `pnpm install --lockfile-only`
- `pnpm install --fix-lockfile`
- `pnpm why <package>`

## Workflows

- [lockfile-conflict-resolution-workflow](workflows/lockfile-conflict-resolution-workflow.md)
- [lockfile-regeneration-review-workflow](workflows/lockfile-regeneration-review-workflow.md)

## Resources and Examples

- [Lockfile conflict checklist](resources/lockfile-conflict-checklist.md)
- [Lockfile conflict notes](examples/lockfile-conflict-resolution-notes.md)

