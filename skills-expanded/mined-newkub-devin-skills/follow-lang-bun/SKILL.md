---
name: follow-lang-bun
description: Develop JS/TS with the Bun toolkit — runtime, package manager, test runner, bundler
argument-hint: "[scope|setup-project|migrate-from-nodejs]"
related:
  - use-bun-native-api
  - use-bun-shell
  - follow-lang-javascript
  - follow-lang-typescript
  - follow-create-bun-cli
  - follow-tool-bunup
  - follow-best-practice
  - setup-cicd
  - use-scripts
  - deep-research
---

## Goal

Develop JavaScript/TypeScript projects on Bun, fast and per official best practices

## Scope

For creating or improving projects that run on the Bun runtime, single package and monorepo. Bun is one all-in-one binary: runtime (drop-in Node.js replacement), package manager, test runner, and bundler. Package: `SKILL.md` entry + `references/toolchain.md` (ecosystem-tool table) + `workflows/` — dispatch: `setup-project` → `workflows/setup-project/SKILL.md`, `migrate-from-nodejs` → `workflows/migrate-from-nodejs/SKILL.md`; verify the current Bun version and features via `/deep-research` at use time (official docs: https://bun.com/docs)

## Execute

### 1. Install And Setup

> Goal: install Bun and verify the version

1. Install with `mise use -g bun` first; fall back to the install script or a package manager only if mise is unavailable
2. Verify with `bun --version` and `bun --revision`
3. Upgrade with `bun upgrade` (or `bun upgrade <version>` to pin); `bun upgrade --canary`/`--stable` for channels
4. Run `/deep-research` + `/follow-best-practice` to note current major-version features and the latest Bun practices before using new APIs (`Bun.Image`, `Bun.WebView`, HTTP/2 in `Bun.serve`, parallel test/run, supply-chain flags)

### 2. Create Project

> Goal: scaffold with the correct template

1. New project → run the workflow `workflows/setup-project/SKILL.md` (argument `setup-project`): `bun init`/`bun create`, directory layout, `package.json` scripts, `bunfig.toml` skeleton, tsconfig, verify, git hygiene
2. App-type scaffold (web, CLI, bot, plugin) → dispatch the matching `/follow-create-*` skill instead
3. Moving from a Node.js project → run the workflow `workflows/migrate-from-nodejs/SKILL.md` (argument `migrate-from-nodejs`)

### 3. Manage Packages

> Goal: manage dependencies with the Bun package manager

1. `bun install` (`--frozen-lockfile`/`bun ci` in CI, `--linker hoisted|isolated`, `--filter <pat>`), `bun add <pkg>` (`-d`, `-g`, `-E`, `--optional`, `--peer`, `--minimum-release-age <s>`), `bun remove`, `bun update [--latest|-i]`
2. Health: `bun outdated`, `bun why <pkg>`, `bun info <pkg>`, `bun audit` (`bun audit fix`); maintenance: `bun dedupe`, `bun prune`
3. Extras: `bun link`/`unlink`, `bun publish` (`--tag`, `--access`, `--provenance`, `--dry-run`), `bun patch <pkg>` + `bun patch --commit`, `bun pm ls|cache|trust|untrusted|migrate`
4. Monorepo: `workspaces` in `package.json`, `bun install --filter`, `bun run --filter <pkg> <script>`, `catalog:` for shared versions

### 4. Run And Develop

> Goal: run and develop on the Bun runtime

1. `bun run <file>` or `bun <file>` — `.ts`/`.tsx`/`.jsx` run directly, no transpile step; flags `--watch`, `--hot`, `--smol`, `-r/--preload`
2. `bun run <script>` for package.json scripts; `bunx <pkg>` for one-off binaries (`-b` forces Bun runtime)
3. Monorepo: `bun run --workspaces <script>`, `bun --parallel|--sequential <script>`
4. `.env` is auto-loaded (never add `dotenv`); disable via `env = false` in `bunfig.toml`
5. `bun exec <cmd>` for one-line shell, `bun repl` for a REPL session

### 5. Test

> Goal: write and run tests with the built-in runner

1. `import { describe, test, expect } from "bun:test"` — Jest-compatible (`mock`, `mock.module`, `spyOn`, snapshots, `test.each`, `test.concurrent`, `setSystemTime`)
2. `bun test` auto-discovers `*.test.*`, `*_test.*`, `*.spec.*`; use `--watch`, `--coverage`, `--parallel` (files across threads), `--bail [n]`, `--timeout <ms>`, `-t <pattern>`, `--rerun-each <n>` (flaky detection), `--update-snapshots`, `--reporter=junit --reporter-outfile` for CI
3. Configure `[test]` in `bunfig.toml`: `root`, `preload`, `coverage`, `coverageThreshold`, `coverageReporter`, `randomize`
4. DOM tests: pair with `happy-dom`/`jsdom` via `[test] preload`

### 6. Bundle And Build

> Goal: bundle for browser/server or compile to a binary

1. `bun build <entry>` — `--target browser|bun|node`, `--format esm|cjs|iife`, `--outdir`, `--splitting`, `--minify`, `--sourcemap`, `--define`, `--external`, `--packages external|bundle`
2. `bun build --compile <file>` for a standalone executable
3. Set defaults in the `[build]` section of `bunfig.toml`
4. Publishing a library → use `/follow-tool-bunup`, not raw `bun build`

### 7. Configure

> Goal: keep configuration in the right files

1. `bunfig.toml` sections: `[install]` (`minimumReleaseAge`, `exact`), `[test]`, `[build]`, runtime/env options — the single config for the Bun toolchain
2. `package.json` stays the source of truth for scripts, dependencies, workspaces, `trustedDependencies`, `overrides`/`resolutions`
3. TypeScript: `bun add -d bun-types typescript` and a bundler-style `tsconfig.json` — `"moduleResolution": "bundler"`, `"target"/"lib": "ESNext"`, `"module": "Preserve"`, `"noEmit": true`, `"verbatimModuleSyntax": true`, `"allowImportingTsExtensions": true`, `strict`, `"types": ["bun-types"]`

### 8. Use Bun APIs

> Goal: use Bun native APIs in code

1. Run `/use-bun-native-api` for the full API catalog (`Bun.serve`, `Bun.file`, `Bun.sql`, `Bun.spawn`, `$` shell, etc.)
2. Use `/use-bun-shell` for the `$` shell template literal
3. Building a CLI → run `/follow-create-bun-cli`

### 9. Verify

> Goal: confirm the project fully works

1. `bun run <entry>` starts; `bun test` passes; `bun build <entry>` succeeds
2. `bun install --frozen-lockfile` confirms the lockfile matches `package.json`
3. Typecheck with `bunx tsc --noEmit` (Bun strips types at runtime, it does not check them)
4. On errors → run `/resolve-errors`

### 10. Migrate From Node.js (If Applicable)

> Goal: move a Node.js project to Bun safely and reversibly

1. Run the workflow `workflows/migrate-from-nodejs/SKILL.md` (argument `migrate-from-nodejs`): `bun pm migrate`, script rewrites, `trustedDependencies`, compatibility checklist, gradual adoption, verify, rollback

## Rules

### 1. Runtime

- Tool inventory → `references/toolchain.md`; scaffold and Node.js migration → `workflows/`
- Bun is a drop-in Node.js replacement — supports `node:*` modules and Node globals (`process`, `Buffer`); prefer Web-standard APIs (`fetch`, `WebSocket`, `ReadableStream`) and `Bun.*` where they win
- TS/JSX run directly (transpile-only, no typecheck at runtime); avoid `const enum`/`import =` (not type-aware)
- Never add `dotenv` (`.env` auto-loads); ESM by default

### 2. Package Management

- Never switch to npm/pnpm/yarn inside a project with a `bun.lock`; commit `bun.lock` (text format, diff-friendly); never edit it by hand
- Dependency lifecycle scripts don't run unless listed in `trustedDependencies`
- Install strategy: `isolated` for new monorepos (blocks phantom dependencies), `hoisted` for single packages
- Supply-chain protection: `--minimum-release-age` / `[install] minimumReleaseAge`; CI uses `bun ci`

### 3. Project Configuration

- `bunfig.toml` is the only toolchain config — don't duplicate settings elsewhere; `package.json` remains the dependency/script truth
- Use `catalog:` in workspaces for shared versions; `overrides`/`resolutions` for transitive fixes

### 4. Quality

- Tests via `bun:test`; CI runs `bun install && bunx tsc --noEmit && bun test --coverage` with a `coverageThreshold` in `bunfig.toml`
- Use `bun run --bun` when a script's shebang points at node but must run on Bun

### 5. Related Skills

- `/use-bun-native-api` for `Bun.*` + Web-standard catalog; `/use-bun-shell` for `$`; `/follow-create-bun-cli` for CLIs; `/follow-tool-bunup` for library bundling; `/follow-lang-typescript` and `/follow-lang-javascript` for the language; `/setup-cicd` for CI; `/use-scripts` for automation

## Expected Outcome

- Bun project set up per official conventions with a committed `bun.lock`
- TS/JSX run with no build step; tests pass via `bun test` with coverage
- Builds/compiles succeed via `bun build`; typecheck passes via `tsc --noEmit`
- `bunfig.toml` covers runtime, install, test, and build configuration
- Bun native APIs used appropriately through `/use-bun-native-api`
