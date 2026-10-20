---
name: follow-create-tui-ratatui
description: Build TUI applications with Rust and Ratatui
argument-hint: "[scope]"
related:
  - design-tui-prototype
  - follow-create-rust-cli
  - deep-review-codebase
  - run-test
  - follow-single-responsibility
  - follow-release

---

## Goal

Build a TUI application with Rust using the Ratatui library

## Scope

- Create a TUI project with Rust from scratch
- Supports layout, components, events, state, and styling
- No web stack
- Layout/keys/states not agreed yet → design them first in chat via `/design-tui-prototype`, then implement here

- Packages: `ratatui` (latest stable, MSRV per crates.io — 0.30 requires Rust 1.88+), `crossterm` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Review the stack

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Confirm the use of Rust + Ratatui + crossterm
3. Record the rationale for the chosen stack

### 2. Setup Rust Project

> Goal: Create the scaffold

1. Run `/follow-create-rust-cli` for the Rust project structure — or scaffold from the official templates: `cargo install cargo-generate` then `cargo generate ratatui/templates <name>`
2. `cargo add ratatui crossterm anyhow` (or `color-eyre`) — crossterm is the default backend; alternatives via features: `termion`, `termwiz`, `termina` (`--no-default-features --features <backend>`)
3. Run `cargo build` to verify the setup

### 3. Setup Terminal

> Goal: Configure the terminal

1. Use the 0.30 helpers: `ratatui::init()` / `ratatui::try_init()` / `ratatui::restore()` or `ratatui::run(app)` for simple apps (automatically handles raw mode + alternate screen + restore); the manual path uses `Terminal::new(CrosstermBackend::new(stdout()))` + `terminal.draw(render)`
3. If setting up manually: configure `enable_raw_mode` and `enter_alternate_screen` with `CrosstermBackend`
4. Set a `PanicHook` (or `color-eyre`) to restore terminal state
5. Handle graceful shutdown on exit

### 4. Create Layout

> Goal: Create the layout

1. Use `Layout` and `Constraint` from `ratatui::layout`
2. Define directions (horizontal, vertical)
3. Define sizes (percentage, fixed, min, max)
4. Split the layout into clearly nested structures

### 5. Build Components

> Goal: Create UI components

1. Use `Paragraph`, `Block`, `Borders` for text
2. Use `List`, `ListItem` for lists
3. Use `Table`, `Row`, `Cell` for tables
4. Use `Gauge`, `Sparkline` for progress and charts

### 6. Handle Events

> Goal: Handle events

1. Create an event loop with `crossterm::event`
2. Handle `KeyEvent` and `MouseEvent`
3. Handle terminal resize events
4. Use `/follow-single-responsibility` to separate event handling from rendering

### 7. State Management

> Goal: Manage state

1. Separate business logic from render logic — use the Elm Architecture (TEA) pattern: `Model` struct + `Message` enum + `update(model, msg)` + `view(model, frame)`
2. Use structs for state management
3. Handle state updates in the event loop
4. Use immutable updates where possible

### 8. Style And Polish

> Goal: Handle styling

1. Use `Style`, `Color`, `Modifier` from `ratatui::style` — or `Stylize` methods on `Line`/`Span`/`&str` (`.red()`, `.bold()`, `.bg()`, `.on_<color>()`)
2. Create design tokens for colors and borders
3. Check contrast and readability
4. Use consistent styling across all components

### 9. Test And Validate

> Goal: Validate the TUI

1. Run `cargo build` and `cargo test` — use `ratatui::backend::TestBackend` + `assert_buffer()` to snapshot-test rendering
2. Run `/run-test all` if there are integration tests
3. Run `/deep-review-codebase` to check usability
4. Test event handling on a real terminal

### 10. Package And Ship

> Goal: Deliver the TUI

1. Check the `Cargo.toml` metadata
2. Create a release build with `cargo build --release`
3. Run `/follow-release` if publishing
4. Test the binary on the target platform

## Rules

### 1. Stack

- Rust only
- Use Ratatui for the TUI
- Don't use a web stack for the TUI

### 2. Quality

- Run `/follow-single-responsibility` after building major components
- Run `/implement-to-production` when done
- Support error handling with `Result`

### 3. Terminal Management

- Always restore terminal state on panic or exit
- Pair `enable_raw_mode()` / `disable_raw_mode()` and `enter_alternate_screen()` / `exit_alternate_screen()` as matched sets
- Set a `PanicHook` to restore terminal state
- Use `Constraint` instead of hardcoded sizes, and keep layout state separate from render logic
- Handle partial updates and use `Frame` for area calculations — `Frame::render_widget` for `Widget`, `render_stateful_widget` for `StatefulWidget`
- Docs: https://ratatui.rs/ + https://docs.rs/ratatui/latest/ratatui/ — companion crates `ratatui-core`, `ratatui-widgets`, `ratatui-macros` can be used separately

### 4. Safety

- Never commit secrets to the repository
- Use `/follow-secret-manager` for secrets
- Use `environment variables` for non-sensitive config
- If there are destructive changes → dry run first

## Expected Outcome

- TUI application runs with Rust + Ratatui
- Layout, components, event handling, and state management are complete
- Error handling is supported
- Tests pass or a plan exists
- The binary can be built and run
