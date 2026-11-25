---
name: follow-tool-mise-config-tools
description: Configure `mise.toml` — tools versions, tasks, env vars without clobbering existing config
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - use-scripts
  - run-verify
---

## Goal

Configure and edit the project's `mise.toml` — pin tool versions, define tasks, configure env vars — merging with the existing config, not overwriting

## Scope

Use when adding/changing tools, tasks, or env in the mise config — install/activation lives in `workflows/setup-mise/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: read the existing config before editing

1. Read `mise.toml` (project), `mise.local.toml` (local overrides, not committed), and `~/.config/mise/config.toml` (global)
2. Run `mise list` to see installed tools — compare with the config
3. If no `mise.toml` exists → create it at the project root (commit to the repo)

### 2. Configure Tools

> Goal: pin tool versions in `[tools]`

1. Use `mise use <tool>@<version>` to add a tool to the config automatically — preferred over hand-editing the file
2. Or define entries in `[tools]` directly, e.g. `node = "24"`, `python = "3.13"`, `bun = "latest"`
3. Run `mise install` to install every tool in the config
4. Use `mise up` to update tools per version constraints; `mise prune` removes unused versions

### 3. Configure Environment

> Goal: set env vars in `[env]`

1. Add an `[env]` section — use `_ = { VAR = "value" }` to set values directly
2. Use `_.file = ".env.local"` to load from an env file (non-sensitive only)
3. Never commit secrets into `mise.toml` — use `/follow-secret-manager` for secrets
4. Run `mise env` to check the env vars that will be exported; use `mise exec -- <command>` to run in the mise env

### 4. Define Tasks

> Goal: create tasks in `[tasks.<name>]`

1. Add `[tasks.<name>]` with `run = "<command>"` — clear names: `build`, `test`, `lint`, `dev`
2. Use `depends = ["build"]` for task dependencies
3. Use `sources` and `outputs` when caching is wanted
4. Don't define tasks that duplicate package-manager scripts without reason
5. Run `mise run <task>` or `mise <task>`; list them with `mise tasks`

### 5. Verify

> Goal: confirm the config works

1. Run `mise doctor` and `mise list` — tools installed per the config
2. `cd` into the project → run `mise env` — env vars load correctly
3. Smoke-test `mise run <task>` — if it breaks → revert the changed keys and report the diff
4. Passing → a short before/after report via `/report-before-after`

## Rules

### 1. Config Files

- `mise.toml` at the project root — committed to the repo
- `mise.local.toml` for local overrides — not committed
- Use `mise use` instead of manual edits when possible; merge, don't clobber

### 2. Versions

- Pin versions for consistency; `latest` only when auto-update is wanted
- Use `mise use -g <tool>` for global tools per `global_rules` — watch for collisions with project versions

### 3. Secrets

- Never put secrets in `mise.toml` — point `_.file` at an untracked env file or use `/follow-secret-manager`
- Check `mise env` before running important commands

## Expected Outcome

- `mise.toml` holds the `[tools]`, `[env]`, `[tasks]` the project needs
- Tools installed at pinned versions; env loads automatically
- `mise run <task>` works; setup is repeatable on another machine
