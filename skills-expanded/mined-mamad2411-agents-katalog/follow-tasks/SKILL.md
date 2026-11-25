---
name: follow-tasks
description: Set up scripts in package.json, Cargo.toml, or moon.yml per the standard
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - run-test
  - run-check
  - run-verify
  - run-scan
  - run-lint
  - run-typecheck
  - run-build
  - run-all-tasks
  - use-scripts
  - follow-monorepo
  - follow-tool-moonrepo
  - deep-review-codebase
  - update-version-to-latest

---
## Goal

Set up scripts in `package.json` or `Cargo.toml` per the Minimal, Standard, Complete tiers

## Scope

Setting up scripts for packages and workspaces in a monorepo; excludes hand-writing config files (use `/deep-review-codebase`); coordinates with `/run-scan`, `/run-lint`, `/run-typecheck`, `/run-build`, `/run-test` (coverage) to execute the configured scripts; `/run-all-tasks` runs the full task suite defined here

## Execute

### 1. Check Prerequisites

> Goal: check the project structure and tools before configuring scripts

1. Confirm `package.json` or `Cargo.toml` exists — missing → stop and report
2. Check for a monorepo (multiple `package.json`, workspace config, git submodules) — if it's a monorepo, run `/follow-monorepo` first
   - If `.moon/workspace.yml` or `moon.yml` exists → run `/follow-tool-moonrepo` first, then use moonrepo mode (see Rules §3)
3. Confirm the tools are installed: Node.js/Bun (`biome`, `vitest` or `bun test`), Rust (`cargo-nextest`, `cargo-llvm-cov`), Python (`pytest`, `ruff`), Go (`go test`, `golangci-lint`)
4. If a required tool is missing → stop and report

### 2. Update Dependencies

> Goal: identify the package manager and update dependencies per ecosystem

1. Identify the package manager (`bun`, `npm`, `pnpm`, `yarn`, `cargo`, `pip`, `go`)
Latest: `taze@21.1.0`, `lefthook@2.1.14` (verified 2026-09-16)

2. For Node.js/Bun → run `/follow-tool-taze` to set up Taze for dependency updates
3. For tools managed by mise → run `mise upgrade` to update dev tools (e.g. `bun`, `gitleaks`, `hk`); to also bump versions in `mise.toml` → use `mise upgrade --bump`
4. Update per ecosystem: Node.js/Bun uses `taze` (Root Only), Rust uses `cargo update`, Python uses `pip install -U`, Go uses `go get -u ./... && go mod tidy`
5. After setup → run `/update-version-to-latest` to always bump all dependencies to latest
6. For Bun monorepos: `taze` and `lefthook install` must live only in the root `package.json` — workspace packages have no `prepare` script — root: `"prepare": "bunx taze -r -w && bunx lefthook install"` (never `-i` in `prepare` — interactive mode hangs in CI; use `-i` only in the manually run `deps:update`)
7. If the update fails → retry (max 3 → stop/report)

### 3. Select Template Level

> Goal: pick the scripts tier by project size and complexity

1. Assess the project size and testing/deployment needs
2. Choose the tier per Rules section 1: Minimal (every project), Standard (testing + deps management), Complete (infra/tooling team)
3. If unsure → start with Minimal and extend later

### 4. Apply Scripts

> Goal: configure scripts in every workspace per the chosen tech stack and template level

1. Pick commands from [references/scripts-tables.md](references/scripts-tables.md) per tech stack — JS/Bun edits `package.json` directly; Rust/Python/Go use a task runner per the Script Mechanism (`justfile`, `cargo-make`, `xtask`, `Makefile`, `poe`, `Taskfile.yml`)
2. Run `/use-scripts` to apply — single workspace: edit the manifest/task file directly; multiple workspaces: run `/follow-monorepo` first
3. If the operation touches > 10 files → use `/use-scripts` for the batch update
4. If applying fails → retry (max 3 → stop/report)

### 5. Setup Config And Secrets

> Goal: configure config files and secrets management together

1. `/deep-review-codebase` per the detected tech stack; check whether `.infisical.json` exists
2. If `.infisical.json` exists or a secret manager is in use → run `/follow-secret-manager` to set up secrets scripts
3. Ensure scripts that need secrets (`dev`, `build`, `deploy`) are wrapped with `infisical run -- <command>` — add root scripts `secrets:dev`, `secrets:build`, `secrets:export`, `secrets:run` (table in the reference)
4. Confirm `INFISICAL_TOKEN` is set in CI/CD — if missing → report and request it be set
5. Run only the necessary workflows, not every one — if the config fails → retry (max 3 → stop/report)

