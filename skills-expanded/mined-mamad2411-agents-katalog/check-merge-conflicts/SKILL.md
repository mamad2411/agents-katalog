---
name: check-merge-conflicts
description: Predict merge conflicts before a real merge — dry-run branch diffs without touching the working tree
argument-hint: "[source-branch] [target-branch]"
related:
  - merge
  - report

---

## Goal

Check whether a merge would produce conflicts before actually merging — uses merge-tree/patch dry-runs to compare branches without touching the working tree

## Scope

- Use before merging a branch (`git merge`) or before creating/updating a PR
- Covers: textual conflicts (same line edited on both sides), semantic conflicts (rename/delete crosses), diverged branches
- Read-only against the working tree — never performs a real merge

## Execute

### 1. Prepare Comparison

> Goal: identify the branches and merge base

1. Take source and target from the arguments — default: current branch vs `main`
2. Run `git fetch` for latest refs, then find the merge base: `git merge-base <source> <target>`
3. Check that the branches actually diverge — if a fast-forward is possible = definitely no conflicts

### 2. Dry-Run Merge

> Goal: predict conflicts without touching the working tree

1. `git merge-tree --write-tree <target> <source>` (git ≥2.38) — shows conflicts without merging
2. Fallback: `git merge --no-commit --no-ff` in a temp worktree (`/use-git-worktrees`) then abort
3. Collect the list of conflicting files with hunk details

### 3. Analyze Conflict Surface

> Goal: understand the scale and nature of the conflicts

1. Group them: trivial (imports, formatting), moderate (logic overlaps), severe (same function edited in different directions)
2. Flag semantic risks where the merge goes green but breaks: a file renamed on one side + edited on the other, a deleted file that was modified
3. Estimate resolution effort: auto-mergeable conflicts vs needing human judgment

### 4. Report

> Goal: summarize conflict risk with a plan

1. Use `/report`: `No.`, `File`, `Conflict Type`, `Severity`, `Auto-resolvable`, `Notes`
2. Verdict: `clean`, `trivial conflicts`, `needs manual resolution`, `high risk`
3. Recommend: merge now, rebase first, or split into smaller merges

## Rules

### 1. No Working Tree Changes

- Dry-run only — use `merge-tree` or a temp worktree; never merge in the real working tree
- Clean up the temp worktree afterwards

### 2. Evidence-Based

- Report only conflicts proven by the dry-run — don't guess from diff size
- Clearly separate textual conflicts from semantic risks

### 3. Actionable

- The verdict must include a next step — safe to merge now / what to do first
- For auto-resolvable conflicts, state how (theirs/ours/format-fix)

## Expected Outcome

- A list of files that will conflict, with severity, before the real merge
- Verdict + recommended merge strategy
- Fewer surprise conflicts during the merge
