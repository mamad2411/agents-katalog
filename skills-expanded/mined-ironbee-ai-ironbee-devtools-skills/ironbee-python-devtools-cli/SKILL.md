---
name: ironbee-python-devtools-cli
description: CLI for debugging running Python processes with non-blocking inspection via debugpy (Debug Adapter Protocol). Use when the user needs to attach to a Python process (already-listening debugpy, PID injection, process name, or Docker), set tracepoints/logpoints/exceptionpoints, capture call stacks and local variables, dump all thread stacks (deadlock/GIL diagnosis), read stdout/stderr logs, capture the process's outbound HTTP requests (egress) with W3C trace-context injection, or run reusable scenarios. Requires daemon and `debugpy` installed in the target's Python environment; connect before other debug commands. Also covers the creds-gated Jira and Linear issue-tracker domains: fetch/search issues, download attachments, attach evidence, comment, transition/set state, and report verification results back to the tracker.
allowed-tools: Bash(ironbee-python-devtools-cli:*)
---

# IronBee Python DevTools CLI

Command-line interface for non-blocking debugging of running Python processes. Part of [IronBee DevTools](https://github.com/ironbee-ai/ironbee-devtools). Connects via **debugpy** over the Debug Adapter Protocol (DAP) and provides tracepoints, logpoints, exceptionpoints, watch expressions, and a Python-specific all-threads stack dump — without pausing execution (probes capture state and immediately resume).

**Runtime prerequisite:** the target's Python environment must have `debugpy` installed (`pip install debugpy`). It is a prerequisite in the *target process*, not on the machine running this CLI.

## Installation

```bash
# Install this skill (skills.sh)
npx skills add ironbee-ai/ironbee-devtools-skills

# Install the CLI binary (same package as the rest of IronBee DevTools)
npm install -g @ironbee-ai/devtools
```

Requires **Node.js >= 22.16.0** (`engines.node` in the package): the backend `db` domain's SQLite engine and the `FTS5` scenario-search strategy run on Node's built-in `node:sqlite`, which replaced the last native dependency.


## Port note

All IronBee DevTools CLIs default to daemon port `2020`. If you want multiple daemons running at once, start the python daemon on a different port (convention: browser 2020, node 2021, backend 2022, android 2023, terminal 2024, python 2025) and pass `--port` to every python CLI call:

```bash
PLATFORM=python ironbee-python-devtools-cli daemon start --port 2025
ironbee-python-devtools-cli --port 2025 debug connect --host 127.0.0.1 --debugpy-port 5678
```

## Quick Start

```bash
# 0. Start the target with debugpy listening (no code changes needed):
#    python -m debugpy --listen 127.0.0.1:5678 app.py

# 1. Start daemon (if not running)
ironbee-python-devtools-cli daemon start

# 2. Connect (already-listening debugpy)
ironbee-python-devtools-cli --session-id my-debug debug connect --host 127.0.0.1 --debugpy-port 5678

# 3. Set a tracepoint on app.py line 42
ironbee-python-devtools-cli --session-id my-debug debug put-tracepoint \
  --file "app.py" \
  --line 42

# 4. Trigger the code path (e.g., make an API request to your app)
# 5. Get captured snapshots
ironbee-python-devtools-cli --session-id my-debug --json debug get-probe-snapshots
```

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session for Python connection persistence | auto |
| `--json` | Output as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |

**AI Agent Recommended:**

```bash
ironbee-python-devtools-cli --json --quiet --session-id "debug-session" <command>
```

## Tool Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| debug | Connection, tracepoints, logpoints, exceptionpoints, watch, snapshots, logs, thread dump | [debug](./references/debug.md) |
| o11y | Outbound HTTP capture (get/clear-http-requests; in-process agent, proxy-free) + W3C trace context (new-trace-id, set/get-trace-context; `traceparent` injected on egress) + reading traces back from the IronBee platform (get-trace, get-session-traces) | [o11y](./references/o11y.md) |
| scenario | Reusable step-based (or legacy single-script) flows — add, update, delete, list, search, recorded-actions, run; `scenario-run` is a direct subcommand with pause/resume for `llm-action` steps and an optional typed `params` contract. Full surface registered on the python CLI. **Note:** the `page` binding is browser-only; inside a python scenario script only `callTool` is available. | [scenario](./references/scenario.md) |
| execute | Batch JavaScript execution (run execute; CLI and MCP). **Note:** the `page` binding is browser-only; on python only `callTool` is available inside the VM. | [execute](./references/execute.md) |
| jira | Jira issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [jira](./references/jira.md) |
| linear | Linear issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [linear](./references/linear.md) |

**Jira / Linear** are platform-agnostic shared issue-tracker domains (like scenario/execute) — registered on every platform CLI, but **only when credentials are configured**: jira needs `JIRA_BASE_URL` plus `JIRA_EMAIL` + `JIRA_API_TOKEN` (Cloud) or `JIRA_PAT` (Server/DC); linear needs `LINEAR_API_KEY`. Without creds the `jira` / `linear` subcommand group does not exist. Write tools (add-comment, attach-file, create/update-issue, transition-issue / set-state, link-issue, report-verification) additionally require `JIRA_WRITE_ENABLED=true` / `LINEAR_WRITE_ENABLED=true` (default off ⇒ read-only intake tools only). Close the loop after a verification run: `ironbee-python-devtools-cli jira report-verification --key PROJ-123 --result pass --report "..." --artifacts ./artifacts/evidence.png` (linear: same shape with `--state` instead of `--transition`). See [jira](./references/jira.md) / [linear](./references/linear.md).

## Connection Methods

Connect via `debug connect` with one of (none require modifying the target's source):

| Method | Option | Example |
|--------|--------|---------|
| Already-listening debugpy (primary) | `--host` + `--debugpy-port` | `--host 127.0.0.1 --debugpy-port 5678` |
| PID injection | `--pid <number>` | `--pid 12345` |
| Process name | `--process-name <pattern>` | `--process-name "app.py"` |
| Docker container | `--container-id` or `--container-name` | `--container-name my-api` |

"Already-listening" means the target was started with `python -m debugpy --listen host:port app.py` or called `debugpy.listen((host, port))`. PID injection runs `<python-path> -m debugpy --listen host:port --pid <pid>` to inject debugpy into the running process (POSIX; needs same-user / ptrace permission); `--python-path` overrides the interpreter used for injection (default `python3`, env `PYTHON_INTERPRETER`). Docker injects via `docker exec` and connects to the published host port.

Defaults come from `PYTHON_DEBUGPY_HOST` (default `127.0.0.1`) and `PYTHON_DEBUGPY_PORT` (default `5678`). `--just-my-code` scopes probes/exceptions to user code (server-side default `true`; the CLI flag is a switch — to force `false`, call via MCP / `run execute`).

## CLI Management Commands

### Daemon

```bash
ironbee-python-devtools-cli daemon status
ironbee-python-devtools-cli daemon start
ironbee-python-devtools-cli daemon stop
ironbee-python-devtools-cli daemon restart
ironbee-python-devtools-cli daemon info
```

### Session

```bash
ironbee-python-devtools-cli session list
ironbee-python-devtools-cli session info <session-id>
ironbee-python-devtools-cli session delete <session-id>
```

### Tools

```bash
ironbee-python-devtools-cli tools list
ironbee-python-devtools-cli tools search <query>
ironbee-python-devtools-cli tools info <tool-name>
```

### Config & Updates

```bash
ironbee-python-devtools-cli config
ironbee-python-devtools-cli update --check
```

## Python-specific configuration

| Env var | Type | Default | Purpose |
|---------|------|---------|---------|
| `PYTHON_DEBUGPY_HOST` | string | `127.0.0.1` | Default debugpy host for `debug connect`. |
| `PYTHON_DEBUGPY_PORT` | number | `5678` | Default debugpy port for `debug connect`. |
| `PYTHON_INTERPRETER` | string | `python3` | Interpreter used for debugpy PID/container injection. |
| `PYTHON_CONSOLE_MESSAGES_BUFFER_SIZE` | number | `1000` | Captured stdout/stderr line buffer for `debug get-logs`. |
| `PYTHON_HTTP_CAPTURE_BUFFER_SIZE` | number | `1000` | Max captured outbound HTTP flows retained (oldest evicted). |
| `PYTHON_HTTP_CAPTURE_BODY_MAX_BYTES` | number | `262144` | Max captured request/response body size in bytes (larger truncated + flagged). |
| `PYTHON_HTTP_HEADERS_REDACT` | string (csv) | `authorization,cookie,x-api-key` | Header names redacted when `--include-headers` is set. |
| `PYTHON_HTTP_BODY_REDACT_KEYS` | string (csv) | `password,token,secret,…` | JSON body keys redacted recursively when `--include-bodies` is set. |

## Examples

### Connect and trace a route handler

```bash
SESSION="--session-id api-debug"

# Target started with: python -m debugpy --listen 127.0.0.1:5678 app.py
ironbee-python-devtools-cli $SESSION debug connect --host 127.0.0.1 --debugpy-port 5678

# Set tracepoint on the handler
ironbee-python-devtools-cli $SESSION debug put-tracepoint \
  --file "routes/users.py" \
  --line 25

# Trigger: curl http://localhost:8000/api/users
# Get snapshots
ironbee-python-devtools-cli $SESSION --json debug get-probe-snapshots
```

### PID injection (no restart needed)

```bash
ironbee-python-devtools-cli debug connect --pid $(pgrep -f "python app.py")
ironbee-python-devtools-cli debug connect --process-name "app.py"
```

### Exception Catching

```bash
SESSION="--session-id exc-debug"

ironbee-python-devtools-cli $SESSION debug connect --host 127.0.0.1 --debugpy-port 5678
ironbee-python-devtools-cli $SESSION debug put-exceptionpoint --state uncaught

# Trigger error in app
ironbee-python-devtools-cli $SESSION --json debug get-probe-snapshots --types exceptionpoint
```

### Thread dump (deadlock / GIL diagnosis)

```bash
# Snapshot EVERY thread's stack at once (momentary pause, auto-resume)
ironbee-python-devtools-cli --json debug dump-threads
ironbee-python-devtools-cli --json debug dump-threads --include-locals
```

### Outbound HTTP Capture (egress)

```bash
SESSION="--session-id egress-debug"

# Connect, then start capture (first call installs the in-process agent — forward-looking)
ironbee-python-devtools-cli $SESSION debug connect --host 127.0.0.1 --debugpy-port 5678
ironbee-python-devtools-cli $SESSION --json o11y get-http-requests

# Trigger the code path, then read what the process called downstream
ironbee-python-devtools-cli $SESSION --json o11y get-http-requests --url-pattern "*/api/*" --include-headers

# Pin a trace id — the agent injects it as traceparent on every hooked outbound request
ironbee-python-devtools-cli $SESSION --json o11y new-trace-id
```

### Batch with execute

```bash
# Run JavaScript in the session VM — python platform only exposes callTool (no `page`)
ironbee-python-devtools-cli run execute --code "await callTool('debug_status', {}, true); await callTool('debug_list-probes', {}, true);"
```

## Interactive Mode

```bash
ironbee-python-devtools-cli interactive
```

| Command | Description |
|---------|-------------|
| `help` | Show commands |
| `exit`, `quit` | Exit |
| `debug connect` | Connect to process |
| `debug status` | Connection status |
| `<domain> <tool>` | Execute tool |

## Shell Completions

```bash
eval "$(ironbee-python-devtools-cli completion bash)"
eval "$(ironbee-python-devtools-cli completion zsh)"
```
