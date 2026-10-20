---
name: pnpm-10-workspace-setup
description: Sets up and reviews pnpm 10 workspaces. Use when creating or editing pnpm-workspace.yaml, workspace package manifests, workspace protocol dependencies, catalogs, filters, package boundaries, injected dependencies, or pnpm deploy behavior.
license: MIT
compatibility: Requires a repository using pnpm 10.x.
---


# pnpm 10 Workspace Setup

Use this skill for pnpm 10 monorepos and multi-package repositories.

## Workspace Foundations

- A workspace must have `pnpm-workspace.yaml` at the root.
- Use explicit package globs.
- Use `workspace:` for local-only internal dependencies.
- Use filters for scoped work.
- Use catalogs only for shared external ranges.
- Avoid cyclic workspace dependencies.

## Common Commands

- `pnpm install`
- `pnpm -r run --if-present <script>`
- `pnpm --filter <package> <command>`
- `pnpm --filter <package> add <dependency>`
- `pnpm --filter <package> --prod deploy <target-directory>`

## Workflows

- [workspace-setup-workflow](workflows/workspace-setup-workflow.md)
- [workspace-deploy-review-workflow](workflows/workspace-deploy-review-workflow.md)

## Resources and Examples

- [Workspace checklist](resources/workspace-checklist.md)
- [Basic workspace example](examples/pnpm-workspace-basic.yaml)

