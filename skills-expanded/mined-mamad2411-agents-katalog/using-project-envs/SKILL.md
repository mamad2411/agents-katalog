---
name: using-project-envs
description: Sets up and uses per-repo development environments on a managed dev machine — personal Devbox overlays for third-party repos, direnv auto-activation, and direnv exec for coding agents and non-interactive launches. Use when starting work in a checkout, cloning a repo, launching an agent (claude/codex) inside a project, when tools are missing in a repo, or when a repo lacks devbox/devcontainer config that shouldn't be committed upstream.
---

# Using project environments

Two modes, chosen by ownership:

- **In-repo** (repos you control, and the default for new projects with no
  origin remote): committable `devbox.json` + `.envrc` in the repo itself.
  Works out of the box on any machine, nothing to migrate later.
- **Overlay** (third-party repos, the default when an origin exists): env
  config stored centrally in
  `$SERVER_CONFIG_DIR/environments/<host>/<owner>/<repo>/`, activated by a
  repo-local `.envrc` excluded via `.git/info/exclude` (never committed,
  never in `.gitignore` — that file is upstream's).

`repo-env setup` picks the default from the remote; override with
`--in-repo` / `--overlay`. For a repo you control that already has an
origin, prefer `--in-repo`.

The `repo-env` tool (Rust, in this repo under `tools/repo-env/`) automates
the mapping; install once with
`cargo install --git https://github.com/gabrielgrant/development-machine-skills repo-env`.

## Entering a repo for the first time

```bash
cd ~/repos/some-project
repo-env setup        # offers git init if needed (--git-init to skip the
                      # prompt); then in-repo or overlay per the rules above
# in-repo:  devbox add <pkgs>            then commit devbox.json/.lock + .envrc
# overlay:  devbox add <pkgs> --config "$(repo-env path)"
#           then commit $SERVER_CONFIG_DIR
```

After that, `cd` into the repo auto-activates (direnv hook). `repo-env
doctor` verifies a checkout, including a stale overlay key after a remote
change. Without repo-env, the manual overlay equivalent is an `.envrc`
containing `use_personal_devbox <host>/<owner>/<repo>` (helper installed
by setting-up-dev-machine).

## Runtime version authority

One authority per runtime — never two declarations:

| Project has | Authority |
|---|---|
| `.nvmrc` | nvm (the `.envrc` runs `nvm use` after devbox) |
| `rust-toolchain.toml` | rustup (devbox may supply rustup itself) |
| `devbox.json` pinning a runtime | devbox |
| `packageManager` field | corepack |
| nothing | pin in your overlay's devbox.json |

## Launching agents / non-interactive commands

An interactive shell that has `cd`-ed into the repo has the environment,
and **every child process inherits it** — launching `claude` or `codex`
from a repo shell (e.g. inside tmux, with `claude --remote-control` for
remote steering) needs nothing special.

direnv's hook only fires around interactive prompts, so anything that
*bypasses* an interactive repo shell — systemd units, an agent portal,
editor tasks, cron, or a command run from outside the repo — must go
through:

```bash
repo-env exec claude          # = direnv exec <git-root> claude
repo-env exec npm test
```

The test is "did this process's ancestry pass through an interactive
shell prompt inside the repo?" — if unsure, `repo-env exec` is always
correct (direnv makes it a no-op when the env is already loaded).

## Devbox overlay vs Dev Container

Default to the Devbox overlay. Reach for a Dev Container when you need OS
isolation, a specific distro/libc, compose-based services, or separated
agent credentials/home. Keep external devcontainer configs in the same
overlay dir (`.devcontainer/devcontainer.json`) and run
`devcontainer up --workspace-folder <repo> --config <overlay>/.devcontainer/devcontainer.json`.

## Upstreaming an overlay

Overlays are stored upstream-shaped, so proposing them is a copy:
`cp "$(repo-env path)"/devbox.json . && cp "$(repo-env path)"/devbox.lock .`
on a clean branch, review, PR. Don't use a long-lived personal branch in
the upstream repo as your environment store — it entangles env commits
with work branches and syncs poorly across machines.
