---
name: monorepo-management
description: "Operate a monorepo: package boundaries, workspace tooling, affected-only CI, versioning strategy and safe incremental builds."
type: procedural
category: development
domain: development
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - monorepo structure design
  - nx turborepo affected build
  - workspace dependency graph
  - monorepo versioning strategy
  - monorepo ci caching
keywords:
  - monorepo
  - workspaces
  - affected
  - turborepo
  - nx
  - changesets
source: custom
enabled: true
---

# Monorepo Management

## Purpose

Operate a monorepo: package boundaries, workspace tooling, affected-only CI, versioning strategy and safe incremental builds.

## When to Use

- A repository holds multiple packages and CI rebuilds everything on every change.
- Shared code must be split into explicit packages with stable boundaries.
- Releases need coordinated versions across packages.

## When NOT to Use

- The repository is a single application that does not benefit from workspaces.
- The team cannot invest in build caching and task graphs.
- Package boundaries would be artificial and change weekly.

## Capabilities

- Define package boundaries that follow ownership and release cadence.
- Configure workspace tooling with a task graph and remote caching.
- Run only affected tasks in CI while keeping full runs available.
- Version packages with a documented strategy (fixed or independent).

## Inputs

- The current repository layout and package manifests.
- The CI provider and its cache capacity.
- The release cadence and which packages are published.

## Workflow

1. Map packages and their dependency edges before changing anything.
2. Make shared code an explicit package rather than deep relative imports.
3. Configure the task graph (build, test, lint) with declared outputs for caching.
4. Gate merges on affected-only runs plus a nightly full run.
5. Automate versioning and changelogs with changesets or the tool's release flow.

## Tools

- Turborepo / Nx / pnpm workspaces
- changesets
- CI cache

## Examples

- `npx turbo run build test --filter=...[HEAD^1]`
- `npx nx affected -t test --base=origin/main`
- `npx changeset`

## Safety

- A cache key that ignores lockfiles can serve stale builds.
- Deep imports across package boundaries make refactoring impossible; enforce with lint rules.
- Publishing from a monorepo can release untouched packages; pin the release graph.

## Source

All-Skills canonical library (`skills/development/monorepo-management`). First-party skill, maintained in this repository.

## Notes

- Affected-only CI is the main reason monorepos stay fast as they grow.
- Declared task outputs are required for caching to be correct.
- Pairs with: `devops/ci-cd-pipeline`, `development/dependency-audit`.
