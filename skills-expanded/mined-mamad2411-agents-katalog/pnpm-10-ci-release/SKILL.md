---
name: pnpm-10-ci-release
description: Prepares CI and release-safe pnpm 10 command sequences. Use when verifying frozen-lockfile installs, cache-aware installs, publish preflight, pack checks, recursive scripts, deploy checks, or release readiness in pnpm 10 repositories.
license: MIT
compatibility: Requires a repository using pnpm 10.x.
---


# pnpm 10 CI and Release

Use this skill for package-manager command choices in CI and release preflight.

## CI Principles

- Enable Corepack or install pnpm 10 before project commands.
- Use the repository `packageManager` field.
- Use `pnpm install --frozen-lockfile` when a lockfile exists.
- Use filtered recursive commands for large workspaces.
- Do not run `pnpm install --no-lockfile` in CI.

## Verification Commands

```bash
pnpm install --frozen-lockfile
pnpm -r run --if-present lint
pnpm -r run --if-present typecheck
pnpm -r run --if-present test
pnpm -r run --if-present build
pnpm audit --audit-level high
```

## Publish Preflight

Run `pnpm pack` or `pnpm publish --dry-run` before actual publish.

## Workflows

- [ci-lockfile-verification-workflow](workflows/ci-lockfile-verification-workflow.md)
- [release-publish-preflight-workflow](workflows/release-publish-preflight-workflow.md)

## Resources and Examples

- [CI checklist](resources/ci-checklist.md)
- [CI command sequence](examples/ci-command-sequence.md)

