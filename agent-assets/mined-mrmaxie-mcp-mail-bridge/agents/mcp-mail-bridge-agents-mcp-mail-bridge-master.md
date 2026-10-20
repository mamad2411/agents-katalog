# McpMailBridge Agent Notes

## Project Shape

- This repository is a Rust MCP server and local configuration manager for mail accounts.
- MCP transport is stdio only until a human explicitly asks for another transport.
- Account data lives in a SQLite database named `mmb.db` next to the executable by default.
- The CLI may accept `--database <path>` for tests, local development, and recovery flows.
- Do not store credentials in tracked files, examples, tests, chat output, or logs.

## Architecture

- Keep binary entrypoint code in `src/main.rs`.
- Keep command parsing and non-interactive config commands in `src/cli.rs`.
- Keep account schema, validation, database path resolution, and SQLite persistence in `src/config.rs`.
- Keep permission checks in `src/permissions.rs`.
- Keep MCP tool registration and stdio serving in `src/mcp.rs`.
- Keep terminal UI code in `src/tui.rs`.
- Keep mail-provider code behind a small boundary before adding provider-specific IMAP, SMTP, OAuth, or SSO behavior.

## Commands

- `cargo build` builds the project.
- `cargo test` runs tests.
- `cargo fmt --check` verifies Rust formatting.
- `cargo clippy --all-targets --all-features -- -D warnings` runs lint checks.
- `cargo run -- serve` starts the MCP stdio server.
- `cargo run -- config list` lists configured accounts.
- `cargo run -- --database ./mmb.db config list` lists accounts from a specific SQLite database.
- `cargo run -- tui` opens the terminal UI for account management.

## Rust Conventions

- Prefer small modules and explicit public contracts over broad catch-all files.
- Prefer typed enums for closed value sets such as permissions, auth kinds, and providers.
- Validate account data at process boundaries before using it.
- Keep exported APIs explicit and boring; avoid framework-like abstractions until repetition proves the need.
- Prefer early returns for invalid input and permission failures.
- Keep errors actionable while redacting secrets.
- Add unit tests for database persistence, validation, and permission behavior when those areas change.

## Dependencies

- Install dependencies through `cargo add` with exact package requirements, for example `cargo add crate@=x.y.z`.
- Do not manually edit dependency versions unless cargo tooling cannot express the required change.
- Keep dependency choices conservative and aligned with a modern Rust stack.

## Recommended Skills

### Text Writing

- `avoid-ai-writing` - use when drafting human-facing updates, summaries, README prose, or project notes.
- `humanizer` - use when prose sounds robotic or over-structured.
- `professional-communication` - use for decision notes, status updates, and implementation summaries.
- `writing-clearly-and-concisely` - use for documentation, error text, and concise project communication.

### Coding

- `rust-pro` - main coding skill for this project.
- `code-simplification` - use when refactoring or reducing complexity.
- `commit-work` - use when the human asks to stage or commit.
- `diagnose` - use for defects, failing checks, and unexpected runtime behavior.
- `doubt-driven-development` - use when changes span several modules or affect security-sensitive flows.
- `incremental-implementation` - use for multi-file implementation work.
- `karpathy-guidelines` - use for pragmatic Rust implementation and review.
- `systematic-debugging` - use before fixing confirmed bugs or failing tests.

## Sensitive Data

- Do not paste secrets, tokens, passwords, or private OAuth URLs into chat, git, docs, or logs.
- Redact secrets in errors and test fixtures.

## Cleanup

- Remove local screenshots, logs, traces, one-off scripts, and generated scratch files after verification unless they are explicitly needed.
- Stop local servers, terminal UIs, browser sessions, or other helper processes when they are no longer needed.

## Git

- Do not create branches, commits, pushes, or pull requests unless the human explicitly asks.
- Use English Conventional Commits without scopes: `feat:`, `fix:`, or `chore:`.
- Before committing, inspect `git status --short --branch --untracked-files=all`.
- Stage only intended source, docs, and configuration changes.
- Remove local screenshots, logs, traces, one-off scripts, and generated scratch outputs after verification unless a human asks to keep them.

## Local Files

- Use `.local/` for machine-local notes, scratch plans, local credentials, and local operating context.
- Keep `.local/` excluded through `.git/info/exclude`.
- Do not commit `.local/` content unless a human explicitly asks for a tracked artifact.
