---
name: analyze-file-structure
description: Analyze project file and folder structure with a Rust CLI
argument-hint: "[scope]"
related:
  - report-file-structure
  - report
  - follow-create-rust-cli
  - deep-review-codebase

---

## Goal

Scan a project and analyze its file/folder structure with statistics, filtering out build/cache files

## Scope

For viewing the file tree plus file counts, types, and sizes, scanned by a Rust CLI built as a single binary

## Execute

### 1. Install

> Goal: Install the CLI

1. For a global install: `cargo install --git https://github.com/newkub/analyze-file-structure`
2. For a dev build:  clone then `cargo build --release`
3. The binary is at `target/release/analyze-file-structure` when built from source

### 2. Analyze Structure

> Goal: Analyze the file structure

1. Run `analyze-file-structure <path>`
2. Filters `node_modules`, `.git`, `dist`, `build`, `target` by default
3. Set depth with `--depth <N>`
4. View stats with `--stats`
5. View JSON output with `--json`

### 3. Report

> Goal: Report results

1. Use `--json` and pass the output to `/report` or `/report-file-structure`
2. For simple output, use `--stats` and read the values in the terminal
3. To visualize in a browser → use `/report html`

## Rules

- Never modify source files in the scanned project — read-only
- Build/cache files are filtered out by default
- Set a depth limit for large projects
- If the CLI doesn't match the tech stack → run `/deep-review-codebase` first

- Use /follow-create-rust-cli if needed
## Expected Outcome

- A readable file and folder listing
- Basic stats (file counts, types, sizes)
- Build/cache files filtered out
- JSON output supported for downstream tools
