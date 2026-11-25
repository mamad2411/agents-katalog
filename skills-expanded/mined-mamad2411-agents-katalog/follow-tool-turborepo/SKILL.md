---
name: follow-tool-turborepo
description: Set up and use Turborepo v2.x for monorepo task orchestration
argument-hint: "[scope]"
related:
  - follow-monorepo
  - follow-tasks
  - follow-tool-taze
  - follow-tool-vite
  - follow-tool-vitest
  - follow-tool-moonrepo
  - run-build
  - run-test

---

## Goal

Set up and use Turborepo v2.x for task orchestration, caching, and build pipelines in a monorepo

## Scope

Use for monorepos that need to orchestrate tasks, cache outputs, use remote cache, and enforce package boundaries

- Package build pipeline: see `references/apis.md`

- Boundary: use Turborepo for JS/TS monorepo task orchestration; if the project uses Moon, use `/follow-tool-moonrepo` instead; for dependency updates across workspaces, use `/follow-tool-taze`
- Latest: `turbo@2.11.4` (verified 2026-09-26)

## Execute

### Workflows

| Topic | Workflow |-------|----------| Install, `turbo.json` init, workspace layout | `workflows/setup-turborepo/SKILL.md` | `tasks`, `dependsOn`, `inputs`/`outputs`, env, package overrides | `workflows/config-pipeline/SKILL.md` | Remote cache, `--filter`, `--affected`, cache hit tuning | `workflows/optimize-cache/SKILL.md` 
### 1. Repository Structure

> Goal: Arrange the workspace structure for Turborepo

1. Use `bun` or the package manager the project uses
2. Set up the root `package.json` with `private`, `packageManager`, `workspaces`
3. Organize directories with `apps/*` and `packages/*`
4. Avoid nested packages
5. Verify each package has a `package.json` with `exports`

### 2. Install Turbo

> Goal: Install the turbo CLI

1. Install with `bun add -D turbo`
2. Verify the version with `bunx turbo --version`
3. See CLI details in 

### 3. Configure turbo.json

> Goal: Create `turbo.json` at the root

1. Create `turbo.json` at the root with `$schema`
2. Define `tasks` for build, test, lint, dev
3. Set `dependsOn`, `inputs`, `outputs`, `cache`
4. Configure `env` and `passThroughEnv`
5. Enable `futureFlags.globalConfiguration` to move global keys into `global`
6. See config details in 

### 4. Package-Level Config

> Goal: override or extend the root config per package

1. Create a `turbo.json` in the package when an override is needed
2. Use `"extends": ["//"]` to inherit from the root
3. Use `$TURBO_EXTENDS$` to append instead of replace
4. Specify package-specific `outputs` and `dependsOn`

### 5. Task Filtering and Watch

> Goal: Use filters and watch mode

1. Run `bunx turbo run <task>`
2. Use `--filter` for specific packages
3. Use `--affected` for changed packages
4. Use `bunx turbo watch <task>` for development
5. Use `--dry=json` to inspect the task graph

### 6. Boundaries and Remote Cache

> Goal: Enforce package isolation and remote cache

1. Use `bunx turbo boundaries` to check package isolation
2. Define `tags` and `boundaries` rules in `turbo.json`
3. Set up the remote cache with `bunx turbo link --yes`
4. Use `TURBO_TOKEN` and `TURBO_TEAM` for authentication
5. Configure `cacheMaxSize` and `cacheMaxAge`

## Rules

### 1. Configuration

- Use `turbo.json` at the root with `$schema`
- Use `futureFlags.globalConfiguration: true`
- Define `inputs` and `outputs` explicitly

### 2. Task Dependencies

- Use `^task` for upstream dependencies
- Use `task` for the same package
- Specify `dependsOn` per the task graph

### 3. Caching

- Enable `cache: true` for deterministic tasks
- Disable `cache` for dev servers and side-effect tasks
- Use `persistent: true` for long-running tasks

### 4. Environment Variables

- Use `env` for variables that affect the cache hash (no `$` prefix)
- Use `passThroughEnv` for secrets
- Never hard-code secrets

### 5. Boundaries

- Use `turbo boundaries` to check package isolation
- Define `tags` and `boundaries` rules
- Avoid imports that cross package boundaries

- Use /follow-monorepo if needed
- Use /follow-tasks if needed
- Use /follow-tool-taze if needed
- Use /follow-tool-vite if needed
- Use /follow-tool-vitest if needed
- Use /follow-tool-moonrepo if needed
- Use /run-build if needed
- Use /run-test all if needed

## References

- [CLI reference](references/cli.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Correct `turbo.json`
- Tasks run and cache properly
- Watch mode and filters work
- Remote cache is configured
- Package isolation enforced with boundaries

