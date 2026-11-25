---
name: check-long-files
description: Detect and report files longer than 250 lines with a Rust CLI
argument-hint: "[threshold]"
related:
  - refactor
  - simplify
  - deep-review-codebase
  - check-code-structure
---

## Goal

Detect and report source-code files whose line count exceeds the given threshold (default 250)

## Scope

Use for scanning `.ts`, `.tsx`, `.js`, `.jsx` files in a workspace without modifying the originals.
This skill uses a Rust CLI instead of a Bun/TS CLI because it needs high performance and a dependency-free binary

## Execute

### 1. Build CLI

> Goal: build the Rust CLI from the source in the skill directory

1. Check that `Cargo.toml` and `src/main.rs` exist in the skill directory
2. Run `cargo build --release` in the skill directory (first build only)
3. Check that the binary exists at `target/release/check-long-files` (or `.exe` on Windows)

### 2. Run CLI

> Goal: run the CLI in the target workspace

1. Change the working directory to the target workspace root
2. Run `<skill-dir>/target/release/check-long-files [threshold]`
3. Get the result: the list of files exceeding the threshold, sorted most to least

### 3. Triage Results

> Goal: separate files that need refactoring from cohesive catalogs

1. A flagged file is not automatically a defect — read the implementation before judging
2. Acceptable cohesive units: single-class fluent API (e.g. `FxImpl`), declarative catalogs (e.g. schema combinators, op delegates), barrel/facade
3. Refactor targets: mixed concerns (several features in one file), separable shared module state, function groups that clearly cohere into subgroups
4. Hand off to `/refactor` with the triaged target list — files long purely from verbosity/redundancy (not mixed concerns) → `/simplify`

## Rules

### 1. File Discovery

- Use the `ignore` crate to walk files and respect `.gitignore` automatically, in both git and non-git repos
- Filter to files with the `.ts`, `.tsx`, `.js`, `.jsx` extensions only
- Do not hardcode skip directories

### 2. Line Counting

- Use `BufReader::lines()` to count lines
- Skip files that are missing or unreadable
- Never modify the original files

### 3. Threshold And Output

- Take the threshold from the first argument, default 250
- Keep only files above the threshold
- Sort by line count, most to least
- Show each file name and line count
- Show the total number of files exceeding the threshold

- Use /refactor if needed
- Use /deep-review-codebase if needed
- Use /check-code-structure if needed

## Expected Outcome

- The CLI binary builds successfully
- Reports files longer than the threshold
- Shows file names and line counts
- Sorted from most to least
- Shows the total number of files exceeding the threshold
- No files in the target workspace are modified
