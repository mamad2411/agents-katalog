---
name: terminal-testing
description: Drive and test interactive terminal programs — shells, language REPLs (python/node/psql), full-screen TUIs (vim/htop/less), SSH sessions, and any CLI that prompts — over a pseudo-terminal (PTY). Use to spawn a program attached to a TTY, type commands and keystrokes, wait for expected output before sending more input, read raw scrollback or the rendered screen, send signals, and assert on output. The platform spawns the process itself (no attaching to a pre-existing external process). For one-shot non-interactive commands prefer `pty run`. For web pages use browser-testing; for server APIs use backend-testing.
allowed-tools: Bash(ironbee-terminal-devtools-cli:*)
---

# Terminal Testing Skill

Drive interactive terminal programs over a PTY using the [Terminal DevTools CLI](../ironbee-terminal-devtools-cli/SKILL.md). Spawn a shell / REPL / TUI attached to a pseudo-terminal, type into it, synchronize on its output, and read what it produced — the way a human (or tmux) would.

## When to Use

This skill activates when:
- User wants to test or automate a CLI, REPL, or full-screen TUI
- User needs a program to run on a real TTY (colors, readline, password prompts, ncurses UIs)
- User wants to type commands/keystrokes into an interactive program and assert on its output
- User wants a one-shot command's full output + exit code
- User mentions a PTY, pseudo-terminal, shell session, `expect`-style automation, or driving `vim`/`psql`/`python`

The platform **spawns the process itself** — it does not attach to a pre-existing external process. For web pages use [browser-testing](../browser-testing/SKILL.md); for server APIs use [backend-testing](../backend-testing/SKILL.md); for Node.js process debugging use the [node CLI](../ironbee-node-devtools-cli/SKILL.md).

## Synchronization model (wait, don't sleep)

There is no assert tool and no fixed-delay step. After sending input, **block on expected output** with `sync wait-for` (regex) or `sync wait-for-idle` (output went quiet) before sending more input or reading. Chain incremental reads by passing the returned `cursor` as `--since` to the next `content capture` / `sync wait-for`, so you only ever see new output. Guessing with sleeps is unreliable; matching on output is not.

## Capabilities

### Pane lifecycle
```bash
ironbee-terminal-devtools-cli --json pty start                          # default shell
ironbee-terminal-devtools-cli --json pty start --command python --cols 100 --rows 30
ironbee-terminal-devtools-cli --json pty list
ironbee-terminal-devtools-cli pty resize --pane-id <id> --cols 120 --rows 40
ironbee-terminal-devtools-cli pty stop --pane-id <id>
```

### Send input (tmux key syntax)
```bash
ironbee-terminal-devtools-cli interaction send-keys --pane-id <id> --keys '["ls -la","Enter"]'
ironbee-terminal-devtools-cli interaction send-keys --pane-id <id> --keys '["C-c"]'
ironbee-terminal-devtools-cli interaction send-text --pane-id <id> --text "SELECT 1;"
```

### Synchronize on output
```bash
ironbee-terminal-devtools-cli --json sync wait-for --pane-id <id> --pattern '\$ $'
ironbee-terminal-devtools-cli --json sync wait-for --pane-id <id> --pattern 'Server listening' --since 1024
ironbee-terminal-devtools-cli --json sync wait-for-idle --pane-id <id>
```

### Read output
```bash
ironbee-terminal-devtools-cli --json content capture --pane-id <id> --since 4096 --strip-ansi
ironbee-terminal-devtools-cli --json content capture --pane-id <id> --mode screen    # rendered grid for TUIs
ironbee-terminal-devtools-cli --json content get-cursor --pane-id <id>
```

### Signals and one-shots
```bash
ironbee-terminal-devtools-cli pty signal --pane-id <id> --signal SIGINT
ironbee-terminal-devtools-cli --json pty run --command "npm test"
```

## Basic Testing Workflow

1. **Spawn**: `pty start` (a shell, or `--command` a specific program); keep the `paneId`.
2. **Wait for ready**: `sync wait-for` on the prompt / banner before sending input.
3. **Send**: `interaction send-keys` (type a command + `Enter`) or `interaction send-text`.
4. **Wait**: `sync wait-for` on the next prompt (or `sync wait-for-idle` when there is no clean marker).
5. **Read**: `content capture` with `--since <cursor>` for only the new output (`--mode screen` for TUIs).
6. **Verify**: judge the captured output yourself; repeat from step 3.
7. **Stop**: `pty stop` the pane.

## End-to-End: drive a psql session

```bash
SESSION="--session-id psql"

PANE=$(ironbee-terminal-devtools-cli $SESSION --json pty start --command psql --args '["-U","app","appdb"]' | jq -r '.paneId')

# Wait for the psql prompt, run a query, wait for the next prompt, read the result
ironbee-terminal-devtools-cli $SESSION --json sync wait-for --pane-id "$PANE" --pattern 'appdb=#'
ironbee-terminal-devtools-cli $SESSION interaction send-keys --pane-id "$PANE" --keys '["SELECT count(*) FROM users;","Enter"]'
CUR=$(ironbee-terminal-devtools-cli $SESSION --json sync wait-for --pane-id "$PANE" --pattern 'appdb=#' | jq -r '.cursor')
ironbee-terminal-devtools-cli $SESSION --json content capture --pane-id "$PANE" --strip-ansi

ironbee-terminal-devtools-cli $SESSION interaction send-keys --pane-id "$PANE" --keys '["\\q","Enter"]'
ironbee-terminal-devtools-cli $SESSION pty stop --pane-id "$PANE"
```

## End-to-End: assert a TUI renders correctly

```bash
SESSION="--session-id tui"
PANE=$(ironbee-terminal-devtools-cli $SESSION --json pty start --command htop --cols 120 --rows 40 | jq -r '.paneId')

# Let it paint, then read the rendered grid (not the raw stream)
ironbee-terminal-devtools-cli $SESSION --json sync wait-for-idle --pane-id "$PANE"
ironbee-terminal-devtools-cli $SESSION --json content capture --pane-id "$PANE" --mode screen

# Quit
ironbee-terminal-devtools-cli $SESSION interaction send-keys --pane-id "$PANE" --keys '["q"]'
ironbee-terminal-devtools-cli $SESSION pty stop --pane-id "$PANE"
```

## Best Practices

1. **Use sessions** (`--session-id`) for multi-step flows — panes are pinned to the session.
2. **Always `sync wait-for` before sending more input** — never guess with delays.
3. **Chain `--since <cursor>`** across captures/waits so you only read new output.
4. **`screen` mode for TUIs, `stream` mode for shells/REPLs** — pick the capture mode to match the program.
5. **`C-c` keystroke vs `pty signal`** — `send-keys ["C-c"]` may be trapped by the program; `pty signal --signal SIGINT` delivers a real process signal.
6. **`pty run` for non-interactive commands** — one call returns full output + exit code; no pane lifecycle to manage.
7. **Stop panes you no longer need** — long-idle panes may be reaped by the daemon.
8. **Batch tight flows** with `run execute --code "..."` and `callTool()` to cut round-trips (only `callTool` is available — no `page`).
