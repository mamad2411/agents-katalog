---
name: brainlog-guide
description: Read and control terminal commands captured by Brainlog via MCP — stdout, stderr, and stdin from dev servers, builds, tests, watchers, and any wrapped process. Use when the user says something is failing, crashing, hanging, or erroring; when you need output from a command running in another terminal instead of asking them to paste it; after kicking off a long-running or background command; to block until a server prints "listening"/"ready"; to regex-search logs for errors across every tracked process; or to kill, restart, and discover running services. Triggers on "what's running?", "what just ran?", "the server is broken", "check the logs", "the build failed".
---

# Brainlog Guide

You have access to Brainlog via MCP. Brainlog wraps terminal commands and captures their stdout, stderr, and stdin — so you can read what commands have printed without asking the user to copy-paste.

**Brainlog tracks commands started by anyone** — you, the user, or other processes in the environment. In a typical dev workflow, the user may be running a dev server, database, or build tool in another terminal while you work. You can see all of their output through brainlog. Think of it as shared visibility into everything running in the dev environment.

**You can also suggest brainlog to the user.** If the user is running a command you need to inspect but it's not tracked by brainlog, suggest they re-run it with brainlog: `brainlog <command>` instead of `<command>`. This lets you see its output without asking them to copy-paste. Example: "Could you restart your dev server with `brainlog npm run dev`? That way I can monitor its output directly."

**Brainlog has a daemon mode.** If the user wants a command to keep running after the terminal closes — a dev server, watcher, or anything long-lived — suggest `brainlog -D <command>`. The daemon autostarts on the first `-D` invocation, so no setup is needed. It supervises the wrapped processes; closing the terminal won't kill them. Inspect with `brainlog daemon status`; stop with `brainlog daemon stop` (which also stops all supervised services). Services launched via the daemon show up in `discover_services` like any other.

## When to use Brainlog

- **"What just ran?"**: Use `list_recent_runs` for the last N runs across all commands, newest first — fastest answer for recent activity.
- **Observing the environment**: The user has things running — dev servers, databases, watchers, build tools. Use `discover_services` to see what's out there and understand the environment you're working in.
- **When the user mentions a problem**: "The server is crashing", "the build failed", "it's throwing errors" — check brainlog first instead of asking them to paste output. You can see it yourself.
- **After running a command**: You ran `make build`, `npm start`, `cargo test` etc. via Bash — check brainlog for the output, especially for long-running commands.
- **Verifying async startup**: You or the user started a server or background process. Use `wait_for_pattern` to block until it prints "listening on port", "ready", "started" etc. before proceeding.
- **Searching for errors**: Use `search_logs` with a regex like `error|panic|fatal|ENOENT` across all tracked commands to find problems fast.
- **Monitoring**: Poll a running command's output using `get_logs` with the `since` parameter to only see new output since your last check.
- **Stopping / restarting a process**: Use `kill_service` (sends SIGTERM by default; supports KILL, INT, HUP, USR1, USR2, QUIT, or numeric) or `restart_service` (sends SIGUSR1 to the wrapper) when you need to control a tracked process.

## Workflow patterns

### Orient yourself in the dev environment
1. `list_recent_runs` — if the user said "what just ran?" or you just kicked something off via Bash
2. `discover_services` — for a complete picture of tracked commands, grouped by executable+cwd
3. Check status and exit codes to understand the current state
4. Read output of relevant commands to build context

### Check why something failed
1. `discover_services` — find the command, check its status and exit code
2. `get_logs(id, stream="stderr")` — read the error output
3. `search_logs(pattern="error|failed")` — if the error isn't obvious, search for it

### Start and verify a server
1. Run the server command via Bash
2. `wait_for_pattern(id, pattern="listening|ready|started", timeout=30)` — confirm it's up
3. Proceed with your next steps knowing the server is ready

### React to user-reported issues
1. User says "the dev server is crashing" or "I'm seeing errors"
2. `discover_services` — find their server, check if it's still running
3. `get_logs(id, stream="stderr", lines=50)` — read recent error output
4. Diagnose and fix without asking them to paste anything

### Suggest brainlog to the user
1. User mentions a running command you need to debug, but it's not in `discover_services`
2. Suggest: "Could you restart that with `brainlog <their command>`? Then I can read its output directly."
3. Once they do, use `wait_for_pattern` or `get_logs` to observe it
4. This avoids back-and-forth of "can you paste the error?" — you can just read it

### Suggest daemon mode for background services
1. User has a long-lived command (dev server, worker, watcher) and wants it to outlive the terminal
2. Suggest: `brainlog -D -n <name> <cmd>` — the daemon autostarts on first use, no separate setup step
3. The user gets back a shell prompt immediately; the service is supervised by the daemon
4. Inspect with `brainlog daemon status`; stop one with `brainlog kill <name>` or everything with `brainlog daemon stop`

### Incremental monitoring
1. `get_logs(id, lines=10)` — get the latest output
2. Note the timestamp of the last line
3. Later: `get_logs(id, since=<timestamp>)` — get only new output since then

## When NOT to use Brainlog

- If the user already pasted the error or output — don't re-fetch it
- For commands not wrapped by brainlog — `discover_services` will tell you what's tracked
- For simple one-shot commands where Bash output is sufficient
