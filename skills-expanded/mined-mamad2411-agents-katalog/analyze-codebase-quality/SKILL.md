---
name: analyze-codebase-quality
description: Analyze codebase quality with the analyze-codebase-quality CLI
argument-hint: "[scope]"
related:
  - deep-validate
  - check-code-structure
  - report
  - suggest-next-action

---

## Goal

Analyze codebase quality with the `analyze-codebase-quality` CLI

## Scope

For TypeScript/JavaScript projects that need an 8-dimension quality report

## Execute

### 1. Install

> Goal: Install the CLI

1. `bun add -g github:newkub/analyze-codebase-quality` — not on npm (verified 2026-09-12)
2. Or clone `https://github.com/newkub/analyze-codebase-quality.git` then `bun install && bun run build`

### 2. Analyze

> Goal: Run the analyzer on the target project

1. Get the target path from the user
2. Run `analyze-codebase-quality <path>`
3. If the CLI fails → report the error to the user

### 3. Validate And Report

> Goal: Summarize results and validate

1. Run `/deep-validate` to check the output
2. Run `/report` if there are tables
3. Run `/suggest-next-action`

## Rules

### 1. CLI

- `analyze-codebase-quality` is the source of truth
- If the CLI cannot be invoked → install or build it first
- Keep under 250 lines

- Use /check-code-structure if needed — `sg outline` adds the symbol-level metrics (top-level symbols, exports, members) the CLI doesn't cover

## Expected Outcome

- Codebase quality report with evidence
- Summary table
- Clear next action
