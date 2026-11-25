---
name: spm
description: Run long-lived processes (dev servers, API servers, workers, bots, tunnels, watchers) and scheduled jobs as persistent native services with spm instead of backgrounding them with `&`, `nohup`, `start /b`, or a terminal that dies with the session. Use whenever a process must keep running after this command or session ends, must restart on crash or reboot, or when the user asks to start, stop, restart, inspect, read logs of, schedule, or remove a background service on Linux, macOS, or Windows.
---

# Running persistent processes with spm

spm turns a command into a native service: a systemd user unit on Linux, a
LaunchAgent on macOS, and a supervised user service on Windows. The process
survives the end of the agent session, restarts if it crashes, starts again at
login, and its output is kept so you can read it later.

## When to use it

Use spm when the process should outlive the command that starts it:

- a dev server or API the user wants to keep using (`npm run dev`, `uvicorn`, `go run .`)
- a worker, queue consumer, bot, tunnel, or file watcher
- something that should run on a schedule and exit (`spm schedule`)

Do not use spm for a command that finishes on its own (tests, builds, one-off
scripts): run those directly.

Never background a long-lived process with `&`, `nohup`, `disown`, `setsid`,
`start /b`, or `Start-Process` when spm is available. Those processes are
killed or orphaned when the session ends, and their output is lost.

## Check that spm is installed

```bash
spm version
```

If it is missing, tell the user and offer the installer from
https://github.com/eyvant/spm#install. Do not install it without asking.

If the `spm_*` MCP tools are available, prefer them over the shell: they return
structured results. The CLI below is equivalent.

## Start a service

Run from the project directory; spm uses the current directory as the working
directory. Always give a clear `--name`, and put the full command after `--`:

```bash
spm start --name web -- npm run dev
spm start --name api -- uvicorn app:app --port 8000
spm start --name worker -- python worker.py
```

Script files can be started directly: `spm start app.js --name api`.

Then confirm it is actually running before telling the user it works:

```bash
spm list
spm logs web -n 50
```

If the logs show a crash loop or a port conflict, fix the cause, then
`spm restart web`. Starting a name that already exists fails on purpose; to
replace its command or options, ask the user, then rerun `spm start` with the
same `--name` and `--force`.

## Everyday operations

| Goal | Command |
| --- | --- |
| List services and their state | `spm list` (`--json` for machine-readable) |
| Details for one service | `spm show NAME` |
| Recent logs | `spm logs NAME -n 100` |
| Why it stopped or restarted | `spm logs --spm NAME -n 50` (starts, exit codes, restarts) |
| Restart | `spm restart NAME` |
| Stop but keep it installed | `spm stop NAME` |
| Remove it | `spm delete NAME` |
| Check the environment | `spm doctor` |

Do not run `spm logs -f` or `spm list --watch` from an agent: they never return.
Read a bounded number of lines instead.

## Scheduled jobs

For a command that should run periodically and exit:

```bash
spm schedule --name backup --cron "0 3 * * *" -- ./backup.sh
spm run backup   # run once now
```

Use `spm start` for things that keep running, `spm schedule` for things that
finish.

## Safety rules

- Default to user scope. Use `--system` only when the user asks for a
  machine-wide service; it needs root or Administrator rights.
- Confirm the service name with the user before `spm delete`, and never run
  `spm delete all` unless they asked for exactly that.
- Put secrets in an env file and pass `--env-file PATH`. Values given with
  `--env` are stored in the service configuration.
- Before creating a service, check `spm list` for an existing one with the same
  name so you do not replace something the user relies on.
- When you finish, tell the user the service name and how to stop it
  (`spm stop NAME`) or remove it (`spm delete NAME`).
