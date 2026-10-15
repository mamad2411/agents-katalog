---
name: multica-daemon
description: Run and diagnose the local Multica agent daemon — the process that registers runtimes and executes assigned agent tasks on this machine. Covers start/stop/logs, workspace watch/unwatch, daemon tuning, and profiles. Use when the user mentions the daemon, runtime, an agent that is not picking up work, or wants to watch a new workspace.
---

# Multica Daemon

The **daemon** is the local agent runtime. It auto-detects installed coding-agent CLIs (`claude`, `codex`, `opencode`, `openclaw`, `hermes`, `gemini`, `pi`, `cursor-agent`), registers each one as a runtime against the Multica server, polls for claimed tasks, and streams results back.

Official docs: https://github.com/multica-ai/multica/blob/main/CLI_AND_DAEMON.md#agent-daemon

## When to use this skill

- User reports an assigned agent is not picking up work.
- Starting / stopping / restarting the daemon.
- Tailing daemon logs to debug a stuck task.
- Watching or unwatching a workspace so the daemon processes (or ignores) its tasks.
- Tuning poll / heartbeat / concurrency limits.
- Running two daemons side by side via profiles (e.g. prod + staging).

## Quick health check

Run these three together. If any fails, the daemon is effectively down for that capability:

```bash
multica daemon status --output json     # Is the daemon running?
multica workspace list                  # What workspaces are being watched?
command -v claude codex gemini 2>/dev/null   # At least one agent CLI on PATH?
```

If the daemon is running but `multica daemon status --output json | jq '.detected_agents'` is empty, install at least one agent CLI — the daemon has no runtime to offer.

## Lifecycle

```bash
multica daemon start                  # Background, logs to ~/.multica/daemon.log
multica daemon start --foreground     # Foreground (debugging, blocks terminal)
multica daemon stop
multica daemon status
multica daemon status --output json
```

Logs:

```bash
multica daemon logs                   # Last 50 lines
multica daemon logs -n 200            # Last 200
multica daemon logs -f                # Follow (tail -f)
```

## Workspaces the daemon serves

A daemon only executes tasks for **watched** workspaces. `multica login` auto-watches every workspace the user belongs to, but new workspaces need an explicit watch.

```bash
multica workspace list                      # Watched ones marked with *
multica workspace get     <workspace-id>
multica workspace watch   <workspace-id>    # Start processing its tasks
multica workspace unwatch <workspace-id>    # Stop
multica workspace members <workspace-id>    # Humans + agents in this workspace
```

Changes take effect on the next poll cycle (default 3s). A restart is not required.

## Tuning

All settings can be flags on `daemon start` or environment variables.

| Setting | Flag | Env var | Default |
|---|---|---|---|
| Poll interval | `--poll-interval` | `MULTICA_DAEMON_POLL_INTERVAL` | `3s` |
| Heartbeat | `--heartbeat-interval` | `MULTICA_DAEMON_HEARTBEAT_INTERVAL` | `15s` |
| Agent timeout | `--agent-timeout` | `MULTICA_AGENT_TIMEOUT` | `2h` |
| Max concurrent tasks | `--max-concurrent-tasks` | `MULTICA_DAEMON_MAX_CONCURRENT_TASKS` | `20` |
| Daemon ID | `--daemon-id` | `MULTICA_DAEMON_ID` | hostname |
| Device name | `--device-name` | `MULTICA_DAEMON_DEVICE_NAME` | hostname |
| Runtime name | `--runtime-name` | `MULTICA_AGENT_RUNTIME_NAME` | `Local Agent` |
| Workspaces root | — | `MULTICA_WORKSPACES_ROOT` | `~/multica_workspaces` |

Agent-specific overrides (point at a non-default binary or model):

```bash
export MULTICA_CLAUDE_PATH=/opt/homebrew/bin/claude
export MULTICA_CLAUDE_MODEL=claude-opus-4-7
export MULTICA_CODEX_PATH=/usr/local/bin/codex
export MULTICA_CODEX_MODEL=gpt-5.1
# Also available: OPENCODE, OPENCLAW, HERMES, GEMINI, PI, CURSOR
```

Restart the daemon after changing env vars: `multica daemon stop && multica daemon start`.

## Profiles (multiple daemons on one machine)

Each profile gets its own config dir, token, daemon state, health port, and workspace root.

```bash
multica daemon start   --profile staging
multica daemon status  --profile staging
multica daemon logs -f --profile staging
multica daemon stop    --profile staging
```

Default profile and named profiles run independently and do not share task queues.

## Diagnosing "my agent isn't picking up work"

Walk this checklist in order — each step rules out a layer:

1. `multica auth status` — token valid?
2. `multica daemon status` — daemon running? Note its PID.
3. `multica daemon status --output json | jq '.detected_agents'` — is the agent's provider detected on this machine?
4. `multica workspace list` — is the issue's workspace marked `*` (watched)?
5. `multica issue get <id> --output json | jq '{status, assignee}'` — correctly assigned?
6. `multica issue runs <id>` — any attempted runs? Inspect with `issue run-messages`.
7. `multica daemon logs -n 200` — any errors around the time the issue was created?

One of those steps will show the break. If all pass and work still stalls, the daemon may have hit `--max-concurrent-tasks`; bump it or wait.

## Gotchas

- `multica daemon stop` sends SIGTERM; the daemon finishes in-flight tasks before exiting. Allow up to `--agent-timeout` on shutdown.
- The daemon writes workspace checkouts under `MULTICA_WORKSPACES_ROOT`. Large runs can consume disk — clean old workspace dirs periodically.
- Running as a launchd / systemd service? Make sure the unit inherits `PATH` so agent CLIs in `/opt/homebrew/bin` or `~/.local/bin` are discoverable.
- After changing `server_url` via `multica config set`, the daemon must be restarted to pick up the new endpoint.
- Two daemons on the same profile will conflict over the PID file. Use `--profile` if you really need two on one host.
