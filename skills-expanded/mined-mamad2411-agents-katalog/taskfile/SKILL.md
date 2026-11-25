---
name: taskfile
description: Build, debug, and refactor `Taskfile.yml` or `Taskfile.yaml` automation using go-task and the `task` CLI. Use this skill whenever the user mentions Taskfile, go-task, `task`, task dependencies, includes, variables, templates, `sources` or `generates` caching, taskfiles split across directories, or migrating Makefiles or npm scripts to Task.
version: 1.0.0
source: https://taskfile.dev/llms-full.txt
license: MIT
---

# Taskfile Skill

Use this skill to create production-grade `Taskfile.yml` automation for local dev, CI, and monorepos.

Task is a YAML task runner with:
- dependency graphs (`deps`)
- templating via Go `text/template` + slim-sprig functions
- incremental execution (`sources`, `generates`, `status`, `method`)
- task composition via `includes`

## What to do first

1. Identify the user's goal (dev workflow, build, test, release, codegen, deploy).
2. Inspect existing `Taskfile.yml` and project scripts (`package.json`, Makefile, CI configs).
3. Decide whether to:
   - add tasks to existing Taskfile,
   - split into included Taskfiles,
   - or bootstrap a fresh Taskfile.
4. Prefer small, composable tasks with clear `desc` and predictable variables.

## Core implementation rules

- Keep root schema on `version: '3'` unless user needs stricter semver gating.
- Use `desc` on user-facing tasks so `task --list` is useful.
- Use `internal: true` for helper tasks not meant for direct invocation.
- Use `deps` for parallelizable prerequisites; use `cmds: - task: ...` for ordered execution.
- Use `requires.vars` for mandatory inputs and enum constraints for safety.
- Use `sources` + `generates` (or `status`) to skip unnecessary work.
- Use `preconditions` for hard-fail checks (missing tools/files/env).
- Use `if` to conditionally skip tasks without failing.
- Use task-level `dir` when running in subfolders/services.

## Output expectations

When writing or editing Taskfiles:
- return valid YAML that can run as-is;
- include concise comments only for non-obvious behavior;
- include at least one `default` or clearly documented entrypoint task when useful;
- include practical examples of calling tasks (with variables and `--` CLI args) in your response.

## Routing guide

- Schema keys and valid shapes: `references/schema-and-model.md`
- Templating and special variables: `references/templating-and-vars.md`
- Execution model, caching, and reliability: `references/execution-patterns.md`
- CLI flags, debug flow, and troubleshooting: `references/cli-and-debugging.md`
- Ready-to-copy Taskfiles: `examples/basic-taskfile.yml`, `examples/monorepo-taskfile.yml`

## High-value patterns to prefer

### 1) Safe deploy tasks
- `prompt` for confirmation
- `requires.vars` for environment selection
- `preconditions` for required secrets/tools

### 2) Fast local dev loops
- a top-level `dev` task that fans out to service tasks
- `watch` where appropriate
- clear task aliases for common commands

### 3) Incremental builds/codegen
- `sources` and `generates` for deterministic re-runs
- `method: checksum` for content-sensitive workflows
- `method: timestamp` only when filesystem mtime behavior is desired

### 4) Monorepo composition
- `includes` with namespaces
- `flatten` only when naming collisions are controlled
- `excludes` for clashing task names

## Anti-patterns to avoid

- Giant single tasks that hide multiple concerns.
- Relying on shell state shared between separate commands.
- Omitting `desc` on user-facing tasks.
- Using `--force` routinely instead of modeling `sources`/`status` correctly.
- Putting sensitive values directly in Taskfiles when env/dotenv is more appropriate.

## Minimal quality checklist

Before finishing, verify:
- `task --list` is readable and meaningful.
- Required variables are enforced (`requires`).
- Tasks run from expected directories (`dir`, `USER_WORKING_DIR` when needed).
- Incremental tasks have correct invalidation (`sources`/`generates`/`status`).
- Task names and namespaces are consistent and predictable.
