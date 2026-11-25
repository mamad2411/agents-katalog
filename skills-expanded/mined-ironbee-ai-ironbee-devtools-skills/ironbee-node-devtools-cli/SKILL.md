---
name: ironbee-node-devtools-cli
description: CLI for debugging Node.js backend processes with non-blocking inspection. Use when the user needs to connect to Node.js processes (by PID, name, Docker, or port), set tracepoints/logpoints/exceptionpoints, capture call stacks and local variables, inspect console logs, capture the process's outbound HTTP requests (egress) with W3C trace-context injection, or run reusable scenarios. Requires daemon; connect before other debug commands. Also covers the creds-gated Jira and Linear issue-tracker domains: fetch/search issues, download attachments, attach evidence, comment, transition/set state, and report verification results back to the tracker.
allowed-tools: Bash(ironbee-node-devtools-cli:*)
---

# IronBee Node DevTools CLI

Command-line interface for non-blocking debugging of Node.js backend processes. Part of [IronBee DevTools](https://github.com/ironbee-ai/ironbee-devtools). Connects via the Inspector Protocol (Chrome DevTools Protocol) and provides tracepoints, logpoints, exceptionpoints, and watch expressions without pausing execution.

## Installation

```bash
# Install this skill (skills.sh)
npx skills add ironbee-ai/ironbee-devtools-skills

# Install the CLI binary (same package as the rest of IronBee DevTools)
npm install -g @ironbee-ai/devtools
```

Requires **Node.js >= 22.16.0** (`engines.node` in the package): the backend `db` domain's SQLite engine and the `FTS5` scenario-search strategy run on Node's built-in `node:sqlite`, which replaced the last native dependency.


## Port note

The browser CLI (`ironbee-devtools-cli` / `ironbee-browser-devtools-cli`) and the node CLI both default to daemon port `2020`. If you want both daemons running at once, start the node daemon on a different port and pass `--port` to every node CLI call:

```bash
PLATFORM=node ironbee-node-devtools-cli daemon start --port 2021
ironbee-node-devtools-cli --port 2021 debug connect --pid 12345
```

## Quick Start

```bash
# 1. Start daemon (if not running)
ironbee-node-devtools-cli daemon start

# 2. Connect to a Node.js process (by PID)
ironbee-node-devtools-cli --session-id my-debug debug connect --pid 12345

# 3. Set a tracepoint on server.js line 42
ironbee-node-devtools-cli --session-id my-debug debug put-tracepoint \
  --url-pattern "server.js" \
  --line-number 42

# 4. Trigger the code path (e.g., make API request to your app)
# 5. Get captured snapshots
ironbee-node-devtools-cli --session-id my-debug --json debug get-probe-snapshots
```

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session for Node connection persistence | auto |
| `--json` | Output as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |

**AI Agent Recommended:**

```bash
ironbee-node-devtools-cli --json --quiet --session-id "debug-session" <command>
```

## Tool Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| debug | Connection, tracepoints, logpoints, exceptionpoints, watch, snapshots | [debug](./references/debug.md) |
| o11y | Outbound HTTP capture (get/clear-http-requests; in-process agent, proxy-free) + W3C trace context (new-trace-id, set/get-trace-context; `traceparent` injected on egress) + reading traces back from the IronBee platform (get-trace, get-session-traces) | [o11y](./references/o11y.md) |
| scenario | Reusable step-based (or legacy single-script) flows — add, update, delete, list, search, recorded-actions, run; `scenario-run` is a direct subcommand with pause/resume for `llm-action` steps and an optional typed `params` contract. Full surface registered on the node CLI. **Note:** the `page` binding is browser-only; inside a node scenario script only `callTool` is available. | [scenario](./references/scenario.md) |
| execute | Batch JavaScript execution (run execute; CLI and MCP). **Note:** the `page` binding is browser-only; on node only `callTool` is available inside the VM. | [execute](./references/execute.md) |
| jira | Jira issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [jira](./references/jira.md) |
| linear | Linear issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [linear](./references/linear.md) |

**Jira / Linear** are platform-agnostic shared issue-tracker domains (like scenario/execute) — registered on every platform CLI, but **only when credentials are configured**: jira needs `JIRA_BASE_URL` plus `JIRA_EMAIL` + `JIRA_API_TOKEN` (Cloud) or `JIRA_PAT` (Server/DC); linear needs `LINEAR_API_KEY`. Without creds the `jira` / `linear` subcommand group does not exist. Write tools (add-comment, attach-file, create/update-issue, transition-issue / set-state, link-issue, report-verification) additionally require `JIRA_WRITE_ENABLED=true` / `LINEAR_WRITE_ENABLED=true` (default off ⇒ read-only intake tools only). Close the loop after a verification run: `ironbee-node-devtools-cli jira report-verification --key PROJ-123 --result pass --report "..." --artifacts ./artifacts/evidence.png` (linear: same shape with `--state` instead of `--transition`). See [jira](./references/jira.md) / [linear](./references/linear.md).

## Connection Methods

Connect via `debug connect` with one of:

| Method | Option | Example |
|--------|--------|---------|
| PID | `--pid <number>` | `--pid 12345` |
| Process name | `--process-name <pattern>` | `--process-name "server.js"` |
| Docker container | `--container-id` or `--container-name` | `--container-name my-api` |
| Inspector port | `--inspector-port <number>` | `--inspector-port 9229` |
| WebSocket URL | `--ws-url <url>` | `--ws-url "ws://127.0.0.1:9229/abc"` |

If the process doesn't have `--inspect` active, the CLI activates it via SIGUSR1 (no code changes). For Docker: expose port 9229 and use `--inspect=0.0.0.0:9229`.

## CLI Management Commands

### Daemon

```bash
ironbee-node-devtools-cli daemon status
ironbee-node-devtools-cli daemon start
ironbee-node-devtools-cli daemon stop
ironbee-node-devtools-cli daemon restart
ironbee-node-devtools-cli daemon info
```

### Session

```bash
ironbee-node-devtools-cli session list
ironbee-node-devtools-cli session info <session-id>
ironbee-node-devtools-cli session delete <session-id>
```

### Tools

```bash
ironbee-node-devtools-cli tools list
ironbee-node-devtools-cli tools search <query>
ironbee-node-devtools-cli tools info <tool-name>
```

### Config & Updates

```bash
ironbee-node-devtools-cli config
ironbee-node-devtools-cli update --check
```

## Examples

### Connect by PID

```bash
SESSION="--session-id api-debug"

# Connect
ironbee-node-devtools-cli $SESSION debug connect --pid $(pgrep -f "node server.js")

# Set tracepoint on route handler
ironbee-node-devtools-cli $SESSION debug put-tracepoint \
  --url-pattern "routes/api.ts" \
  --line-number 25

# Trigger: curl http://localhost:3000/api/users
# Get snapshots
ironbee-node-devtools-cli $SESSION --json debug get-probe-snapshots
```

### Connect by Process Name

```bash
ironbee-node-devtools-cli debug connect --process-name "api"
```

### Docker Container

```bash
# App runs in container with -p 9229:9229
ironbee-node-devtools-cli debug connect \
  --container-name my-node-app \
  --host host.docker.internal \
  --inspector-port 9229
```

### Exception Catching

```bash
SESSION="--session-id exc-debug"

ironbee-node-devtools-cli $SESSION debug connect --pid 12345
ironbee-node-devtools-cli $SESSION debug put-exceptionpoint --state uncaught

# Trigger error in app
# Check snapshots
ironbee-node-devtools-cli $SESSION --json debug get-probe-snapshots --types exceptionpoint
```

### Outbound HTTP Capture (egress)

```bash
SESSION="--session-id egress-debug"

# Connect, then start capture (first call installs the in-process agent — forward-looking)
ironbee-node-devtools-cli $SESSION debug connect --process-name "server.js"
ironbee-node-devtools-cli $SESSION --json o11y get-http-requests

# Trigger the code path, then read what the process called downstream
ironbee-node-devtools-cli $SESSION --json o11y get-http-requests --url-pattern "*/api/*" --include-headers

# Pin a trace id — the agent injects it as traceparent on every hooked outbound request
ironbee-node-devtools-cli $SESSION --json o11y new-trace-id
```

### Batch with execute

```bash
# Run JavaScript in the session VM — node platform only exposes callTool (no `page`)
ironbee-node-devtools-cli run execute --code "await callTool('debug_status', {}, true); await callTool('debug_list-probes', {}, true);"
```

## Interactive Mode

```bash
ironbee-node-devtools-cli interactive
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
eval "$(ironbee-node-devtools-cli completion bash)"
eval "$(ironbee-node-devtools-cli completion zsh)"
```
