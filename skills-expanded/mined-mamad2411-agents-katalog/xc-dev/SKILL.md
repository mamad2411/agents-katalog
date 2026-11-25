---
name: xc-dev
description: Use for iOS / Xcode build, run, test, and simulator workflows in projects that have an `.xc-dev/` directory. Routes work through `xc-dev <task>` instead of raw `xcodebuild`.
---

# xc-dev

`xc-dev` is a Rust task runner for Xcode projects. It reads `.xc-dev/project.toml`,
`.xc-dev/simulator.toml`, and `.xc-dev/tasks.toml` and runs named tasks (`build`, `run`,
`test`, `test-package`, …) with `{{scheme}}` / `{{bundle_id}}` / `{{sim_id}}` /
`{{derived_data}}` / `{{git_branch}}` substituted in.

## When to use this skill

Activate when **all** of these are true:

- The user is doing iOS / Xcode work (build, run, test, install, launch, archive, log
  stream, etc.).
- The project has a `.xc-dev/` directory anywhere up from cwd (run
  `ls -d .xc-dev 2>/dev/null` or walk up; an existing `tasks.toml` is the dispositive
  signal).

Do **not** use this skill — fall back to generic Xcode tooling — when:

- The project has no `.xc-dev/` and the user isn't asking to set one up.

## Discovery first

Before assuming task names, list them:

```sh
xc-dev               # bare form is shorthand for `xc-dev :list`
xc-dev :list
```

For variables (scheme, bundle id, sim id, derived data path, git branch, …):

```sh
xc-dev :get scheme
xc-dev :get bundle_id
xc-dev :get sim_id
xc-dev :get derived_data
xc-dev :get sim.ipad.id      # qualified, non-default sim
xc-dev :get git_branch
```

To sanity-check the config and every task's variable references:

```sh
xc-dev :doctor
```

## Running tasks

```sh
xc-dev build
xc-dev build Release           # positional override of `args = ["config=Debug"]`
xc-dev test-package Networking
xc-dev -v build                # echo expanded command to stderr (handy for debugging)
```

Exit codes:
- `0` — success
- `1` — task error (config invalid, command failed, variable unresolved, …)
- `2` — CLI parse error (unknown built-in, missing flag value, …)

## When the task you need doesn't exist

**Prefer adding a task to `.xc-dev/tasks.toml`** rather than constructing an `xcodebuild`
invocation yourself. Two reasons:

1. The next person doing the same thing will benefit from the task being there.
2. The variables are already wired up — `{{scheme}}`, `{{derived_data}}`, etc. all
   resolve correctly, so you don't have to re-derive them.

Show the user the proposed task and ask before editing.

## Built-in verbs (cheat sheet)

| Verb | What |
|---|---|
| `xc-dev :proj init` | Scaffold `.xc-dev/` (autodetects scheme/bundle_id via `xcodebuild`) |
| `xc-dev :list` | List all tasks with their `desc` |
| `xc-dev :get <key>` | Print one variable |
| `xc-dev :doctor` | Sanity-check config + every task's vars + depends |

## Common patterns

**Boot + launch the default sim:**

```sh
xc-dev run     # if the user has set up the example `run` task
# else manually:
xcrun simctl boot $(xc-dev :get sim_id) 2>/dev/null || true
xcrun simctl install $(xc-dev :get sim_id) $(xc-dev :get app_path)
xcrun simctl launch $(xc-dev :get sim_id) $(xc-dev :get bundle_id)
```

**Inspect the app bundle that the build produced:**

```sh
ls "$(xc-dev :get app_path)"
```

**Per-worktree DerivedData:**

`{{derived_data}}` defaults to `{{xc_dev_dir}}/DerivedData`, so each git worktree has its
own build cache and they don't fight each other.

## Reference docs

If you need more detail than this skill provides, point the user at:

- `crates/xc-dev/docs/tasks.md` — full Task DSL reference
- `crates/xc-dev/docs/variables.md` — every built-in variable + resolution order
- `crates/xc-dev/docs/config.md` — TOML schemas
- `crates/xc-dev/docs/examples.md` — example task recipes

## Relationship to other skills

- **`xcodebuildmcp-cli`** — reserved for UI automation, log streaming, and interactive
  debugging that xc-dev doesn't cover.