### 6. Validate

> Goal: check scripts syntax and confirm the commands really run

1. Check the scripts syntax in `package.json` or the task runner file — invalid syntax → fix and recheck (max 3 → stop)
2. Confirm `check` script = `format && lint && typecheck && scan` (format before lint) and `verify` = `check && test && build` for small projects; large projects' `verify` at least `check && test` — `ci` must be read-only via `format:check`, not `format`
3. Run `/run-test all` to execute unit, integration, e2e, coverage
4. Test-run `bun run verify` — if it fails → fix and retry (max 3 → stop/report)
5. If the project has a `tools/review-codebase` workspace → run `bun run review-codebase` for a first codebase review — if it fails → use `/deep-review-codebase` to create/update the CLI, then retry

## Rules

### 1. Scripts Levels And Root Only

Pick the tier by project size and complexity
- Minimal (Default): dev, build, typecheck, lint, format, test, scan, check, verify, ci - fits most projects
- Standard: Minimal + test:watch, test:coverage, deps:analyze, clean, security, db scripts, predeploy, deploy:staging - fits projects needing extra testing and dependency management
- Complete: Standard + build:watch, typecheck:watch, test:integration, test:e2e, benchmarks, prerelease, db:studio - fits infra/tooling teams

For Bun monorepos:
- `taze` and `lefthook install` must live only in the root `package.json`
- Workspace packages have no `prepare` script
- Root `package.json`: `"prepare": "bunx taze -r -w && bunx lefthook install"` — never `-i` in `prepare` (interactive hangs in CI); `-i` only in the manually run `deps:update`

### 2. Script Tables

All command-lookup tables live in [references/scripts-tables.md](references/scripts-tables.md) — the single source of truth covering:

- `Script Mechanism` — `Cargo.toml`/Python/Go have no built-in script runner → use `justfile`, `cargo-make`, `xtask`, `Makefile`, `poe`, `nox`, `Taskfile.yml` (never put scripts in `Cargo.toml`)
- `Bun-Native Alternatives` — `bun test`, `bun audit`, `bun ci`, `bun run --workspaces`, `bun --filter`
- `Required / Watch / Testing / Deps / Database / Prerelease+Bench / Security / Deploy / Docs` — every stack covered: Bun, Nuxt (`nuxi` commands), Next.js, Solid Start, SvelteKit, Tauri, Rust, Python, Go
- `Secrets, Monorepo, Review CLI, Other Ecosystems` (Kotlin, PHP, Swift, Zig, Lua, C#)

Key rules tied to the tables:
- `check` = `format && lint && typecheck && scan` (format writes — local dev)
- `ci` = `format:check && lint && typecheck && scan && test && build` (read-only — no file mutation in the pipeline)
- `verify` = `check && test && build` (small projects); large projects at least `check && test`
- `release` does not belong in the package manifest — release via CI/CD workflows on a tag or `/run-release`
- If a `tools/review-codebase` workspace exists → add the `review-codebase` scripts (table in the reference) and run `bun run review-codebase` once — if it fails, use `/deep-review-codebase`

### 3. Moonrepo Mode

If the project uses moonrepo (has `.moon/workspace.yml` or `moon.yml`):

- Use `moon.yml` instead of plain `package.json` scripts — edit `.moon/tasks/all.yml` for shared tasks such as `build`, `test`, `typecheck`, `lint`
- Each workspace's `moon.yml` defines only project-specific tasks — don't repeat `project` in every file; rely on `id` and `.moon/tasks/all.yml`
- Have `package.json` scripts point at `moon run <task>` only where necessary
- Never define the same task in both `moon.yml` and `package.json` scripts — `package.json` holds only scripts not in `moon.yml`
- Validate with `moon run :check`
- For full details follow `/follow-tool-moonrepo`

- Use /open-web-for-config-secret if needed (tasks)
- Use /run-check if needed
- Use /run-verify if needed

## Expected Outcome

- `package.json` or the task runner file carries the scripts of the chosen template (state change)
- Scripts match the tech stack (tables in [references/scripts-tables.md](references/scripts-tables.md))
- The `verify` and `ci` pipelines work correctly — `bun run verify` passes, `ci` is read-only
- If `tools/review-codebase` exists, `bun run review-codebase` passes or the failure cause is known
- With Infisical: root `package.json` has the `secrets:*` scripts and `INFISICAL_TOKEN` is set in CI/CD
