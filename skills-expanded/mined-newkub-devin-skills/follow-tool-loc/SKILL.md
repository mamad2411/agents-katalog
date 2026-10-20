---
name: follow-tool-loc
description: Use the loc tool to count lines of code fast, filter files, and analyze file sizes
argument-hint: "[path] [options]"
related:
  - check-long-files
  - report-file-structure
  - scan-codebase
  - use-scripts
---

## Goal

Use the `loc` tool to count lines of code by language and file, with conditional file filtering

## Scope

For projects that already have `loc` installed — covers counting lines, filtering files, and analyzing file sizes

- Latest: `loc@0.5.0` (crates.io, verified 2026-09-26; npm `loc@0.6.1` is a different project) — latest release 2018 (the tool is dormant; the author himself suggests `scc` in the README); for a maintained alternative consider `tokei` or `scc`
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Check Prerequisites

> Goal: confirm `loc` is installed and ready

1. Check whether `loc` is installed: `loc --version`
2. If absent → install with `cargo install loc` or download a binary from https://github.com/cgag/loc/releases
3. If Rust/Cargo is missing → install from https://www.rustup.rs/

### 2. Count Lines Of Code

> Goal: count lines of code by language and path

1. Run `loc` to count lines of code for the whole project: `loc`
2. Specify a path: `loc src/` or `loc ci benches`
3. The result is a table per language: Files, Lines, Blank, Comment, Code

### 3. Show Per-File Statistics

> Goal: show file-level statistics with sortable ordering

1. Run `loc --files` for file-level statistics
2. Use `--sort` for ordering:
   - `--sort Code` (default) — by code lines
   - `--sort Lines` — by total lines
   - `--sort Comment` — by comment count
   - `--sort Blank` — by blank lines
3. `Language` and `Files` are valid only without `--files`

### 4. Filter Files

> Goal: Filter Files

1. Use `--include <REGEX>` to keep only matching files:
   - `loc --include '\.ts$'` — TypeScript files only
   - `loc --include 'src/'` — files under src/ only
2. Use `--exclude <REGEX>` to skip matching files:
   - `loc --exclude 'sh$'` — exclude shell scripts
   - `loc --exclude 'node_modules/'` — exclude node_modules
3. Several `--include` or `--exclude` flags can be combined (OR logic)
4. Use `-u` to bypass `.gitignore` and `-uu` to include hidden files

### 5. Filter Long Files

> Goal: Filter Long Files

1. Run `loc --files --sort Lines` then pipe to filter files over the threshold:
   ```bash
   pwsh -NoProfile -Command "loc --files --sort Lines | Select-String -Pattern '^\|' | ForEach-Object { $line = $_.Line; if ($line -match '\|\s*(\S+)\s+(\d+)\s+') { if ([int]$Matches[2] -gt 250) { $line } } }"
   ```
2. Change `250` to the wanted threshold
3. See `/check-long-files` for the dedicated workflow

## Rules

### 1. Installation

- Install via `cargo install loc` or download a binary from the releases page
- Rust/Cargo is required before installing via cargo
- Supports Windows, macOS, and Linux

### 2. CLI Flags

- `--files` — show file-level statistics (default: per-language summary only)
- `--sort <COLUMN>` — order by column: `Code`, `Comment`, `Blank`, `Lines`, `Language`, `Files` (default: `Code`)
- `--include <REGEX>` — keep only files matching the regex (multiple flags supported, OR logic)
- `--exclude <REGEX>` — skip files matching the regex (multiple flags supported, OR logic)
- `-u` / `--unrestricted` — bypass `.gitignore` (use `-uu` to include hidden files)
- `[target]...` — paths or files (default: current directory)

### 3. Output Format

- The table shows columns: Language, Files, Lines, Blank, Comment, Code
- Use `--files` for the per-file breakdown (lines start with `|`)
- Results are sorted high→low by the chosen `--sort` column

### 4. Regex Syntax

- `--include` and `--exclude` use Rust regex syntax
- Use `\.ts$` for .ts files (the dot must be escaped)
- Use `src/` for files whose path contains `src/` in any directory
- Multiple flags use OR logic: `--include '\.ts$' --include '\.tsx$'` matches both .ts and .tsx

### 5. Performance

- `loc` is 100x faster than `cloc` and 2-10x faster than `tokei`
- Uses parallel processing with a worker pool across all CPU cores
- Uses byte-level iteration for high speed
- Filter with `--include`/`--exclude` before counting to cut run time

- Use `/report-file-structure` to report the file structure
- Use `/scan-codebase` for further codebase scanning
- Use `/use-scripts` to post-process the output
- Use /check-long-files if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Line counts by language and file are known
- Files can be filtered by type or path
- Files longer than the threshold can be identified
- Clear tabular output, ordered as wanted
