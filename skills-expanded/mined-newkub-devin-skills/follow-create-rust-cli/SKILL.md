---
name: follow-create-rust-cli
description: Build Rust CLI applications following context and best practices
argument-hint: "[scope]"
related:
  - follow-create-cli
  - follow-tool-cargo
  - deep-review-codebase
  - flatten-directory
  - rethink
  - run-test

---
## Goal

Build high-performance CLI applications with Rust, with type safety and zero-cost abstractions

## Scope

Use for building CLI applications with the Rust runtime — if Rust vs Bun is unclear, use `/follow-create-cli` to pick the stack first

- Packages: Rust toolchain (`edition = "2024"`), `clap` (derive API — 4.x renamed the builder `App` → `Command`), `color-eyre`, `cargo-dist`, `thiserror`/`anyhow`, `serde` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Inspect the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the reasons for choosing the stack and libraries for later reference (create rust cli)

### 2. Decide Architecture

> Goal: Choose the architecture that fits the CLI

1. If Rust vs Bun is unclear → run `/follow-create-cli` first
2. Run `/deep-review-codebase` or `/deep-review-codebase` to assess the context
3. Choose the architecture based on the workload:
   - Simple CLI with a few subcommands → Command/Handler split
   - Needs to support multiple output modes (TTY/JSON/agent) → Functional Core / Imperative Shell
   - Multiple backends/complex IO with heavy testing → Hexagonal / Ports & Adapters
4. Record the reasons for choosing this architecture

### 3. Setup Project Structure

> Goal: Create the project structure per the chosen architecture

1. Create the project with `cargo new --name <project> <path>`
2. Create directories per the chosen architecture:
   - Command/Handler split: `src/cli/`, `src/commands/`, `src/services/`, `src/output.rs`, `src/config.rs`
   - Functional Core: `src/core/`, `src/shell/`, `src/cli/`, `src/output.rs`
   - Hexagonal: `src/core/`, `src/ports/`, `src/app/`, `src/adapters/`, `src/commands/`, `src/wiring.rs`
3. Separate concerns: CLI parsing, business logic, output, external I/O
4. Create entry points: `src/main.rs` for the binary, `src/lib.rs` for the library
5. If the project has multiple binaries: create them in `src/bin/`
6. If a directory nests deeper than 3 levels and it isn't necessary → run `/flatten-directory --mode code`

### 4. Configure Dependencies

> Goal: Add the dependencies a CLI needs in `Cargo.toml`

1. Add CLI dependencies: `cargo add clap --features derive,env` (argument parsing), `serde` (serialization), `serde_json` (JSON)
2. Add logging: `tracing`, `tracing-subscriber`
3. Add error handling: `thiserror` (library), `anyhow` (application)
4. Add colored output: `colored` or `nu-ansi-term`
5. Add progress indicators: `indicatif`
6. Add interactive prompts: `dialoguer` or `inquire`
7. Add table output: `comfy-table` or `prettytable-rs`
8. Set `edition = "2024"` in `Cargo.toml`

### 5. Configure Build Profiles

> Goal: Configure build profiles for development and production

1. Set `[profile.dev]` with `debug = "line-tables-only"` and `incremental = true`
2. Set `[profile.release]` with `lto = true`, `opt-level = "z"`, `strip = true`, `codegen-units = 1`, `panic = "abort"`
3. Set `[profile.dev.package."*"]` with `debug = false` to speed up deps compilation

### 6. Setup Scripts

> Goal: Create a justfile for reusable development scripts

1. Add a `dev` recipe: `cargo watch -x run`
2. Add a `build` recipe: `cargo build --release`
3. Add a `lint` recipe: `cargo clippy -- -D warnings && cargo fmt --check`
4. Add a `test` recipe: `cargo nextest run && cargo test --doc`
5. Add a `run` recipe: `cargo run --`

### 7. Development Workflow

> Goal: Use a workflow with watch mode, lint, and automatic formatting

Use an efficient development workflow

1. Use `cargo watch -x run` for development with watch mode
2. Use `cargo build --release` for production builds
3. Use `cargo clippy -- -D warnings` for code quality checks
4. Use `cargo fmt` for formatting

### 8. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Project Structure

The structure must be correct

- Separate concerns: CLI parsing, business logic, output formatting, external I/O
- Choose the architecture by context; don't force Clean or Layered
- Default for a typical CLI: Command/Handler split with `src/cli/`, `src/commands/`, `src/services/`, `src/output.rs`, `src/config.rs`
- With multiple clients (TTY/JSON/agent): Functional Core / Imperative Shell
- With multiple backends/complex IO: Hexagonal / Ports & Adapters
- Use flat modules (`foo.rs` + `foo/`) per Rust 2018+ instead of `mod.rs` when appropriate
- Name files in snake_case
- Name types in PascalCase

### 2. CLI Design

Design the CLI to be easy to use

- Use `clap` v4 for argument parsing with derive macros
- Use subcommands for complex CLIs
- Use `#[command(version, about)]` for auto-generated help
- Use `clap::Parser` derive for type-safe argument parsing
- Use `clap::Subcommand` for subcommands
- Define `#[arg(short, long, value_name = "FILE")]` for arguments
- Use `clap_complete` for shell completions (bash, zsh, fish, powershell)

### 3. Error Handling

Use the appropriate error handling patterns

- Use `thiserror` for library errors
- Use `anyhow` for application errors
- Define error types clearly with `#[from]`
- Add context with `.context()`
- Never use `unwrap()` in production code
- Use `?` instead of `unwrap()` or `expect()`

### 4. Output Formatting

Format output to be readable

- Use `colored` or `nu-ansi-term` for terminal colors
- Use `indicatif` for progress bars and spinners
- Use `comfy-table` or `prettytable-rs` for table output
- Use `serde_json::to_string_pretty` for JSON output
- Use `tracing` for structured logging
- Use `dialoguer` or `inquire` for interactive prompts

### 5. Build Configuration

Configure build tools appropriately

- Use `edition = "2024"` in `Cargo.toml`
- Set `[profile.release]` with `lto = true`, `opt-level = "z"`, `strip = true`
- Set `rust-toolchain.toml` to lock the Rust version
- Use `cargo-watch` for development watch mode
- Use `cargo-nextest` for parallel test execution

### 6. Development Workflow

Use efficient scripts

- Use `cargo watch` for development watch mode
- Use a `justfile` for development scripts
- Run `cargo clippy` and `cargo fmt` before committing
- Use `cargo nextest run` for fast test execution

- Use /follow-tool-cargo if needed
- Use /rethink if needed
- Use /deep-test cli if needed
- Use /run-test if needed


## Expected Outcome

- A CLI project with a good, maintainable structure
- The chosen architecture fits the context and the reasons are recorded
- Directory structure isn't nested too deeply (use `/flatten-directory` if needed)
- An efficient development workflow
- A type-safe CLI application ready for production
- Zero-cost abstractions and memory safety
- Robust error handling
- Readable output with colors and formatting
