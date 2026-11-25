---
name: diff-file-history
description: Compare one file across git history — evolution, regressions, and change patterns
argument-hint: "<path> [range]"
related:
  - git-file-history
  - report

---

## Goal

Analyze a file's evolution across git history — when it changed, what changed, by whom, additions or removals — to understand context, locate regression points, or trace decision history

## Scope

- Inspect a single file across commits: change frequency, growth/shrink, major rewrites, regression points
- Covers: per-commit diffs, line counts over time, blame patterns, rename history
- Read-only: analysis from git — never modifies files or history
- Boundary: evolution/pattern analysis only — find commits matching a condition → `/check-git-logs`; interactive viewer → `/git-file-history`

## Execute

### 1. Trace File History

> Goal: map the file's commit timeline

1. `git log --follow --oneline -- <path>` — includes rename history via `--follow`
2. Identify: when it was created, renamed from what, last modified when
3. Flag: long gaps in history (abandoned file?) vs very frequent changes (hotspot?)

### 2. Measure Evolution

> Goal: measure how the file changed over time

1. Line count per commit: `git log -p` or `git show <sha>:<path> | measure` — growth trend
2. Commit authors per file — who are the primary owners
3. Classify commits: features, fixes, refactors — from messages + diff nature

### 3. Find Key Changes

> Goal: find the commits with significant changes

1. Major rewrites: commits with unusually large diffs (>50% of the file)
2. Regression candidates: if there is a current bug → bisect-style search for the introducing commit
3. `git log -S"<pattern>"` — find when a string/symbol entered or left (pickaxe)
4. `/deep-review-codebase` or `/git-file-history` for detailed diffs of commits of interest

### 4. Report Evolution

> Goal: summarize the history as insight

1. Use `/report`: `No.`, `Commit`, `Date`, `Author`, `Lines Δ`, `Type`, `Significance`
2. Timeline summary: created → major changes → current state
3. Insights: hotspot (frequent changes = should split/refactor?), stable (untouched for a long time), regression point (if found)

## Rules

### 1. Follow Renames

- Always use `--follow` — history stays continuous across renames
- Include pre-rename history in the analysis

### 2. Evidence-Based

- Every claim cites real commit SHAs — never conclude from messages alone
- Line counts and diff sizes must be actually measured

### 3. Purpose Driven

- Answer the question the user needs — regression hunt, context, ownership — do not dump raw history
- State limitations: shallow clones and history rewrites make history incomplete

## Expected Outcome

- The file's timeline with key commits
- Change patterns: hotspot vs stable, growth trend, ownership
- Regression point if found, with a precise commit SHA
