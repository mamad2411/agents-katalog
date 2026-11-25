---
name: follow-tool-moonrepo-config-pipeline
description: Configure moon tasks, deps, inputs/outputs and shared task config in `.moon/`
argument-hint: "[scope]"
related:
  - follow-monorepo
  - run-build
  - run-test
---

## Goal

Configure moonrepo's task pipeline — `tasks`, `deps`, `inputs`/`outputs`, shared config in `.moon/tasks/` and per-project `moon.yml` — without clobbering existing config

## Scope

Use when defining/changing tasks in moonrepo — it doesn't cover install/workspace init (see `workflows/setup-moonrepo/SKILL.md`) or cache tuning (see `workflows/optimize-cache/SKILL.md`)

## Execute

### 1. Read Current Config

> Goal: read the existing config before editing

1. Read `.moon/workspace.yml`, `.moon/toolchains.yml`, `.moon/tasks/*.yml`, and every project's `moon.yml`
2. Check `package.json` scripts (JS/Bun) and `Cargo.toml` (Rust) — task names must map to real scripts
3. If `.moon/` is not found → do `workflows/setup-moonrepo/SKILL.md` first

### 2. Define Shared Tasks

> Goal: define shared tasks in `.moon/tasks/all.yml`

1. Use the same task names across workspaces: `build`, `dev`, `test`, `lint`, `typecheck`, `check`
2. JS/Bun: map tasks to `package.json` scripts
3. Rust: map tasks to `cargo build`, `cargo test`, `cargo clippy`
4. Set `deps` correctly — `^build` for upstream dependencies
5. Set `inputs` and `outputs` for build tasks so cache hashes are correct

### 3. Per-Project Tasks

> Goal: override/extend per project with `moon.yml`

1. Create `moon.yml` in projects that need custom tasks
2. Define extra tasks or override shared config only for genuinely different keys — never duplicate shared config without need
3. Specify `outputs` of build tasks per tool used (`dist/**`, `target/**`, etc.)

### 4. Options And Boundaries

> Goal: set task options and project boundaries

1. Set `options` as needed — e.g. caching behavior, run mode for long-running tasks (check official docs for uncertain option names)
2. Use kebab-case for task labels
3. Verify the project globs in `.moon/workspace.yml` cover every project — JS/Bun = package, Rust = crate

### 5. Verify

> Goal: check the task graph is correct

1. Run `moon run :build` — verify the dependency order is correct
2. Run `moon check` or `moon run :check` to validate the config
3. Re-run to confirm a cache hit — if it breaks → revert the changed keys and report the diff

## Rules

### 1. Config Discipline

- Merge with the existing config — never overwrite a whole file unless necessary
- Shared behavior lives in `.moon/tasks/all.yml`; per-project overrides live only in `moon.yml`

### 2. Task Naming

- Use the same task names across workspaces
- Use kebab-case for task labels
- Avoid tasks without clear `deps`

### 3. Task Graph

- Use `^task` for upstream dependencies
- Don't create circular `deps`
- Don't overlap project boundaries

- Use /follow-monorepo if needed

## Expected Outcome

- `.moon/tasks/` and `moon.yml` have a correct task graph
- `moon run` executes the correct tasks in the correct dependency order
- Builds/tests get cache hits on unchanged inputs
