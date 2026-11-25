---
name: rust-coding-standard
description: Rust coding standards for the splitfire-agent crate. Covers error handling, naming, async patterns, tool/toolset conventions, deterministic music computation, logging, and clippy compliance. Apply to all Rust edits.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: false
---

# Rust Coding Standard

Rules for writing Rust in the `splitfire-agent` crate. These are traps to avoid, not maps to follow.

This crate holds only the *music* part of a music-domain ACP agent. The ACP server, session/turn
loop, approval, workspace tools, terminal UI and MCP layer all come from the Onde Agent Platform
crates (`ed-acp`, `ed-acp-tui`, `ed-mcp`). When something is protocol-, session-, or
approval-related, it belongs there, not here.

---

## Correctness First

Prioritize correctness and clarity. Performance is secondary unless explicitly stated. Complete,
mostly-correct code beats perfect code that doesn't solve the problem.

The music theory and audio code exists so the model *computes* answers instead of recalling them.
Results must be exact: diatonic spelling (letter plus accidental, never bare pitch classes), so C#
major really has E# and B#. A plausible-but-wrong answer is worse than no tool at all.

## Error Handling

- This crate uses `anyhow` throughout. There is no custom error enum and no `thiserror`; don't
  introduce one unless a real need appears.
- Propagate errors with `?`. Return `anyhow::Result<T>`. Use `anyhow!("...")` and `.context("...")`
  to add meaning at the point of failure.
- Never call `.unwrap()` or `.expect()` outside of `#[cfg(test)]` code.
- Never silently discard errors with `let _ =` on fallible operations:
  - Propagate with `?` when the caller should handle it.
  - Use `tracing::warn!` or `tracing::error!` when you need to ignore but want visibility.
  - Use `match` or `if let Err(error)` when custom recovery logic is needed.
- Tool handlers return `Result<ToolOutcome>`; surface a clear message for bad arguments
  (`Err(anyhow!("unknown tool `{name}`"))`) rather than panicking.
- Be careful with indexing operations that may panic if out of bounds. Prefer `.get()` and safe
  alternatives — especially when indexing audio sample buffers or note arrays.

## Naming

- Use full words for all variable and parameter names. No single-letter names, no abbreviations
  (`progression` not `prog`, `argument` not `arg`, `error` not `e`).
- `snake_case` for functions and variables, `CamelCase` for types, `SCREAMING_SNAKE_CASE` for
  constants.
- Tool name constants and the env prefix follow the existing style: screaming-snake constants
  (`NAME`, `INFO`, `DEMUCS`), env vars prefixed `SPLITFIRE_`.
- Tool names are lowercase with underscores and a domain prefix: `theory_scale`, `theory_chord`,
  `analyze_audio`, `list_separations`.

## Comments

- Comments explain **why**, never **what**. Do not write comments that summarize or re-describe the
  code.
- Doc comments (`///` on items, `//!` at module top) are encouraged — they explain the contract and
  the design intent. The existing modules lead with a `//!` that states the invariant (e.g.
  "Deterministic music theory: pure functions, no I/O"). Keep that style.
- Do not add organizational separators like `// --- Helper functions ---` unless they are already
  established in the file's style.

## Module Structure

- This crate already uses `mod.rs` as the module root for `tools/`, `theory/` and `audio/`. Follow
  the existing layout — add new theory under `src/theory/`, new audio under `src/audio/`, new tools
  under `src/tools/`. Do not restructure established module roots.
- Prefer implementing functionality in existing files unless it's a genuinely new logical component.
  Avoid creating many small single-purpose files.
- Keep the layering intact:
  - `src/theory/` and `src/audio/` are pure computation — no ACP types, and `theory` does no I/O.
  - `src/tools/` adapts that computation into `Toolset` entries.
  - `src/profile.rs` is the single wiring point (identity, prompt, toolsets, slash commands,
    built-in demucs). `src/prompt.rs` holds the system prompt and slash commands.
