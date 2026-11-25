---
name: nx-best-practices
description: Applies Nx monorepo best practices for project structure, caching, affected commands, targets, and generators. Use when working with Nx workspace, creating or configuring apps/libs, optimizing CI and cache, or resolving Nx configuration.
---

# Nx Best Practices

## Mental model

Nx uses a **project graph** (dependencies between projects), a **task graph** (which tasks run and in what order), **affected** (which projects/tasks are impacted by changes), and **computation hashing + caching** (replay results when inputs match). Use generators and Nx commands instead of ad-hoc scripts so the graph stays accurate.

## Project structure

- **Layout**: Use `workspaceLayout` in `nx.json` (e.g. `appsDir: "apps"`, `libsDir: "libs"`). Prefer a **flat** structure: many independent projects under `apps/` and `libs/` rather than deep nesting.
- **Apps vs libs**: Apps are deployable entry points; libs are shared code. Put new apps in `apps/<name>`, libs in `libs/<name>` (or `libs/<scope>/<name>` if you use scope folders).
- **Dependencies**: Declare dependencies via imports; Nx infers the graph. Use workspace `importPath` (e.g. `@meli-challenge/shared`) so libs are consumable with a single import.
- **Generators**: Create projects with Nx generators (`nx g @nx/node:app apps/api`, `nx g @nx/js:lib libs/shared --importPath=@meli-challenge/shared`) instead of copying folders manually.

## Configuration layers

Project config is merged in this order (later overrides earlier):

1. **Inferred** from plugins (e.g. from `package.json` scripts or tool config).
2. **Workspace** `targetDefaults` in `nx.json`.
3. **Project** `project.json` or `package.json` "nx" / scripts.

Prefer `targetDefaults` in `nx.json` for shared behavior (e.g. cache inputs/outputs, executor); override only per project when needed.

## Targets, inputs, and outputs

- **Targets**: Define `build`, `serve`, `test`, `lint` (and others) in `project.json` or via plugin inference. Use the same target names across projects when possible so `nx run-many -t build` works.
- **Inputs**: What the task depends on (source files, env, deps). Use `["production", "^production"]` for builds so Nx hashes project + dependencies. Tune so cache invalidates only when relevant files change.
- **Outputs**: Where the task writes artifacts (e.g. `["{projectRoot}/dist"]`). Required for cache restore and for downstream tasks that depend on build output.
- **Cache**: Tasks are cacheable by default when inputs/outputs are set. Use `nx run <project> --skip-nx-cache` only for one-off no-cache runs.

## Affected and CI

- **Affected**: `nx affected -t build` (or `test`, `lint`) runs the target only for projects impacted by changes since a base (e.g. `main`). Use in CI: `nx affected -t build --base=origin/main`.
- **Base ref**: Set `--base` to the comparison ref (commit or branch). CI typically uses the merge base with the default branch.
- **Flatter structure**: More, smaller projects increase the chance that only a subset is affected per PR; deep or few large projects reduce the benefit of affected.
- **Remote cache**: Pair affected with remote caching (Nx Cloud or self-hosted) so repeated CI runs reuse cache across machines.

## Dependency management

- **Single version vs per-project**: Nx supports both. Single version at root (lockfile + shared deps) simplifies upgrades; per-project deps allow independent versions when needed. Document the choice in the repo.
- **Workspace packages**: Use the package manager workspace protocol (e.g. `"@meli-challenge/shared": "workspace:*"`) for internal libs so the graph and installs stay correct.
- **Tags**: Use `tags` in `project.json` (e.g. `["scope:api", "type:app"]`) for boundary rules and `nx enforce-module-boundaries` if you adopt dependency constraints.

## Running tasks

- **Single project**: `nx run <project>:<target>` or `nx <target> <project>` (e.g. `nx build api`).
- **All projects**: `nx run-many -t build` (or `-t test`, `-t lint`).
- **Affected**: `nx affected -t build` (add `--base=...` in CI).
- **Graph**: `nx graph` to visualize project and task dependencies; use to verify structure and why a project is affected.

## Generators and plugins

- **Prefer plugin generators**: Use `@nx/node`, `@nx/express`, `@nx/react`, `@nx/js`, etc. to add apps/libs so config (targets, tsconfig, paths) is correct from the start.
- **Custom generators**: For repeated patterns, add local generators or invoke Nx generators with the same options so the workspace stays consistent.
- **Do not**: Create projects by hand-copying config; avoid scripts that run builds outside `nx run`/`nx affected` for projects that are already in the workspace.

## Checklist for new projects

- [ ] Created with Nx generator in the right folder (`apps/` or `libs/`).
- [ ] `project.json` (or plugin-inferred) has correct targets and, for build, inputs/outputs.
- [ ] Lib has `importPath` matching workspace scope (e.g. `@meli-challenge/<name>`).
- [ ] Dependencies on other workspace projects are via imports (graph inferred).
- [ ] `nx graph` shows the project and its edges correctly.
- [ ] `nx run <project>:<target>` and `nx affected -t <target>` behave as expected.

## Reference

- Project configuration, inputs/outputs, workspace layout: [reference.md](reference.md)
- Official docs: [nx.dev/docs](https://nx.dev/docs)
