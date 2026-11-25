---
name: shared-tree
description: "Use when working in a repository whose working tree may hold someone else's uncommitted changes — another agent session, a teammate, the user's own in-progress edits. Records what was already modified, stages by explicit path (never `git add -A`), avoids tree-wide resets and stashes, and copies a file aside before rewriting it."
---

# Shared Tree

## The failure mode this fixes

Agents treat the working tree as theirs. `git add -A` sweeps a stranger's half-finished file into the commit. `git checkout .` or `git stash` to "get back to clean" erases an afternoon of someone else's edits. A one-line script rewrites a file and, on a bad day, truncates it first — and the section another session had added an hour ago is gone.

Uncommitted work exists in exactly one place. No reflog, no remote, no history holds it. With several agent sessions and a human all working in the same checkout, the tree is shared whether or not anyone said so — and the cost of forgetting is unrecoverable.

This skill makes "what here isn't mine?" the first question, and keeps every command scoped to the answer.

## When to Use This Skill

- `git status` shows modified or untracked files you didn't create this session
- More than one agent session, or an agent and a human, work in the same checkout
- You're about to commit, stash, reset, clean, or switch branches
- You're about to rewrite a whole file with a script or a full-file write
- A cleanup step would touch paths outside the change you were asked to make

**Don't use when:** the tree was clean when you started and every change in it is yours, or you're in a private worktree or fresh clone. If you can get one, do — an isolated worktree removes the problem instead of managing it.

## Instructions

### 1. Take stock before the first edit

Run `git status` at the start and write down what's already modified, staged, or untracked. That list is not yours. Anything that appears later that you didn't write is not yours either — another session may be working right now.

### 2. Stage by explicit path

`git add <the files you changed>`, never `git add -A`, `git add .`, or `git commit -a`. Read the staged diff before committing; every hunk should be one you can account for. If a file holds both your change and someone else's, stage only your hunks or leave the file and say so.

### 3. No tree-wide destructive commands

`git reset --hard`, `git checkout .`, `git restore .`, `git clean`, and `git stash` act on everything, including what isn't yours. Scope the command to the paths you own, or don't run it. Switching branches with foreign changes in the tree needs the owner's say-so, not a stash.

### 4. Copy aside before rewriting a file

Before editing a file that carries foreign changes, copy its current state somewhere outside the repo. Prefer a narrow in-place edit over regenerating the file. In a script: read into a variable, transform, check the result, then write — opening a file for writing before reading it truncates it, and a failure mid-transform leaves it empty.

### 5. Report what you left alone

Close with what you committed and what remains uncommitted exactly as you found it. The owner of those changes should be able to see at a glance that their work is intact.

## Output format

```
TREE AT START
  already modified (not mine): <paths>
  untracked (not mine):        <paths>

MY CHANGES
  - <path> — staged by path, committed in <sha>

LEFT UNTOUCHED
  - <path> — still uncommitted, as found

COPIED ASIDE
  - <path> → <backup location> (before editing a file with foreign changes)
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| `git add -A` / `commit -a` | Commits whatever is lying around under your message. Someone's draft is now in history, attributed to you. |
| Stash or reset to "get to clean" | Clean for you, gone for them. A dropped stash of foreign work is not recoverable in practice. |
| Whole-file regenerate | Rewriting a file from your in-memory version discards every edit made since you read it. |
| Write-before-read one-liners | The file is truncated before the read happens; any error leaves it empty. |
| "Tidying" unknown files | An untracked file you don't recognize is someone's work in progress until proven otherwise. Ask, don't delete. |

## Mental Model

> The working tree is a shared desk, not your desk. Touch what you put there, leave everything else exactly where it was, and say what you left.
