---
name: sync
description: "Pull, push, or rebase with conflict context and resolution guidance"
category: git
tags: [pull, push, rebase, conflict]
depends-on: [init]
input: "sync operation (pull, push, rebase)"
output: "synced repo + conflict resolution if needed"
token-estimate: 3000
parallel-safe: false
argument-hint: "[pull | push | rebase] [--force]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# Sync

Handle pull, push, and rebase with context-aware conflict resolution.

## Steps

### 1. Parse intent
- `pull` (default) / `push` / `rebase [target]`

### 2. Pre-sync assessment
- `git status` → check for uncommitted changes (warn if dirty)
- `git fetch` → get latest remote state
- `git rev-list --left-right --count HEAD...@{upstream}` → check divergence
- Read `.ccs/branches/<current>.md` if exists
- Report: ahead N, behind N

### 3. Execute

**Pull:** If clean → `git pull`. If dirty → ask to stash first (→ `/ccs-stash`). On conflicts → step 4.

**Push:** `git push`. If rejected → suggest pull first. If `--force` → confirm, then `git push --force-with-lease`.

**Rebase:** `git rebase <target>`. On conflicts → step 4. After success → regenerate branch ref (hashes changed).

### 4. Conflict resolution context
- `git diff --name-only --diff-filter=U` → conflicted files
- Read `.ccs/file-index.md` → importance of conflicted files
- Read `.ccs/branches/<branch>.md` → what this branch changed and why
- For each conflict: `git log --oneline -5 -- <file>` on both branches, file rank, which branch has more recent changes
- Present resolution recommendations: start with low-risk (B/C rank), manually review S/A rank
- Ask user how to proceed

### 5. Post-sync
- Update branch ref with new state if exists
- `git log --oneline -5` → show latest commits

### 6. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: action, branch, ahead/behind, conflicts, resolution.

## Rules
- Run `git fetch` once, not repeatedly
- Use `--name-only` to avoid full diff output
- Read branch ref for context — don't re-scan source files
- Only read conflicted files, not all changed files
- Force push requires explicit `--force` flag AND user confirmation

## Refs
- Branch refs: `.ccs/branches/`
- File index: `.ccs/file-index.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
