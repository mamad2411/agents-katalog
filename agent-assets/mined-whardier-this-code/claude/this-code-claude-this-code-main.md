# This Code — Claude Code Guide

## Project

This Code (`whardier.this-code`) is a VS Code launch interceptor and session tracker. A TypeScript extension records session state (workspace, open files, --user-data-dir, --profile, server commit hash) into per-instance JSON files and a SQLite index. A Rust CLI (`this-code`) intercepts the `code` command, avoids recursive self-invocation, and reads the session store for routing.

## GSD Workflow

This project uses GSD (Get Shit Done) for structured execution.

**Planning artifacts are in `.planning/`:**
- `PROJECT.md` — requirements, constraints, key decisions
- `REQUIREMENTS.md` — 35 REQ-IDs across 8 categories
- `ROADMAP.md` — 4-phase execution plan
- `STATE.md` — current phase and progress
- `research/` — domain research (stack, features, architecture, pitfalls)

**GSD commands:**
- `/gsd:next` — detect state and advance to next step automatically
- `/gsd:discuss-phase N` — gather context for phase N
- `/gsd:plan-phase N` — create execution plan for phase N
- `/gsd:execute-phase N` — execute plans for phase N
- `/gsd:verify-work` — verify phase deliverables against success criteria
- `/gsd:progress` — show current state

## Technology Stack

### VS Code Extension (TypeScript)

- **TypeScript** ~5.7 — strict mode
- **@types/vscode** ^1.75.0 — pin to minimum engine version
- **@vscode/sqlite3** ^5.1.12-vscode — Node-API prebuilts, ABI-stable across Electron. NOT `better-sqlite3` (NODE_MODULE_VERSION mismatch).
- **esbuild** ^0.28.0 — bundler (VS Code official recommendation)
- **@vscode/vsce** ^3.9.0 — VSIX packaging and Marketplace publishing

### Rust CLI

- **Rust** edition 2024, same toolchain as periphore (`../periphore/`)
- **clap** 4.6 (derive) — CLI argument parsing
- **figment** 0.10 + TOML — configuration
- **rusqlite** 0.39 (bundled) — SQLite with bundled libsqlite3; no system dependency
- **tracing** + **tracing-subscriber** — logging
- **thiserror** + **anyhow** — error handling

## Architecture

### Storage Model

- **Per-instance JSON**: `~/.vscode-server/bin/{commit-hash}/this-code-session.json`
  - Primary record for each VS Code Server instance
  - Zero locking concerns, collocated with server binary
- **SQLite index**: `~/.this-code/sessions.db` (WAL mode + busy_timeout)
  - Aggregated store for CLI querying across all instances
  - `extensionKind: ["workspace"]` means this lives on the same machine as the files

### Extension Lifecycle

- Activation: `onStartupFinished`
- Events: `onDidOpenTextDocument`, `onDidCloseTextDocument`, `onDidChangeWorkspaceFolders`
- Output: OutputChannel "This Code" (no UI, no webview)
- `extensionKind: ["workspace"]` — runs on remote host during SSH sessions

### CLI Architecture

- Installed at `~/.this-code/bin/` (dedicated directory, no PATH pollution)
- Symlinked/copied as `code` when used as shim
- Self-detection: env var guard (`THIS_CODE_ACTIVE=1`) + PATH stripping (pyenv/rbenv pattern)
- Shell integration: `this-code init bash|zsh|fish` prints eval-able setup

## Constraints

- **Platforms**: macOS and Linux primary; Windows best-effort
- **No GUI**: Extension is config + output channel only
- **No saves tracking**: Open/close events only
- **Commits**: Conventional commits via commitizen + prek hooks
- **SQLite WAL note**: CLI must open DB with read-write (not read-only) even for SELECTs — WAL requires `-shm` write access
