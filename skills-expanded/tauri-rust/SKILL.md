---
name: tauri-rust
description: Implement Tauri 2 Rust commands, managed state, validation, errors, and native integrations. Use when changing `src-tauri`, exposing commands, or reviewing Rust-side application logic.
---

# Tauri Rust

## Workflow

1. Read `src-tauri/Cargo.toml`, `lib.rs`/`main.rs`, command registration, state setup, and existing error conventions.
2. Define a narrow command with serializable arguments and return values. Validate paths, URLs, sizes, identifiers, and authorization context before side effects.
3. Use [managed state](https://v2.tauri.app/develop/state-management/) for shared application state; choose synchronization deliberately and avoid holding locks across slow I/O or callbacks.
4. Return structured, user-safe errors to the frontend while logging diagnostic context without secrets.
5. Register the command exactly where the application already registers commands, then run `cargo fmt --check`, `cargo check`, and relevant tests.

## Safe defaults

- Prefer standard Rust error handling and typed domain errors over `unwrap()` in command paths.
- Canonicalize and constrain filesystem paths before access; do not accept a frontend path as trusted.
- Keep blocking work off the UI thread and use async only where the operation and runtime support it.
- Use the [Tauri 2.0 API reference](https://docs.rs/tauri/2.0.0/tauri/) for signatures matching the crate actually installed; verify newer crate versions against their corresponding docs.rs version.

A command is a security boundary, not merely a convenience wrapper. Pair implementation changes with capability/permission review.
