---
name: follow-tool-cargo
description: Configure Cargo lint rules and workspace lint configuration
argument-hint: "[scope]"
related:
  - deep-analyze
  - run-verify
  - follow-lang-rust
  - follow-tool-mr-boxington

---

## Goal

Configure Cargo lint rules and workspace lint configuration in `Cargo.toml`

## Scope

For configuring Cargo lint rules in Rust projects, both single crate and workspace (Rust 1.98+)

- Boundary: this skill covers only lint/toolchain config (`[lints]`, `[workspace.lints]`, clippy, fmt, hooks) — for Rust language/idioms see `/follow-lang-rust`; to verify after config use `/run-verify`; for Cargo build cache (mbx) see `/follow-tool-mr-boxington`
- Latest: Rust `1.98.1` (cargo `1.98.1`) (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
- For Clippy lint rules and error handling see `references/cli.md`

## Execute

### 1. Analyze Project

> Goal: inspect the project structure to identify single crate or workspace

1. Run `/deep-analyze` to see the project structure
2. Inspect the existing `Cargo.toml`
3. Check the workspace configuration
4. Determine whether it is a single crate or a workspace

### 2. Configure Cargo.toml Lint Rules

> Goal: add lint attributes in the `[lints]` section for Rust and Clippy

1. Add lint attributes in the `[lints]` section:
   ```toml
   [lints.rust]
   unused_extern_crates = "warn"
   unused_import_braces = "warn"
   unused_qualifications = "warn"
   variant_size_differences = "warn"
   missing_docs = "warn"
   ```

2. Add clippy lint rules:
   ```toml
   [lints.clippy]
   all = "warn"
   pedantic = "warn"
   nursery = "warn"
   ```

3. For a workspace use `[workspace.lints]`:
   ```toml
   [workspace.lints.rust]
   unused_extern_crates = "warn"
   unused_import_braces = "warn"
   unused_qualifications = "warn"

   [workspace.lints.clippy]
   all = "warn"
   pedantic = "warn"
   ```

4. See details in 

### 3. Configure Workspace Lints

> Goal: set workspace-level lint rules and inheritance for member crates

1. Set workspace-level lint rules in the root `Cargo.toml`
2. Use `[workspace.lints]` for shared lint rules
3. Each crate can inherit with:
   ```toml
   [lints]
   workspace = true
   ```
4. See details in 

### 4. Setup Pre-commit Hooks

> Goal: install pre-commit hooks to enforce lint rules automatically

1. Install `lefthook` or `pre-commit`
2. Add hooks for:
   - `cargo check --all-targets`
   - `cargo clippy --all-targets -- -D warnings`
   - `cargo fmt --check`
3. Configure in `lefthook.yml`:
   ```yaml
   pre-commit:
     true
     commands:
       check:
         run: cargo check --all-targets
       clippy:
         run: cargo clippy --all-targets -- -D warnings
       fmt:
         run: cargo fmt --check
   ```

### 5. Verify Configuration

> Goal: run verification commands to confirm the lint rules work

1. Run `cargo check --all-targets`
2. Run `cargo clippy --all-targets -- -D warnings`
3. Confirm the lint rules behave correctly
4. Run `/run-verify` to confirm everything works

## Rules

### 1. Rust Lint Categories

- `unused_extern_crates`: warn (unused external crates)
- `unused_import_braces`: warn (unused import braces)
- `unused_qualifications`: warn (unused type qualifications)
- `variant_size_differences`: warn (enum variant size differences)
- `missing_docs`: warn (missing documentation)
- See 

### 2. Clippy Lint Categories

- `all`: warn (all clippy lints)
- `pedantic`: warn (pedantic lints)
- `nursery`: warn (experimental lints)
- See 

### 3. Workspace Configuration

- Set lint rules at the workspace level in the root `Cargo.toml`
- Use `[workspace.lints]` for shared lint rules
- Each crate can inherit with `workspace = true`
- Each crate can override rules when necessary
- See 

- Use /deep-analyze if needed
- Use /follow-lang-rust if needed
- Use /run-verify if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Cargo lint rules configured automatically
- Workspace lint configuration applied
- Pre-commit hooks enforce lint rules
- Consistent code quality across the project
