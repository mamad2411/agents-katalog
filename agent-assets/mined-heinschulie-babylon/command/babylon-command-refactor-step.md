---
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
description: Scoped refactor step for the red-green-refactor loop — redesigns a naive TDD green-pass into an optimal solution for a single issue while keeping all tests green
argument-hint: [adw_id] [issue_number] [issue_body] [pre_tdd_sha] [changed_files]
model: opus
---

# Purpose

Redesign the naive TDD green-pass implementation into an optimal solution for the current issue, while keeping all tests green. This is the "refactor" phase of red-green-refactor — a **design task**, not a code quality sweep. Every change must trace back to a better implementation of the specified issue. Follow the `Instructions` and `Workflow` to redesign the naive solution, then produce the `Report`.

## Variables

adw_id: $1
issue_number: $2
issue_body: $3
**pre_tdd_sha: $4**
**changed_files: $5**

## Design Principles

Apply these when evaluating refactor opportunities:

**Deep modules** — small interface + deep implementation. Reduce method count, simplify parameters, hide complexity inside. Avoid shallow modules (large interface, thin implementation that just passes through).

**Interface design for testability** — accept dependencies (don't create them internally), return results (don't produce side effects), minimize surface area (fewer methods = fewer tests needed).

**Refactor candidates** — duplication (extract function/class), long methods (break into private helpers, keep tests on public interface), shallow modules (combine or deepen), feature envy (move logic to where data lives), primitive obsession (introduce value objects).

## Instructions

- IMPORTANT: This is a scoped refactor for issue #$2 only. You are NOT scanning for general code quality improvements across the codebase.
- **Only refactor files in the changed files list above.** Do not explore or modify files outside this set.
- The green-pass was intentionally minimal — your job is to implement the *right* design for this issue.
- IMPORTANT: Do NOT fix unrelated code quality issues you encounter along the way. If you see duplication, poor naming, or structural problems in code unrelated to issue #$2, leave them alone.
- Do NOT add new features or functionality beyond the issue scope.
- Do NOT write new tests. Do NOT modify existing tests. The test contract is sacrosanct.
- Do NOT change observable behavior.
- All existing tests must continue to pass after each change. If a change breaks a test, revert it.
- Apply changes one at a time. After EACH change, run `bun run test`.
- **If after reading the changed files you determine no design improvement is warranted, report that immediately and exit. Do not explore unrelated code.**
- IMPORTANT: For every file you modify, you must be able to justify how it serves issue #$2. If you cannot justify a change, do not make it.
- Do not run `git diff` — the changed files are listed above.

## Workflow

1. Read the `issue_body` carefully. This is the design goal — internalize what problem is being solved.
2. Read the files listed in `changed_files` and their corresponding tests to understand the naive implementation.
3. Run `bun run test` to establish a green baseline. If tests fail, STOP and report the failure — do not refactor broken code.
4. Think hard about the optimal solution for issue #$2 using the Design Principles above. The green-pass gave you working code — now redesign it properly. If no design improvement is warranted, report "no changes needed" and exit.
5. Apply changes one at a time. After EACH change, run `bun run test`. If a change breaks a test, revert it immediately.
6. Once all changes are complete, produce the `Report`.

## Report

Output a structured report with these two sections:

### Changes

For each file modified, list:
- **File**: `path/to/file`
- **Justification**: One sentence explaining how this change serves a better implementation of issue #$2

### Summary

- Total files modified
- Run `git diff --stat $4 HEAD` to show the final diff
- Brief description of the design improvement achieved

## Step Summary

IMPORTANT: You MUST end your output with this exact block. Fill in each field with a single line.

## Step Summary
- status: pass | fail
- action: <one line describing what you did>
- decision: <one line -- key choice and why>
- blockers: <one line, or "none">
- files_changed: <comma-separated list, or "none">