- `src/lib.rs` is the embeddable library (the `Profile` for hosts using `ed_acp::serve`);
  `src/main.rs` is the binary (TUI / `--acp` / `--setup` / `--list-models`). Keep library logic out
  of `main.rs`.

## Adding or Changing a Tool

`MusicTools` is one `Toolset`. When you add or change a tool, update all of these together:

1. `definitions()` — the JSON schema for the tool's arguments.
2. `handles()` — the name match so the toolset claims the call.
3. `describe()` — the human title, `ToolKind`, and any `ToolCallLocation`s.
4. `execute()` — the dispatch arm that runs it.

Music tools are read-only and never ask for approval. Anything that writes files or runs commands
belongs to `ed-acp`'s workspace tools, not here.

## Async

- Runtime is `tokio` (`features = ["full"]`). Use `tokio::sync::Mutex`, not `std::sync::Mutex`, for
  async-held locks.
- `Toolset::execute` is `async` (via `async_trait`). Keep pure theory synchronous (it is) and only
  reach for `async` where there is real I/O (audio decode, the separation library, demucs).
- Use variable shadowing to scope `.clone()` calls inside async closures, minimizing borrow
  lifetimes:

```rust
tokio::spawn({
    let server = server.clone();
    async move {
        server.start().await;
    }
});
```

## Logging

- Use the `tracing` crate macros: `tracing::debug!`, `tracing::info!`, `tracing::warn!`,
  `tracing::error!`. Logs go to stderr via `RUST_LOG`.
- No `println!` or `eprintln!` in library code (`src/lib.rs` and everything it pulls in). The one
  place direct stdout is correct is `src/main.rs` CLI output (`--version`, `--list-models`), where
  the printed text is the program's result.
- Log at `debug` for routine operations, `info` for lifecycle events (demucs started/disabled),
  `warn` for recoverable issues (an MCP server that failed to start), `error` for failures.

## Edition and Toolchain

- Edition 2024. Prefer modern idioms it enables.
- Dependencies are pinned in `Cargo.toml`; reuse what's already there (`symphonia`, `ebur128`,
  `realfft`, `serde`/`serde_json`, `uuid`) before adding a crate.

## Clippy Compliance

All code must pass `cargo clippy --locked --all-targets -- -D warnings`. Common traps:

- `&PathBuf` in function parameters → use `&Path` instead.
- `unwrap_or_else(Type::default)` → use `unwrap_or_default()`.
- `filter_map(|x| { ... Some(y) })` where every path returns `Some` → use `map`.
- `.map(|x| f(x))` where `f` is a plain function → use `.map(f)`.
- Redundant type annotations in closures: `.map(|note: &String| note.trim())` → `.map(|note| note.trim())`.
- Prefer `and_then(Value::as_str)` over a closure, matching the existing arg-parsing style.

## Testing

- Unit tests go in a `#[cfg(test)] mod tests` block at the bottom of the file they test — this is
  where the theory and audio correctness lives, so test exact spellings and edge cases (enharmonics,
  dotted/triplet tempo, cents offsets).
- Use `#[tokio::test]` for async tests.
- Tests may use `.unwrap()` and `.expect()` — the panics are the assertions.
- Test names describe the scenario: `transpose_keeps_enharmonic_spelling`, not `test_transpose` or
  `test_1`.
- Integration tests (`tests/`) run the real binary against a scripted mock model and a test MCP
  server, and include the platform conformance suite from `ed-acp-testkit`. Shared helpers live in
  `tests/common/`.
- `tests/live.rs` hits real Onde Cloud and is skipped unless `ONDE_API_KEY=app-id:app-secret` is set.

## Build Verification

Always run `cargo check` before returning work. If code does not compile, fix it — do not return
with TODOs. Before pushing, run exactly what CI runs:

```sh
cargo fmt -- --check
cargo clippy --locked --all-targets -- -D warnings
cargo test --locked
```

To also check the embeddable library alone (no TUI, no MCP test stub):

```sh
cargo check --no-default-features
```
