---
name: follow-create-zed-extensions
description: Build Zed extensions with Rust/WASM and an extension manifest
argument-hint: "[scope]"
related:
  - follow-create-rust-crate
  - follow-create-sdk
  - follow-lang-rust
  - deep-review-codebase
  - report

---
## Goal

Create a Zed extension project with an `extension.toml` manifest, Rust/WASM code when needed, plus themes, languages, snippets, or language server integrations

## Scope

Use to create Zed extensions that provide languages, themes, icon themes, snippets, debuggers, or MCP servers — supporting both pure-manifest extensions and Rust/WASM custom code

- Package: `zed_extension_api` (crates.io, 0.x — check compatibility with the target Zed version) — always confirm the latest version with `/deep-research` + `/follow-best-practice` (never pinned in this file — per `/update-devin-global-skills`); target `wasm32-wasip2` (wasip1 deprecated), `schema_version = 1`

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create zed extensions)
3. Record the rationale for the chosen stack and libraries for future reference (create zed extensions)

### 2. Determine Extension Type

> Goal: choose the extension type

1. Adding language support: use `languages/` with a `config.toml` and highlights
2. Adding a theme: use `themes/` with JSON
3. Adding snippets: use `snippets/`
4. Language server/debugger/MCP: use Rust/WASM custom code

### 3. Setup Manifest

> Goal: create `extension.toml`

1. Create a root `extension.toml` with `id`, `name`, `version`, `schema_version`, `authors`, `description`, `repository`
2. Declare `themes`, `languages`, `snippets`, `lib` per feature

### 4. Add Rust/WASM Code (If Needed)

> Goal: implement custom code for a language server or debugger

1. Install the Rust target `wasm32-wasip2` with `rustup target add wasm32-wasip2`
2. Create a `Cargo.toml` with `crate-type = ["cdylib"]`
3. Add `zed_extension_api = "0.7.0"` to `Cargo.toml` (latest on crates.io — verify compatibility with the Zed version you want to support)
4. Create `src/lib.rs` with `impl zed::Extension for MyExtension` and `register_extension!`
5. Be aware that `std::env::var` does not work in WASM

### 5. Add Languages

> Goal: add language support

1. Create `languages/{language}/config.toml`
2. Create `languages/{language}/highlights.scm`
3. Declare `path_suffixes`, `line_comments`, `tab_size`

### 6. Add Themes

> Goal: add a theme or icon theme

1. Create `themes/{theme}.json`
2. Follow the theme format from the Zed docs
3. Declare the theme in `extension.toml`

### 7. Test Locally

> Goal: test the extension in Zed

1. Open Zed → Extensions → Install Dev Extension
2. Select the extension directory
3. Check logs with `zed: open log`
4. For a Rust extension, open Zed with `zed --foreground` to see `println!` output

### 8. Publish

> Goal: publish to the Zed extension registry

1. Verify `extension.toml` and `Cargo.toml` are complete
2. Build the Rust extension with `cargo build --target wasm32-wasip2 --release`
3. Create a GitHub repo for the extension (the registry uses a git submodule pointing to this repo)
4. Submit a PR to `zed-industries/extensions`: add the submodule at `extensions/<id>` and an entry in the root `extensions.toml`, with `version` matching `extension.toml`
5. Once the PR is merged → the extension is packaged and published to the Zed extension registry automatically
6. Run `/ship`

## Rules

- `extension.toml` must include `id`, `name`, `version`, `schema_version`
- `id` uses lowercase, hyphens, and no spaces
- Rust code must target `wasm32-wasip2`
- Use `zed_extension_api::current_platform()` instead of `std::env::var`
- Avoid `std::fs` in WASM; use `Worktree` methods

- Use /follow-create-rust-crate if needed
- Use /follow-create-sdk if needed
- Use /follow-lang-rust if needed
- Use /open-in-zed if needed
- Use /report if needed

## Expected Outcome

- `extension.toml` is correct
- The extension installs in Zed as a dev extension
- The Rust/WASM build passes (if present)
- Languages, themes, or snippets work
- Ready to publish to the Zed registry

