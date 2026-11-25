---
name: merge
description: "Merge branches with dependency checking and conflict context"
category: git
tags: [merge, conflict, resolution]
depends-on: [init, branch]
input: "source and target branches"
output: "merged code + conflict resolution + .ccs/merge-history.md entry"
token-estimate: 4000
parallel-safe: false
argument-hint: "[source-branch] [into target-branch]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-opus-4-6
context: fork
agent: general-purpose
---

# Merge

Merge branches with full dependency awareness. Predicts conflicts, provides context-rich resolution guidance.

## Steps

### 1. Identify branches
Parse `<source>` into `<target>` (default target: current branch). Find common ancestor: `git merge-base <source> <target>`.

### 2. Pre-merge analysis
- Read `.ccs/branches/<source>.md` and `.ccs/branches/<target>.md`
- `git diff --name-only <base>...<source>` and `<base>...<target>` → find overlapping files
- Read `.ccs/file-index.md` → rank overlapping files
- Read `.ccs/project-map.md` → check shared dependencies

### 3. Conflict prediction
- Preview conflicts via `git merge-tree` or `git diff` on overlapping files
- Classify risk: Low (no overlaps or D/C-rank), Medium (B-rank overlaps), High (S/A-rank overlaps or conflicting deps)
- Present overlap assessment table and strategy recommendation

### 4. Confirm with user
Ask: proceed, abort, or `--no-commit` for review.

### 5. Execute merge
- Run `git merge <source>` (or `--no-commit` if requested)
- If conflicts: list conflicted files (`git diff --name-only --diff-filter=U`), provide context from branch refs, suggest resolution by file rank and recency
- If clean: report success

### 6. Post-merge
- Update `.ccs/branches/<source>.md` → status: `merged`
- Append to `.ccs/merge-history.md`: date, strategy, commit hash, conflicts, files affected
- Update `.ccs/branches/<target>.md` if exists
- Clean up source branch ref if branch deleted

### 7. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: source → target, strategy, conflicts, risk level, files merged.

## Rules
- Read branch refs first — they contain change summaries
- Use `--name-only` for file lists, not full diffs
- Only read conflicted files, not all merged files
- After merge → suggest `/ccs-test` to verify
- Does not push → use `/ccs-sync push`

## Refs
- Branch refs: `.ccs/branches/`
- Merge history: `.ccs/merge-history.md`
- File index: `.ccs/file-index.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
