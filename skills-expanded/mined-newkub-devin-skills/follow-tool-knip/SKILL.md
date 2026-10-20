---
name: follow-tool-knip
description: Setup and configure Knip for detecting unused files, dependencies, and exports in monorepos
argument-hint: "[scope]"
related:
  - follow-monorepo
  - follow-tasks
  - run-scan
---

## Goal

Set up and use Knip to detect unused files, dependencies, and exports correctly per official best practices

## Scope

Use with any project that needs unused-code analysis — supports both single projects and monorepos with workspaces; for a monorepo, run `/follow-monorepo` first

- Latest: `knip@6.38.0` (verified 2026-09-24) — v6 uses `oxc-parser`/`oxc-resolver` (2-4x faster) and requires Node `^20.19.0 | >=22.12.0` or Bun
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Install And Create Config

> Goal: install Knip and create the config file in the root directory

1. Install `knip` with the project's package manager:
   - Bun project: `bun add -D knip`
   - If the project doesn't use Bun: use its package manager (npm, pnpm, yarn)
2. Create `knip.json` in the root directory for a monorepo or single project
3. Set `$schema` to `https://unpkg.com/knip@latest/schema.json`
4. For a monorepo → use the `workspaces` object instead of root-level `entry`/`project`

### 2. Configure Workspaces

> Goal: define entry points and project patterns per workspace

1. Knip reads workspaces automatically from `package.json#workspaces`, `pnpm-workspace.yaml`, or `knip.json#workspaces`
2. Each workspace needs a valid `package.json` — if the package manifest isn't valid, run `/follow-tasks` first; if there's no `package.json` → add the path to the `workspaces` object in `knip.json`
3. Specify `entry` only for files Knip doesn't detect automatically — Knip has plugins that auto-detect entry files from common patterns such as `src/index.ts`, `package.json#exports`
4. Set `project` as glob patterns of the workspace's source files
5. If a workspace has no custom entry/project → use an empty object `{}`
6. Run `bunx knip --debug` to verify the patterns are correct and nothing is redundant

### 3. Configure Advanced Options

> Goal: add options that improve detection accuracy

1. Add `ignoreExportsUsedInFile` to ignore exports used only within their own file — `{ "interface": true, "type": true }` is recommended
2. Add `includeEntryExports: true` in each workspace that is a private package to check unused exports in entry files
3. Add `treatConfigHintsAsErrors: true` to enforce a correct config — exit code 1 when config hints exist
4. Use `ignoreDependencies` only when necessary — e.g. type packages that never appear directly in imports
5. Use `ignoreBinaries` for binaries that are used but don't come from a dependency, e.g. `["docker-compose", "bunx"]`

### 4. Configure Package.json Scripts

> Goal: add scripts to run Knip in `package.json`

1. Add `"knip": "knip"` for the default analysis
2. Add `"knip:prod": "knip --production"` for production-only analysis (excludes tests, devDependencies)
3. Add `"knip:strict": "knip --strict"` for strict production mode (includes peerDependencies, type-only imports)
4. Never add `"knip:fix"` until the config is settled with no config hints — `knip --fix` is dangerous with an incomplete config

### 5. Run And Fix Issues

> Goal: run Knip and fix issues by priority

1. Run `bunx knip` first to see config hints — always fix config hints before anything else
2. Once config hints are gone → run `bunx knip` again to see actual issues
3. Review the reported issues — separate false positives from real ones
4. Fix unused code by deleting it or using it — don't ignore without reason
5. If ignoring is truly needed → use targeted options (`ignoreFiles`, `ignoreBinaries`, `ignoreDependencies`, `ignoreMembers`, `ignoreUnresolved`) instead of overly broad `ignore`
6. Run `bunx knip --production` to check production code separately

## Rules

### 1. Avoid Ignore Patterns

- Never use broad `ignore` like `/*.config.*`, `/*.d.ts` — Knip is not an ESLint-style file-based linter
- `ignore` only suppresses reporting, it doesn't exclude files from analysis — creating blind spots
- Use correct `entry` and `project` patterns instead of ignoring
- If truly needed, use targeted options: `ignoreFiles`, `ignoreBinaries`, `ignoreDependencies`, `ignoreMembers`, `ignoreUnresolved`

### 2. Monorepo Workspaces

- In a monorepo, use the `workspaces` object — root-level `entry`/`project` are ignored
- The root workspace is named `"."` under `workspaces`
- Each workspace supports: `entry`, `project`, `ignore`, `ignoreBinaries`, `ignoreDependencies`, `ignoreIssues`, `ignoreMembers`, `ignoreUnresolved`, `includeEntryExports`, `paths`, plugins
- Never nest workspaces in the Knip config — but the folder structure may nest
- Use the `--workspace` or `-W` flag to filter a workspace, e.g. `knip -W apps/website`
- v6: workspace isolation and libs inclusion are always the default — the `--include-libs` and `--isolate-workspaces` flags were removed; the `classMembers` issue type was removed and `namespaceMembers` was added

### 3. Production Mode

- Use `--production` to analyze production code only — automatically excludes tests, stories, devDependencies
- Use the `!` suffix in entry/project patterns to mark production files, e.g. `"src/index.ts!"`
- `--strict` implies `--production` and adds: verify workspace isolation, include peerDependencies, report type-only imports
- Run both default and production mode separately — they complement, not replace each other

### 4. Configuration Hints

- Always fix config hints first — they mean Knip doesn't understand the project, causing false positives
- Enable `treatConfigHintsAsErrors: true` to enforce a correct config
- Never ignore or disable config hints — fix the root cause
- Use `--debug` for verbose output of workspaces, plugins, and resolved files

### 5. Exports Configuration

- Use `ignoreExportsUsedInFile` for types/interfaces used only in their own file — reduces noise without hiding issues
- Use `includeEntryExports: true` for private/self-contained packages to check unused exports in entry files
- Use JSDoc tags like `@internal` or `@lintignore` to tag exports you want to exclude
- Define `tags` in the config to filter tagged exports, e.g. `{ "tags": ["-lintignore"] }`

### 6. Plugins

- Knip has plugins for Vite, Vitest, Playwright, Next.js, Remix, Astro, Svelte and more
- Plugins auto-detect entry files and config — never duplicate them in the workspace `entry`
- Disable a plugin with `false`, e.g. `{ "webpack": false }`
- Enable a plugin with `true`, e.g. `{ "playwright": true }`
- Override plugin config/entry, e.g. `{ "mocha": { "config": "config/mocha.config.js", "entry": ["/*.spec.js"] } }`

### 7. Safe Usage

- Never run `knip --fix` until the config is settled with no config hints — it can delete code actually in use
- Always review reported issues by eye before fixing
- Use `--include` or `--exclude` to filter issue types, e.g. `knip --include files,dependencies`
- Use `rules` in the config to set severity: `"error"`, `"warn"`, `"off"`, e.g. `{ "rules": { "files": "warn", "duplicates": "off" } }`

- Use /follow-monorepo when the project is a monorepo
- Use /follow-tasks to wire knip into task runner scripts
- Use /run-scan for additional auditing

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `knip.json` fully configured per official best practices
- No config hints
- Scripts for default, production, and strict modes ready to use
- No unused files, dependencies, or exports (or only necessary targeted ignores)
- Every workspace in the monorepo analyzed completely
