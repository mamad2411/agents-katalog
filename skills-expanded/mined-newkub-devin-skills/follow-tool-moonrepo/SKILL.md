---
name: follow-tool-moonrepo
description: Use moonrepo for monorepo builds, tasks, and project boundaries across stacks
argument-hint: "[scope]"
related:
  - follow-monorepo
  - follow-tool-mise
  - follow-tool-github-actions
  - use-subagents
  - run-build
  - run-lint
  - run-test
  - run-verify
  - deep-validate
  - follow-tool-hk
---

## Goal

Set up and use moonrepo for a monorepo with `.moon/` configuration, task graph, and project boundaries

## Scope

For projects that choose moonrepo as the monorepo orchestrator instead of turborepo; supports Bun, Node, Rust

- If the repo still uses turborepo → use `/follow-tool-turborepo` (or migrate per Step 5)
- If the job is tool version/env management rather than task orchestration → use `/follow-tool-mise`

## Execute

### Workflows

| Topic | Workflow |-------|----------| Install moon, `moon init`, `.moon/` workspace layout | `workflows/setup-moonrepo/SKILL.md` | `tasks`, `deps`, `inputs`/`outputs`, `moon.yml` per project | `workflows/config-pipeline/SKILL.md` | Cache tuning, `--affected` targets | `workflows/optimize-cache/SKILL.md` | `moon ci` — CI pipeline, `runInCI`, sharding, reports | `workflows/run-ci/SKILL.md` 
### Subagents

- Use the `project-configurator` profile (inline below in the `## Subagents` section) when configuring/verifying `moon.yml` across many projects at once — spawn per `project-path` via `/use-subagents` with `mode` = `configure` or `verify`

### 1. Install moon

> Goal: install the moon CLI on the environment

1. Install with the appropriate package manager:
   - Bun project: `bun add -D @moonrepo/cli`
   - If the project doesn't use Bun: use its package manager (npm, pnpm, yarn)
   - PowerShell: `irm https://moonrepo.dev/install/moon.ps1 | iex`
   - macOS/Linux/WSL: `bash <(curl -fsSL https://moonrepo.dev/install/moon.sh)`
   - proto: `proto install moon`
   - mise: `mise use -g moon` (if `mise` is in `.tool-versions` or `mise.toml`)
2. Check the version with `moon --version` (latest `2.5.5`, verified 2026-09-16)
3. To let other projects in this repo use moon → use the workspace package manager (default: `bun add -D @moonrepo/cli`)
4. See more details in 

### 2. Identify Workspace

> Goal: confirm the project uses moonrepo

1. Check for `.moon/workspace.yml` or `moon.yml`
2. Read the root manifests: `package.json` scripts for JS/Bun, `Cargo.toml` workspace for Rust
3. Identify the monorepo's projects from the `.moon/workspace.yml` globs
4. Record the project list (package = JS/Bun, crate = Rust)

### 3. Configure Workspace

> Goal: set up the moonrepo workspace

1. Create/update `.moon/workspace.yml` with project globs
   - JS/Bun: `packages/*` or `apps/*`
   - Rust: `crates/*`
2. Create/update `.moon/toolchains.yml` per stack (Bun, Node, Rust)
3. Create `.moon/tasks/all.yml` for shared task config
4. Check the `moon.yml` of every project

### 4. Define Tasks

> Goal: define tasks in moonrepo

1. Use the same task names across workspaces
2. JS/Bun: use `package.json` scripts (`build`, `dev`, `test`, `lint`, `typecheck`, `scan`)
3. Rust: use `cargo build`, `cargo test`, `cargo clippy`
4. Set `deps` (`^build`) correctly
5. Set `outputs` for build tasks
6. Set `inputs` and `options` as needed

### 5. Migrate From Turborepo

> Goal: move from turborepo to moonrepo

1. Try the built-in migration first: `moon ext migrate-turborepo` (or `moon ext migrate-nx` for Nx)
2. Delete `turbo.json`
3. Remove `turbo` from `package.json` devDependencies
4. Change `package.json` scripts from `turbo run` to `moon run`
5. Update README, AGENTS, and docs to state moonrepo
6. Update `rules/` (ast-grep) and skills that reference turborepo

### 6. Integrate CI

> Goal: the CI pipeline uses `moon ci` correctly

1. Use `moon ci` instead of `moon run` in CI — it runs only affected tasks with `runInCI`
2. Set `runInCI: false` for long-running tasks (`dev`, `start`, `serve` default to off)
3. Full git history is required — never shallow clone (use `filter: 'blob:none'`)
4. Follow `workflows/run-ci/SKILL.md` for provider config, sharding, and reports

### 7. Configure VCS Hooks (Optional)

> Goal: git hooks via the built-in `vcs.hooks` — no external hook manager needed

