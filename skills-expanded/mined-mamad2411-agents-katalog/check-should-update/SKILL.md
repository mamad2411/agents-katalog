---
name: check-should-update
description: Inspect git changes to decide whether a target needs updating
argument-hint: "<target>... [--refs <from-ref..to-ref>]"
allowed-tools:
  - exec
  - grep
  - glob
  - find_file_by_name
  - read
related:
  - deep-review-codebase
  - follow-create-rust-cli
  - follow-tool-git
  - refactor
  - update-devin-global-skills

---

## Goal

Inspect the git changes of the target paths to decide whether to update, skip, or create new

## Scope

Use in any workflow that must check whether a target needs updating based on code changes, before starting work.
This skill ships a Rust CLI for fast checks and use outside Devin.

## Execute

### 1. Build CLI

> Goal: build the Rust CLI from the source in the skill directory

1. Check that `Cargo.toml` and `src/main.rs` exist in the skill directory
2. Run `cargo build --release` in the skill directory
3. Verify the binary is at `target/release/check-should-update` (or `.exe` on Windows)

### 2. Run CLI

> Goal: run the CLI in the target workspace

1. Change the working directory to the target project root
2. Run the command `<skill-dir>/target/release/check-should-update.exe <target>... [--refs <from-ref..to-ref>]`
3. The default ref range is `HEAD~1..HEAD`
4. Accept the result: `skip`, `update`, or `create`

### 3. Check Changes

> Goal: interpret the result correctly

1. If any target does not exist yet → return `create`
2. If every target is in a git repo and there are no changes → return `skip`
3. If every target is in a git repo and at least one path has changes → return `update`
4. If not in a git repo or the git command fails → return `update` with a warning

## Rules

### 1. Target Paths

- The calling workflow must specify the target path(s) to check
- Use glob patterns supported by `git diff --name-only`
- Both files and directories are supported

### 2. Return Values

- `skip` — no changes, move on to validate
- `update` — changes found, continue with the next steps
- `create` — target does not exist yet, continue with the creation steps

### 3. CLI Behavior

- `refs` defaults to `HEAD~1..HEAD`
- If `HEAD~1` does not exist (root commit or fresh repo) → the CLI returns `update` when the target exists
- If `refs` is user-supplied and the git command fails → the CLI returns exit code 1
- Use `-v` or `--verbose` to see the reasoning on `stderr`

- Use /deep-review-codebase if needed
- Use /follow-create-rust-cli if needed
- Use /follow-tool-git if needed
- Use /refactor if needed
- Use /update-devin-global-skills if needed (should update)

## Expected Outcome

- Know whether the target needs `skip`, `update`, or `create`
- No wasted time updating when nothing changed
- The Rust CLI builds cleanly and works correctly
