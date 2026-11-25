---
name: ironbee-terminal-devtools-cli
description: CLI for driving interactive terminal programs (shells, REPLs, full-screen TUIs) over a pseudo-terminal (PTY). Use when the user needs to spawn a CLI/REPL/TUI attached to a TTY, type commands and keystrokes (tmux key syntax), wait for expected output before sending more input, capture raw scrollback or the rendered screen grid, send process signals, resize the terminal, or run a one-shot command and read its output + exit code. The platform spawns the process itself (it does not attach to a pre-existing external process). For server APIs use the backend CLI; for Node.js process debugging use the node CLI. Also covers the creds-gated Jira and Linear issue-tracker domains: fetch/search issues, download attachments, attach evidence, comment, transition/set state, and report verification results back to the tracker.
allowed-tools: Bash(ironbee-terminal-devtools-cli:*)
---

# IronBee Terminal DevTools CLI

Command-line interface for driving interactive terminal programs over a single bridge — a pseudo-terminal (PTY). Part of [IronBee DevTools](https://github.com/ironbee-ai/ironbee-devtools). It spawns a program attached to a PTY and exchanges input/output the way a terminal multiplexer (tmux) does — so programs that behave differently off a TTY (colors, readline, password prompts, ncurses UIs) run the way they would for a human.

Scope: **programs the platform spawns itself.** It does not attach to a pre-existing external process. Use it for shells, language REPLs (python, node, psql), full-screen TUIs (vim, htop, less), SSH sessions, and any CLI that prompts. For browser UIs use [../ironbee-browser-devtools-cli/SKILL.md](../ironbee-browser-devtools-cli/SKILL.md); for Node.js process debugging use [../ironbee-node-devtools-cli/SKILL.md](../ironbee-node-devtools-cli/SKILL.md); for server APIs use [../ironbee-backend-devtools-cli/SKILL.md](../ironbee-backend-devtools-cli/SKILL.md).

## Installation

```bash
# Install this skill (skills.sh)
npx skills add ironbee-ai/ironbee-devtools-skills

# Install the CLI binary (same package as the rest of IronBee DevTools)
npm install -g @ironbee-ai/devtools
```

Requires **Node.js >= 22.16.0** (`engines.node` in the package): the backend `db` domain's SQLite engine and the `FTS5` scenario-search strategy run on Node's built-in `node:sqlite`, which replaced the last native dependency.


Works on macOS, Linux, and Windows (Windows uses ConPTY; POSIX signals are emulated — see [pty](./references/pty.md)).

## Port note

All IronBee DevTools CLIs default to daemon port `2020`. To run the terminal daemon alongside browser (2020), node (2021), backend (2022), and android (2023) daemons, start it on its own port and pass `--port` to every terminal CLI call:

```bash
PLATFORM=terminal ironbee-terminal-devtools-cli daemon start --port 2024
ironbee-terminal-devtools-cli --port 2024 pty list
```

## Quick Start

```bash
# 1. Start daemon (if not running)
ironbee-terminal-devtools-cli daemon start

# 2. Spawn a shell pane, capture the paneId
ironbee-terminal-devtools-cli --session-id work --json pty start

# 3. Type a command and run it
ironbee-terminal-devtools-cli --session-id work interaction send-keys --pane-id <id> --keys '["ls -la","Enter"]'

# 4. Block until the prompt returns, then read what was emitted
ironbee-terminal-devtools-cli --session-id work --json sync wait-for --pane-id <id> --pattern '\$ $'
ironbee-terminal-devtools-cli --session-id work --json content capture --pane-id <id>

# 5. Stop the pane when done
ironbee-terminal-devtools-cli --session-id work pty stop --pane-id <id>
```

For a non-interactive command, skip the pane lifecycle entirely:

```bash
ironbee-terminal-devtools-cli --json pty run --command "npm test"
```

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session for pane persistence (panes live per session) | auto |
| `--json` | Output as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |

**AI Agent Recommended:**

```bash
ironbee-terminal-devtools-cli --json --quiet --session-id "terminal-session" <command>
```

## Model (panes)

A **pane** is one PTY-backed process. `pty start` spawns a shell (or a specific program) and returns a `paneId`; many panes can run concurrently in a session. Panes are addressed by `--pane-id` on every interaction / content / sync / signal / resize call. Exited panes are retained — with their final output still readable via `content capture` — until `pty stop` forgets them.

## Synchronization model (wait, don't sleep)

There is no assert tool and no fixed-delay step. Send input, then **block on expected output** with `sync wait-for` (regex match) or `sync wait-for-idle` (output went quiet) before sending the next input or reading. Use the returned `cursor` to chain incremental reads — pass it as `--since` to the next `content capture` / `sync wait-for` so you only see new output. This is the right way to drive a prompt-driven program; guessing with delays is unreliable.

## Capture modes

- `stream` (default): the raw scrollback as the program emitted it — best for line-oriented programs (REPLs, shells, git/npm output). Supports incremental reads via `--since`.
- `screen`: the current rendered terminal grid (what a user would see now) — best for full-screen TUIs (vim, htop, less) where cursor positioning matters.

## Tool Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| pty | Pane lifecycle: spawn, stop, one-shot run, signal, resize, list (start, stop, run, signal, resize, list) | [pty](./references/pty.md) |
| interaction | Send keystrokes / literal text (send-keys, send-text) | [interaction](./references/interaction.md) |
| content | Read output: raw stream or rendered screen, cursor position (capture, get-cursor) | [content](./references/content.md) |
| sync | Block until output matches or goes idle (wait-for, wait-for-idle) | [sync](./references/sync.md) |
| o11y | Read traces back from the IronBee platform (get-trace, get-session-traces). Terminal pins no trace context of its own, so the pin tools are absent | [o11y](./references/o11y.md) |
| execute | Batch tool calls via JavaScript (`run execute`; CLI and MCP). **Note:** only `callTool` is available inside the VM (no `page` binding — that is browser-only). | [execute](./references/execute.md) |
| jira | Jira issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [jira](./references/jira.md) |
| linear | Linear issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [linear](./references/linear.md) |

**Jira / Linear** are platform-agnostic shared issue-tracker domains (like scenario/execute) — registered on every platform CLI, but **only when credentials are configured**: jira needs `JIRA_BASE_URL` plus `JIRA_EMAIL` + `JIRA_API_TOKEN` (Cloud) or `JIRA_PAT` (Server/DC); linear needs `LINEAR_API_KEY`. Without creds the `jira` / `linear` subcommand group does not exist. Write tools (add-comment, attach-file, create/update-issue, transition-issue / set-state, link-issue, report-verification) additionally require `JIRA_WRITE_ENABLED=true` / `LINEAR_WRITE_ENABLED=true` (default off ⇒ read-only intake tools only). Close the loop after a verification run: `ironbee-terminal-devtools-cli jira report-verification --key PROJ-123 --result pass --report "..." --artifacts ./artifacts/evidence.png` (linear: same shape with `--state` instead of `--transition`). See [jira](./references/jira.md) / [linear](./references/linear.md).

**Full `scenario` surface on this CLI.** The terminal CLI registers the scenario CRUD subcommands (`scenario-add` / `scenario-update` / `scenario-delete` / `scenario-list` / `scenario-search` / `scenario-recorded-actions`) plus a direct `scenario-run` subcommand under the `default` group — e.g. `ironbee-terminal-devtools-cli default scenario-run --name <name>` (with `--args` / `--param key=value` / `--timeout-ms`, and `--resume` / `--step-by-step` / `--refresh` for step-based scenarios). `scenario-run` is also reachable from inside `run execute` via `await callTool('scenario-run', { name: '...' })`. See the [scenario](./references/scenario.md) reference. Inside a scenario script only `callTool` is available (no `page` binding — that is browser-only).

## Secret redaction

Terminal output can echo secrets (`export TOKEN=...`, tokens pasted at prompts). Returned content from `content capture`, `sync wait-for`, and `pty run` is scrubbed of well-known secret shapes (Bearer / Basic / header / KV / env-secret) before it reaches the model, and the same scrubbing covers tool input/output on collector events. Master toggle: `TERMINAL_REDACT_ENABLE` (default `true`).

## CLI Management Commands

### Daemon

```bash
ironbee-terminal-devtools-cli daemon status
ironbee-terminal-devtools-cli daemon start
ironbee-terminal-devtools-cli daemon stop
ironbee-terminal-devtools-cli daemon restart
ironbee-terminal-devtools-cli daemon info
```

### Session

```bash
ironbee-terminal-devtools-cli session list
ironbee-terminal-devtools-cli session info <session-id>
ironbee-terminal-devtools-cli session delete <session-id>
```

### Tools

```bash
ironbee-terminal-devtools-cli tools list
ironbee-terminal-devtools-cli tools search <query>
ironbee-terminal-devtools-cli tools info <tool-name>
```

### Config

```bash
ironbee-terminal-devtools-cli config
```

## Terminal-specific configuration

| Env var | Type | Default | Purpose |
|---------|------|---------|---------|
| `TERMINAL_OUTPUT_BUFFER_CHARS` | number | `500000` | Per-pane scrollback ring size in characters (oldest output trimmed past this). |
| `TERMINAL_SCROLLBACK` | number | `5000` | Rendered-screen scrollback in lines. |
| `TERMINAL_MAX_PANES` | number | `50` | Max concurrent panes per session. |
| `TERMINAL_WAIT_TIMEOUT_MS` | number | `10000` | Default timeout for `sync wait-for` / `sync wait-for-idle`. |
| `TERMINAL_IDLE_QUIET_MS` | number | `500` | Quiet period that counts as idle for `sync wait-for-idle`. |
| `TERMINAL_RUN_TIMEOUT_MS` | number | `30000` | Default timeout for `pty run` before the process is killed. |
| `TERMINAL_REDACT_ENABLE` | boolean | `true` | Scrub well-known secrets from returned output. |
| `TERMINAL_SERVER_INSTRUCTIONS_ENABLE` | boolean | `true` | Include platform server-instructions in MCP server info. |
| `TERMINAL_POLICY_USAGE_ENABLE` | boolean | `false` | Include the usage-policy block in MCP server info. |

The default shell comes from `$SHELL` (POSIX) or `%COMSPEC%` / PowerShell (Windows); override per-pane with `pty start --command`.

## Examples

### Drive a Python REPL

```bash
SESSION="--session-id repl"

# Spawn python directly as the pane process
PANE=$(ironbee-terminal-devtools-cli $SESSION --json pty start --command python | jq -r '.paneId')

# Wait for the >>> banner, then send an expression
ironbee-terminal-devtools-cli $SESSION --json sync wait-for --pane-id "$PANE" --pattern '>>> '
ironbee-terminal-devtools-cli $SESSION interaction send-keys --pane-id "$PANE" --keys '["2 + 40","Enter"]'

# Block until the next prompt, then read only the new output
ironbee-terminal-devtools-cli $SESSION --json sync wait-for --pane-id "$PANE" --pattern '>>> '
ironbee-terminal-devtools-cli $SESSION --json content capture --pane-id "$PANE" --strip-ansi

ironbee-terminal-devtools-cli $SESSION pty stop --pane-id "$PANE"
```

### Inspect a full-screen TUI

```bash
SESSION="--session-id tui"
PANE=$(ironbee-terminal-devtools-cli $SESSION --json pty start --command vim --cols 120 --rows 40 | jq -r '.paneId')

# Read the rendered grid (not raw stream) for a TUI
ironbee-terminal-devtools-cli $SESSION --json content capture --pane-id "$PANE" --mode screen

# Type ':q!' then Enter to quit
ironbee-terminal-devtools-cli $SESSION interaction send-keys --pane-id "$PANE" --keys '[":q!","Enter"]'
```

### One-shot command with exit code

```bash
# pipes / && / redirection work because the command runs through a shell
ironbee-terminal-devtools-cli --json pty run --command "grep -r TODO src | wc -l"
```

### Interrupt a long-running process

```bash
# Send the Ctrl-C keystroke (the program may trap it) ...
ironbee-terminal-devtools-cli interaction send-keys --pane-id <id> --keys '["C-c"]'
# ... or deliver a real process signal (kept pane)
ironbee-terminal-devtools-cli pty signal --pane-id <id> --signal SIGINT
```

### Batch with execute

```bash
# Run multiple tool calls in one request — terminal exposes only callTool (no `page`)
ironbee-terminal-devtools-cli run execute --code "const p = await callTool('pty_start', {}, true); await callTool('interaction_send-keys', { paneId: p.paneId, keys: ['echo hi','Enter'] });"
```

## Interactive Mode

```bash
ironbee-terminal-devtools-cli interactive
```

| Command | Description |
|---------|-------------|
| `help` | Show commands |
| `exit`, `quit` | Exit |
| `pty start` | Spawn a pane |
| `pty list` | List open panes |
| `<domain> <tool>` | Execute tool |

## Shell Completions

```bash
eval "$(ironbee-terminal-devtools-cli completion bash)"
eval "$(ironbee-terminal-devtools-cli completion zsh)"
```
