---
name: anypoc
description: AnyPoC skills — setup projects, find bugs, generate PoCs, retry a PoC run with new guidance, hunt (scan + PoC in one pass), launch the dashboard, check status of active runs, or list all subcommands via help. Subcommands include setup-project, find-bugs, run-poc, retry-poc, hunt, dashboard, status, help.
disable-model-invocation: true
argument-hint: hunt PROJECT for what kinds of bugs
---

You are running an AnyPoC skill. The subcommand is "$0" with arguments: $1

**Provider note (applies to `hunt`, `find-bugs` / scan, `run-poc`, `retry-poc`):** these commands spawn a coding agent inside each container via caw. caw picks the agent from the `CAW_PROVIDER` env var (defaults to `claude`). If you yourself are running as Codex (not Claude Code), prepend `CAW_PROVIDER=codex` to every `anypoc` command you build for the user — both the raw command and the tmux-wrapped variant — so the in-container agent matches the host agent the user is already using and authenticated with. Example: `CAW_PROVIDER=codex anypoc hunt run history -p wasmtime time_range="last 6 months"`. Skip this for `dashboard`, `status`, `setup-project`, and `help` — they don't spawn agents.

**Model note:** `CAW_MODEL` selects which model the in-container agent runs with. Leave it unset to use caw's default for the chosen provider — that is the right choice for almost all runs. Only set it (e.g. `CAW_MODEL=claude-opus-4-7 anypoc hunt run ...`) if the user *explicitly* names a model they want to use; don't infer it, don't suggest it proactively, don't add it just because it's available. If you do set it, prepend it to both the raw and tmux-wrapped commands.

Read the instructions file for this subcommand from references/:

- [setup-project](references/setup-project.md) — interactively set up a new AnyPoC project
- [find-bugs](references/find-bugs.md) — pick a scanning strategy and build an `anypoc scan run` command
- [run-poc](references/run-poc.md) — generate PoCs from bug reports produced by an earlier scan (`anypoc poc run`)
- [retry-poc](references/retry-poc.md) — rerun PoC generation on an existing bug (new attempt), optionally with extra guidance (`anypoc poc retry`)
- [hunt](references/hunt.md) — scan for bugs and generate PoCs concurrently in one pass (`anypoc hunt run`)
- [dashboard](references/dashboard.md) — launch the AnyPoC web dashboard (optionally in tmux)
- [status](references/status.md) — list active anypoc tmux sessions and inspect one for a status summary
- [help](references/help.md) — list every subcommand with a one-line description

If "$0" does not match any subcommand above, tell the user the available subcommands and stop.
