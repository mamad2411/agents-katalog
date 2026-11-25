---
name: stash
description: "Stash and restore WIP with tracked context"
category: git
tags: [stash, wip, restore]
depends-on: [init]
input: "stash operation (save, list, pop, apply)"
output: "stashed/restored state + context tracking"
token-estimate: 1500
parallel-safe: true
argument-hint: "[save \"message\"] | [pop [index]] | [list] | [drop index]"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, AskUserQuestion, Task, EnterPlanMode
model: claude-haiku-4-5-20251001
context: fork
agent: general-purpose
---

# Stash

Stash and restore work-in-progress while tracking what was being worked on in `.ccs/branches/` and `.ccs/task.md`.

## Steps

### 1. Parse intent
- `save "<message>"` → stash with message (default if no args: auto-generated message)
- `pop [index]` → restore stash
- `list` → show stashes with context
- `drop <index>` → remove stash

### 2. Execute

**Save:**
1. `git status --short` → capture current state
2. `git diff --stat` → what's changed
3. `git stash push -m "<message>"`
4. Update `.ccs/branches/<current>.md` if exists — add stash note

**Pop:**
1. `git stash list` → available stashes
2. Read `.ccs/task.md` → find matching stash save entry for context
3. `git stash pop <index>`
4. `git status --short` → show restored state
5. Display what was being worked on (from task.md)

**List:**
1. `git stash list --format="%gd|%gs|%cr"`
2. Cross-reference with `.ccs/task.md` stash entries
3. Display enriched list with context

**Drop:**
1. `git stash drop <index>`

### 3. Log to `.ccs/task.md`
Append using template at `.claude/skills/_ccs/templates/task-template.md`: action, branch, message, files stashed, stash index.

## Rules
- Use `git status --short` (faster than verbose)
- Read `.ccs/task.md` once for context matching
- Keep stash context under 20 lines
- Conflicts from stash pop must be resolved manually

## Refs
- Branch refs: `.ccs/branches/`
- Task log: `.ccs/task.md`
- Task template: `.claude/skills/_ccs/templates/task-template.md`

---
*codebase-context-skill v2.0.0*
