---
name: monorepo-management
description: Sets up and maintains a TypeScript monorepo with workspaces, shared configs, task caching and CI that builds only the packages a change affects.
---

# Monorepo management

Structure decides cost. Fix the graph before the tooling.

## Layout

- `apps/*` for deployables, `packages/*` for libraries. Apps depend on packages; packages never depend on apps; a package depending on another package is declared, never reached by a relative path.
- Use the package manager's workspaces (pnpm, npm or yarn) with the `workspace:*` protocol for internal dependencies. One lockfile at the root.

## Steps

1. Map the current graph: each package's name, its internal dependencies and its scripts. Report cycles and fix them by extracting the shared part into a third package.
2. Shared config goes in packages: `tsconfig.base.json` extended by each package, one ESLint config, one formatter config. Packages use TypeScript project references (`composite: true`) when builds are separate, or point `exports` at built output.
3. Every package exposes the same scripts: `build`, `test`, `lint`, `typecheck`. Add a task runner (Turborepo or Nx): declare `dependsOn: ["^build"]`, list inputs and outputs per task, and enable the cache.
4. Dependencies: keep versions aligned across packages (a `catalog` in pnpm, or syncpack). Put tools in the root only when every package uses them.
5. CI: run only affected tasks, for example `turbo run build test --filter=...[origin/main]`, and cache between runs. Keep a full run on the default branch.
6. Releases: use changesets or similar so each package versions on its own when it needs to.

## Rules

- Never add a path alias that reaches into another package's `src`.
- Verify with a clean install and `build` from scratch before you finish.

## Report

The graph before and after, config added, and CI time with and without the cache.
