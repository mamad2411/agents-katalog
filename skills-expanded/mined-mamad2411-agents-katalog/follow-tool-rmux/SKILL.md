---
name: follow-tool-rmux
description: Set up and use the RMUX terminal multiplexer for automation and scripting
argument-hint: "[scope]"
related:
  - follow-lang-rust
  - follow-tool-cargo
  - follow-create-plugins
  - follow-tool-usage
---

## Goal

Set up and use RMUX for terminal multiplexing, automation, and programmatic control

## Scope

Use for projects that want a tmux-compatible CLI or want to drive terminal sessions via the Rust/Python/TypeScript SDK

- Latest: `rmux@0.10.0` (crates.io; see rmux.io) (verified 2026-09-16)

## Execute

### 1. Install RMUX

> Goal: install the RMUX CLI on the environment

1. Use `mise use -g rmux` or `cargo install rmux --locked`
2. On Windows use `winget install rmux`, `choco install rmux`, or `scoop bucket add rmux https://github.com/Helvesec/scoop-rmux` then `scoop install rmux`
3. On macOS use `brew install rmux`
4. Verify with `rmux -V` or `rmux --version`
5. See details in 

### 2. Create and Attach Sessions

> Goal: create and attach sessions

1. Create a session with `rmux new-session -s mysession` or `rmux new -s mysession`
2. Attach with `rmux attach -t mysession`
3. Detach with `rmux detach`
4. List all sessions with `rmux ls`
5. See details in 

### 3. Manage Panes and Windows

> Goal: manage panes, windows, and layouts

1. Create a window with `rmux new-window -n name`
2. Split a pane with `rmux split-window -h` or `rmux split-window -v`
3. Select a pane/window with `rmux select-pane -t 0.1` or `rmux select-window -t 1`
4. Send a command to a pane with `rmux send-keys -t 0.0 "ls" Enter`
5. See details in 

### 4. Configure RMUX

> Goal: configure RMUX for shell and key bindings

1. Create the config file at `~/.rmux.conf` (Linux/macOS) or `%USERPROFILE%\.rmux.conf` (Windows)
2. Set the prefix key, mouse support, history limit, and status line
3. Reload the config with `rmux source-file ~/.rmux.conf`
4. See details in 

### 5. Automate with SDK

> Goal: drive RMUX via the SDK for automation

1. Use the Rust crate `rmux-sdk` for a typed async API
2. Use the Python package `librmux` or npm `@rmux/sdk` for TypeScript
3. Create sessions, spawn panes, send text, capture output, and wait for text
4. See details in 

### 6. CI Integration

> Goal: run RMUX sessions in CI pipelines

1. Install RMUX in CI with the release binary or a package manager
2. Use `rmux new-session -d -s ci` to create a detached session
3. Send commands and capture output via the CLI or SDK
4. Use `rmux diagnose --human` when troubleshooting runtime/CLI issues (set `RMUX_DISABLE_TINY_CLI=1` to force the full CLI helper)
5. See details in 

## Rules

### 1. CLI Compatibility

- RMUX supports a tmux-compatible command surface of more than 90 commands
- Use `rmux` instead of `tmux` when you want a native cross-platform runtime
- Use `mise use -g rmux` for the global install per `global_rules`

### 2. Configuration

- Keep the config at `~/.rmux.conf` or `%USERPROFILE%\.rmux.conf`
- Use `rmux source-file <path>` to reload without restarting the daemon
- Don't hard-code secrets or sensitive paths

### 3. Automation

- Use the SDK for programmatic control instead of parsing text output where possible
- Use `wait-for` or the SDK equivalent to synchronize between panes
- Use `rmux web-share` when you want to share a session through the browser (E2E encrypted)
- Use `rmux claude [args]` to run Claude Code in an RMUX workspace with tmux teammate mode
- Close unused sessions with `rmux kill-session -t <name>`

- Use /follow-lang-rust if needed
- Use /follow-tool-cargo if needed
- Use /follow-create-plugins (tui-ratatui) if needed
- Use /follow-tool-usage if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- RMUX CLI installed and working on the target platform
- Sessions, windows, panes can be created and managed
- Config loads and key bindings work as set
- The SDK or CLI drives automation
- No detached sessions left behind after a workflow ends

