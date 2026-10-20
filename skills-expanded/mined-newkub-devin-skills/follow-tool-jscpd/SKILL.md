---
name: follow-tool-jscpd
description: Set up and use jscpd to detect code duplication in a codebase
argument-hint: "[scope]"
related:
  - refactor
  - report
  - use-scripts
  - run-scan
---

## Goal

Set up and run jscpd to detect code duplication and prioritize refactoring

## Scope

Used for detecting and analyzing code duplication — it does not cover the refactor itself (see `/refactor`)

- Latest: `jscpd@5.3.2` (verified 2026-09-24)
- References: [cli](references/cli.md) | [apis](references/apis.md) 
## Execute

### 1. Setup Configuration

> Goal: create `.jscpd.json` for project-level config

1. Create `.jscpd.json` at the project root with `ignore` patterns for `node_modules`, `dist`, `.turbo`, `coverage`
2. Set `minLines: 5`, `minTokens: 50`, `threshold: 0` (report everything, no exit error)
3. Set `reporters: ["console", "json"]` and `output: "report"`
4. For a monorepo → add `ignore` entries for `/*.lock`, `/bun.lock`, `/.output/`

### 2. Run Duplication Detection

> Goal: run jscpd to detect duplication

1. Run `bunx jscpd . --reporters console,json --output report`
2. For a large project → specify paths: `bunx jscpd ./src ./integrations --reporters console,json`
3. For a CI gate → add `--threshold 10` (exit error when duplication >= 10%)
4. For an HTML report → add `html` to the reporters

### 3. Analyze Results

> Goal: analyze `report/jscpd-report.json`

1. Read `report/jscpd-report.json` to see the `duplicates` array
2. Group duplicates by file and pattern
3. Rank by size (lines, tokens) and frequency (clone count)
4. Separate core-logic duplication from boilerplate and config patterns
5. Run `/report` to summarize as a table

### 4. Plan Refactor

> Goal: plan refactoring based on duplication results

1. Priority 1: duplicated core logic with high impact
2. Priority 2: shared utilities used across workspaces
3. Priority 3: boilerplate that can be extracted into a template or helper
4. Hand off each item to `/refactor`

## Rules

### 1. Configuration

- Use `.jscpd.json` for project-level config — not scattered CLI flags
- `minLines: 5`, `minTokens: 50` — the defaults suit most projects
- `threshold: 0` for report mode, `threshold: 10` for CI mode
- `ignore` must cover: `/node_modules/`, `/dist/`, `/.turbo/`, `/coverage/`, `/*.lock`, `/bun.lock`
- `gitignore: true` to respect `.gitignore` patterns

### 2. Reporters

- `console` — summary in the terminal for quick reading
- `json` — structured output for script parsing
- `html` — interactive report for sharing with the team
- `markdown` — for including in a PR or docs
- `sarif` — for integrating with GitHub Code Scanning

### 3. Detection Modes

- `mild` (default) — skip ignored blocks, new lines, empty symbols — suits most cases
- `strict` — use all token types — for detailed inspection
- `weak` — also skip comments — to reduce noise from comment duplication

### 4. Advanced Clone Detection (v5.2+)

- Type-2 clones: `--ignore-identifiers`, `--ignore-literals`, `--ignore-annotations` — normalize tokens to catch blocks differing only in names/literal values/annotations; clones carry `kind: "exact" | "renamed"` in the JSON report
- Near-miss merge: `--max-gap-lines N` — merge clones separated by at most N unmatched lines into one clone (`kind: "similar"` with a `similarity` score; merges below 0.5 similarity are rejected)
- Function-level similarity (JS/TS only): `--similarity 0.9` — compare every function/method by 4-gram similarity (default `1` = exact match only)

### 5. Monorepo

- Run at the root and use `ignore` patterns to exclude unwanted workspaces
- Or run per workspace: `bunx jscpd ./apps/website/src --reporters console,json`
- Use `--skip-local` to check only cross-workspace duplication
- Add a `report:duplication` script in the root `package.json`: `bunx jscpd . --reporters console,json --output report`

### 6. CI Integration

- Use `--threshold` to fail CI when duplication exceeds the limit (exit 1)
- Use `--reporters sarif` for GitHub Code Scanning — or the GitHub Action `kucherenko/jscpd@v5` (uploads SARIF automatically)
- Use `--baseline .jscpd-baseline.json` + `--fail-on-new-clones` to gate only new duplication — tolerant of legacy clones (`--baseline-from-ref origin/main` needs no committed baseline file; `--update-baseline` refreshes it)
- Use `--fail-on-empty` when an empty scan in CI means misconfiguration (default: warn + exit 0)
- Use `--no-tips` to suppress non-essential messages in CI output
- Use `--exit-code N` to set the exit code when duplication is found (default 1)
- `--cross-formats "javascript,typescript"` (preset `js-ts`) to catch clones across JS/TS
- `--skip-isolated "packages/a|packages/b"` skips cross-folder clones owned by different teams
- `--summary` = codebase summary (top files/folders by tokens/complexity); `--history v5.0.0..HEAD` = duplication trend through git history; `--mcp` = built-in MCP server

- Use /refactor to refactor the duplicates found
- Use /report to summarize results as a table
- Use /use-scripts to parse `report/jscpd-report.json`
- Use /run-scan for additional auditing

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `.jscpd.json` config at the project root
- `report/jscpd-report.json` with duplication results
- A duplicate summary table with refactor priorities
- Handoff to `/refactor` for each high-priority item
