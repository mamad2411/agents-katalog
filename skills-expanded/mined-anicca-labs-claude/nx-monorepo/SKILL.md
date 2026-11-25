---
name: nx-monorepo
description: Nx + pnpm monorepo conventions — workspace layout, module-boundary enforcement via ESLint tags, affected-based test/build runs, and caching config. Use when the project has an nx.json, apps/ + libs/ layout, or a pnpm-workspace.yaml.
---

Apply the following conventions to Nx + pnpm monorepo projects. Check `package.json`'s `packageManager` field or which lockfile is present (`pnpm-lock.yaml`) before running any install/add command — never assume yarn just because another plugin in this toolkit defaults to it.

## Workspace layout

`pnpm-workspace.yaml` at the repo root defines which directories are workspace packages:

```yaml
packages:
  - 'apps/*'
  - 'libs/*'
```

Convention: `apps/` holds deployable units (a web app, an API server); `libs/` holds everything shared between them (UI components, data-access, business logic, contracts). A change inside `libs/` should never import from `apps/` — dependencies flow one direction, into libs, never back out.

## Module boundaries: ESLint rule + package.json tags, not nx.json

The `@nx/enforce-module-boundaries` ESLint rule is what actually blocks a disallowed import, and it reads its rules from each package's `nx.tags` field in `package.json` (or `project.json`) — **not** from `nx.json`. This is a common misconception: `nx.json` holds target defaults and caching config, it has no boundary/dependency rules in it.

```json
// libs/data-access-billing/package.json
{
  "name": "@repo/data-access-billing",
  "nx": {
    "tags": ["type:data-access", "scope:billing"]
  }
}
```

```js
// eslint.config.js (root)
{
  rules: {
    '@nx/enforce-module-boundaries': [
      'error',
      {
        depConstraints: [
          { sourceTag: 'type:app', onlyDependOnLibsWithTags: ['type:feature', 'type:data-access', 'type:ui', 'type:util'] },
          { sourceTag: 'type:feature', onlyDependOnLibsWithTags: ['type:data-access', 'type:ui', 'type:util'] },
          { sourceTag: 'type:data-access', onlyDependOnLibsWithTags: ['type:util'] },
          { sourceTag: 'type:ui', onlyDependOnLibsWithTags: ['type:util'] },
          { sourceTag: 'type:util', onlyDependOnLibsWithTags: ['type:util'] },
          { sourceTag: 'scope:billing', onlyDependOnLibsWithTags: ['scope:billing', 'scope:shared'] },
          { sourceTag: 'scope:admin', onlyDependOnLibsWithTags: ['scope:admin', 'scope:shared'] },
        ],
      },
    ],
  },
}
```

## Two independent tag axes

A real Nx workspace typically tags on two orthogonal axes at once, and a lib usually carries one tag from each:

- **`type:`** — architectural layer, strictly layered so higher layers can depend down but not the reverse: `app` → `feature` → `data-access` / `ui` → `util`. A `util` lib (pure helpers, formatting, constants) can never import a `data-access` lib — that's the boundary rule catching an accidental layering violation.
- **`scope:`** — product-area isolation, so unrelated areas can't reach into each other's internals: `scope:billing`, `scope:admin`, `scope:onboarding`, plus a `scope:shared` that everything is allowed to depend on (design system, generic utils, the contracts package).

A lib tagged `type:data-access, scope:billing` can be imported by `type:feature` libs in `scope:billing` (or `scope:shared`), but never by something tagged `scope:admin` — catching cross-feature coupling that would otherwise only surface as a confusing production bug when billing internals change and admin silently breaks.

## `nx affected` for fast feedback

Run only what changed relative to a base branch, instead of the whole workspace:

```bash
nx affected -t test --base=main
nx affected -t lint build test --base=main
```

Nx computes the affected project graph from the git diff plus the dependency graph, so a change to a leaf `util` lib re-runs every consumer transitively, while a change to an isolated feature only re-runs that feature. Use `nx run-many -t test` (no `affected`) when you deliberately want everything, e.g. before a release cut.

## Caching via `targetDefaults`

`nx.json`'s `targetDefaults` (not the ESLint boundary config — that distinction matters, see above) controls what gets cached and what its cache key depends on:

```json
{
  "targetDefaults": {
    "build": { "cache": true, "dependsOn": ["^build"] },
    "test": { "cache": true },
    "lint": { "cache": true },
    "dev": { "cache": false },
    "e2e": { "cache": false }
  }
}
```

`build`/`test`/`lint` are deterministic given the same inputs — cache them. `dev` (a long-running watch process) and `e2e` (depends on external/live state, non-deterministic ordering) are typically left uncached; caching a long-running or non-deterministic target either does nothing useful or actively hides a stale result.

## Package manager: check, don't assume

This toolkit's default elsewhere is yarn, but an Nx workspace with a `pnpm-workspace.yaml` and `pnpm-lock.yaml` uses pnpm — confirm via `package.json`'s `"packageManager"` field (e.g. `"packageManager": "pnpm@9.x"`) or by checking which lockfile exists before running any install, add, or run command. Running `yarn add` in a pnpm workspace creates a second, conflicting lockfile and silently breaks `nx affected`'s dependency graph the next time someone installs cleanly.
