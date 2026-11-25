---
name: orbit
description: Start, stop, restart and inspect the local services of a project run with orbit (an orbit.yaml next to the code, or the user mentions orbit). Use it to bring up the dev stack, check whether a service is running or healthy, read a service's logs to debug an error, restart a service after changing its code, apply edits to orbit.yaml, or run a project task.
---

# orbit

orbit supervises a project's local services (processes, Docker containers, `docker compose` services) declared
in `orbit.yaml`, respecting their dependencies. Drive it through its CLI from the project folder (or any folder
below it). The services run in a background daemon that the user's orbit TUI shares: whatever you do shows up
there, and the user may be watching.

Check that it applies: an `orbit.yaml` exists in the working directory or a parent, and `orbit --version` works.
This skill needs orbit 1.4 or later; on an older one, use `orbit daemon` as a background command instead of
`orbit up -d`, and drop `--json` from `orbit logs`.

## Never block

These never return. Do not run them as foreground commands:

- `orbit` / `orbit <dir>` / `orbit open`: the interactive TUI.
- `orbit up` without `-d`: streams logs until ctrl+c.
- `orbit logs -f`: follows forever. Use `-n` instead, or a timeout (`timeout 10 orbit logs api -f --json`).

## Workflow

1. **Look first**: `orbit status --json` (from another folder: `orbit status -p <name|path> --json`; `-p` works with every command that talks to a project). `"running": false` with exit code 1 just means nothing is running yet.
   Each service has a `status`: `stopped`, `waiting` (on dependencies, see `waitingOn`), `starting`, `running`,
   `healthy`, `unhealthy`, `stopping`, `exited`, `crashed` or `failed`, plus `error`, `health`, `restarts` and
   `exitCode` when they apply.
2. **Start what you need**: `orbit up -d [service|group…]` starts them (dependencies first) in the background and
   returns once they are ready; exit code 1 means some did not become ready. With no names it starts every
   autostart service.
3. **Read logs**: `orbit logs <service> -n 100 --json` prints one `{"service","stream","text"}` object per line
   (`stream` is `stdout`, `stderr` or `system`, orbit's own messages). Narrow it with `--grep <regex>`; for
   Docker services `--since 10m` also works.
4. **After changing a service's code**: `orbit ctl restart <service>` restarts it and waits until it is ready. Skip
   it when the service has `"watch": "active"` in its status: orbit restarts it on file changes by itself; wait a
   moment and check its status instead. Then confirm with `orbit status --json` and its logs.
5. **After editing `orbit.yaml`**: `orbit validate` (exit code 1 lists the errors), then `orbit ctl reload`, which
   restarts only the services that changed.
6. **Tasks** (migrations, seeds, tests the project declares): `orbit run` lists them,
   `orbit run <task> -- <args>` runs one in the foreground and returns its exit code.

`orbit ls` lists services, groups, tasks and profiles; `orbit graph` prints the dependency graph. Check the
dependents before stopping or restarting a service others depend on.

## Be a good guest

- The stack belongs to the user. Do not `orbit down`, `orbit ctl stop` or restart services you were not asked to
  touch, and leave running what you started unless the user asks you to stop it.
- Do not pass `--profile` / `--no-profiles` unless asked: the selection is remembered for the project and changes
  what the user's TUI runs too.
- Plugins run code with the user's permissions: do not install, upgrade, enable or remove one. `orbit plugin ls`
  shows what is installed; a plugin may add commands (`orbit <plugin> …`) and service types to `orbit.yaml`: use
  them when the user's task calls for it, as any other command.
- Do not edit `orbit.yaml` to work around a failing service without saying so; report what the logs show.

For every command and flag, and the JSON shapes, see [references/cli.md](references/cli.md).
