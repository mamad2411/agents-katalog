---
name: log
description: "Smart commit history with context and task.md cross-references"
category: git
tags: [history, commits, cross-ref]
depends-on: [init]
input: "log scope (branch, range, all)"
output: "formatted commit history with task cross-references"
token-estimate: 1500
parallel-safe: true
argument-hint: "[branch] [--all] [--since=7d]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-haiku-4-5-20251001
context: fork
agent: general-purpose
---

# Log

Display commit history enriched with `.ccs/` context — groups by branch, cross-references with task.md entries.

## Steps

### 1. Parse arguments
- No args → last 20 commits on current branch
- `<branch>` → commits on specific branch
- `--all` → commits across all branches
- `--since=<period>` → filter by time (7d, 2w, 1m)

### 2. Gather git history
- `git log --oneline --graph --all -30` → visual overview
- `git log --format="%h|%s|%an|%ar|%D" -20 <branch>` → structured data
- If `--all` → `git log --oneline --all --since=<period> -50`

### 3. Enrich with context
- Read `.ccs/task.md` → match commits to logged tasks by timestamp or description
- Glob `.ccs/branches/*.md` → check which commits belong to tracked branches

### 4. Output
Table: hash, message, author, when, matched task. Branch graph. Activity summary: commits this session, files touched, active branches, tracked vs untracked commits.

### 5. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: scope, commits shown, matched to tasks.

## Rules
- Use `--format` flags for structured data — don't parse verbose output
- Read `.ccs/task.md` once, match by scanning
- Read-only — does not modify history
- Does not fetch from remote → use `/ccs-sync` first for latest

## Refs
- Branch refs: `.ccs/branches/`
- Task log: `.ccs/task.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