1. Add `vcs.hooks` to `.moon/workspace.yml` (requires moon v1.9+):
   ```yaml
   vcs:
     hooks:
       pre-commit:
         - 'moon run :lint :format --affected --status=staged'
       pre-push:
         - 'moon run :typecheck :test --affected'
     sync: true
   ```
2. `sync: true` = auto-generate + link hooks on every task run; otherwise contributors opt in with `moon sync hooks` themselves
3. Generated scripts live in `.moon/hooks` (or `.config/moon/hooks`) — commit or ignore, either is fine; easy to audit/test since moon sets `core.hooksPath` there
4. Use `--affected` + `--status=staged` to keep hooks fast — moon already knows the task graph + cache
5. `/follow-tool-hk` isn't needed — hk adds value only for parallel staged-file linting, non-moon hook steps, or one hook config across non-moon repos

### 8. Verify

> Goal: confirm moonrepo works

1. Run `moon check` or `moon run :check`
2. Run `moon run :build` to verify the project graph
3. Run `moon ci` on a test branch to confirm affected detection
4. Check that no `turbo.json` or `turbo` dependencies remain
5. Inspect graph/tasks with `moon project <id>`, `moon task <id>:<task>`, `moon query projects`, `moon query tasks` when debugging structure
6. If generated hook scripts exist → verify `git config core.hooksPath` points at `.moon/hooks`
7. Run `/deep-validate` to verify the setup

## Rules

### 1. Prefer moonrepo For This Codebase

- Use `moon` for task orchestration
- Don't add `turbo` dependencies back
- Use `moon run :<task>` in root scripts

### 2. Task Naming

- Use the same task names across workspaces
- Use kebab-case for task labels
- Avoid tasks without clear `deps`

### 3. Project Boundaries

- Define project globs in `.moon/workspace.yml`
- Use moonrepo's implicit project detection
- Don't overlap project boundaries
- JS/Bun project = package, Rust project = crate (Cargo package)
- Use `tags` in `moon.yml` + `dependsOn` for explicit boundaries — see `references/apis.md`

### 4. Git Hooks

- In a moon repo → `vcs.hooks` is always the default, not `/follow-tool-hk` — see Step 7
- Use `hk` only when: parallel staged-file linting moon commands can't do, hook steps that aren't moon tasks, or one hook config across non-moon repos

- Use /follow-monorepo if needed
- Use /follow-tool-mise if needed
- Use /follow-tool-github-actions if needed
- Use /use-subagents if needed
- Use /run-build if needed
- Use /run-lint if needed
- Use /run-test if needed
- Use /run-test all if needed
- Use /run-verify if needed
- Use /deep-validate if needed

## References

- [CLI reference](references/cli.md)
- See best-practices/ for recommended patterns and pitfalls

## Subagents

> Goal: independent work that can spawn in parallel — the profile lives in this section, no separate file

### project-configurator — configure or verify one project's `moon.yml` + task definitions in the monorepo

- **Inputs**: `project-path` (e.g. `apps/web`, `packages/ui`, `crates/cli`), `stack` (`bun`/`node`/`rust` — detect from the manifest if not given), `shared-config` (path to `.moon/tasks/all.yml` if present), `mode` (`configure` writes/edits moon.yml, `verify` only inspects and reports)
- **Tools**: `read`, `grep`, `find_file_by_name`, `exec` — every mode; `edit`/`write` only in mode `configure`
- **Execute**:
  1. Read the project's `package.json` scripts (JS/Bun) or `Cargo.toml` (Rust)
  2. Read `.moon/tasks/all.yml` and any shared config affecting the project
  3. Check the project's current `moon.yml` (if any)
  4. mode `configure`: write `moon.yml` with standard task names (`build`, `dev`, `test`, `lint`, `typecheck`, `check`), correct `deps` (`^build` for build), `outputs` for build tasks, `inputs` covering sources+configs, `runInCI: false` for dev/serve tasks
  5. mode `verify`: check task coverage, missing `deps`, missing `outputs`, `runInCI` violations, then report
  6. Run `moon project <name>` to confirm the project is detected correctly
- **Output**: an updated `moon.yml` (mode configure) or a verification report (mode verify) + a list of task issues: missing deps, missing outputs, wrong runInCI, naming drift
- **Constraints**: edit only the assigned project's `moon.yml` — never touch `.moon/` workspace config or other projects; follow the shared config's existing task names, don't invent new conventions; don't change `package.json`/`Cargo.toml` scripts — report them as findings instead; mode `verify` writes no files

## Expected Outcome

- Correct, complete `.moon/` configuration
- No `turbo.json` or `turbo` dependency
- Root scripts use `moon run`
- The project graph can build
- `moon ci` ready on the CI provider — affected detection + `runInCI` correct
- Supports JS/Bun packages and Rust crates
