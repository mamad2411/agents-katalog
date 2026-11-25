---
name: diff
description: "Smart diff with impact analysis — dependency chains and blast radius"
category: git
tags: [diff, impact, dependency-chain]
depends-on: [init]
input: "diff scope (file, branch, commit range)"
output: "categorized diff with blast radius analysis"
token-estimate: 3000
parallel-safe: true
argument-hint: "[branch1] [branch2]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Diff

Go beyond raw `git diff` — follow dependency chains, categorize changes, and calculate blast radius.

## Steps

### 1. Identify branches
Parse `<branch1>` and `<branch2>` (default: current vs main). Find common ancestor via `git merge-base`. Read `.ccs/branches/<branch>.md` if they exist.

### 2. Gather raw diff
- `git diff --stat <branch1>...<branch2>` → file-level changes
- `git diff --shortstat <branch1>...<branch2>` → totals
- `git diff --name-only <branch1>...<branch2>` → clean file list
- `git log --oneline <branch1>...<branch2>` → commit list

### 3. Analyze impact
- Read `.ccs/file-index.md` → rank changed files
- Read `.ccs/project-map.md` → find downstream dependents (1 level)
- Flag entry points, configs, shared utilities
- Categorize: feature (new files/exports), fix (small changes), refactor (renames/moves), config

### 4. Calculate blast radius
- Direct changes: files in diff
- First-order dependents: files importing changed files
- Risk level: based on file ranks (S-rank = high risk)
- Breaking change potential: exports removed, interfaces changed, types modified

### 5. Generate report
Output: change type, risk level, direct changes count, blast radius count. Table of changed files by importance (file, rank, +/-, dependents). Dependency impact table. Change categories breakdown. Commits list. Risk assessment (breaking changes, S-rank mods, shared utils, test coverage).

Update `.ccs/branches/<branch-name>.md` with analysis.

### 6. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: branches compared, direct changes, blast radius, risk level, change type.

## Rules
- Use `--name-only` and `--stat` — never full diff output
- Read file-index and project-map once, not per file
- Grep for import statements rather than reading entire files
- Cap dependency walking at 1 level
- For 100+ file diffs → summarize top 20 by rank

## Refs
- Branch refs: `.ccs/branches/`
- File index: `.ccs/file-index.md`
- Project map: `.ccs/project-map.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
