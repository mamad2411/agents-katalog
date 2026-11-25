---
name: rebase-on-main
description: Rebase current branch on main with conflict resolution, build verification, and optional merge/fast-forward/squash. Use when the user wants to merge to main, update a branch from main, ship a feature, or get ready for a PR.
---

# Rebase on Main

Execute every step in order. Stop and report on unexpected failure.

Scripts: `$HOME/.claude/skills/rebase-on-main/scripts`

## Phase 1: Detect & rebase

Check current branch and working-tree state first:

- **On `main` + clean** → "Nothing to do — on main with no changes." Stop.
- **On `main` + dirty** → Branch-from-main sub-flow (below). Skip to Phase 2 after.
- **On a feature branch** → run the rebase script and handle status as listed.

Run: `pwsh -NoProfile -File "$HOME/.claude/skills/rebase-on-main/scripts/git-rebase-onto.ps1"`

Handle `status`:
- **error** → report `reason`, stop.
- **fetch-failed** → report `fetchOutput`, stop (never rebase onto a stale base).
- **dirty** → list files, ask via `AskUserQuestion`: **Retry** / **Cancel**.
- **up-to-date** → skip to Phase 2.
- **success** → Phase 2.
- **conflicts** → resolve (see below).

Inside a worktree the script rebases in place (`isWorktree: true`, `mainRepoRoot` set); `rebaseTarget` is `origin/main` when local `main` is checked out elsewhere and can't be moved. Merge actions then run from `mainRepoRoot` (see Merge prompt).

### Branch-from-main sub-flow

Goal: get the dirty changes onto a feature branch on top of latest main, then proceed to Phase 2.

1. Show changed files. Suggest a branch name (apply `/commit`'s tag-selection on the diff; prefix `feature/<kebab-tag>`). Ask via `AskUserQuestion` for the branch name with the suggestion as the Recommended option.
2. Run `pwsh -NoProfile -File "$HOME/.claude/skills/rebase-on-main/scripts/git-branch-from-main.ps1" -BranchName <name>`. Handle `status`:
   - **ready** → step 3.
   - **pop-conflicts** → resolve as in Phase 1 source conflicts, stage, then continue.
   - error → report `reason`, stop.
3. Invoke `/commit` to commit the changes on the new branch (bracket-tag format).
4. Skip to Phase 2 — branch is one commit ahead of latest main, ready to merge.

### Conflict Resolution

Main is the foundation — start from main's version, apply feature's intent on top.

**Generated files** (compiled CSS, bundled JS, lockfiles): `git checkout --theirs <file>`, stage, move on. Build will regenerate.

For source conflicts: read both sides, resolve favoring main's structure + feature's changes, stage, `git rebase --continue`. Repeat for subsequent commits. Bail after 3 failed attempts on one commit (`git rebase --skip`). Full bail if unrecoverable (`git rebase --abort`).

### Track critical events

Note whether any of these occur during Phase 1 — they drive Phase 2's presentation:

- Source conflicts required manual resolution (user should verify semantics).
- Generated files resolved with `--theirs` (build must regenerate correctly).
- A commit was skipped (`git rebase --skip` used — work dropped).

## Phase 2: Build → Test → Merge Prompt

After Phase 1 succeeds (or branch was already up-to-date), always run `/build` before any prompt. Catches breakage from new main; gives the user a running server to test against. `/build` returns success for no-build repos (claude-config, docs-only, etc.) via its graceful-skip path.

### Build failure

One fix attempt. If still failing, prompt (numbered list — no clickable):

```text
Build failed after rebase. One fix attempt didn't recover.

(1) Fix again  (2) Abort  (3) Drop into manual
```

- **Fix again** → another fix attempt, loop back.
- **Abort** → `git reset --hard ORIG_HEAD`, report, stop.
- **Drop into manual** → leave repo as-is, print: "Branch is rebased but build is broken. Fix manually then re-invoke `/rebase-on-main`, or merge at your own risk." Stop.

### Test verdict

Run `/test` once, after `/build`, before the prompt; reuse the verdict.

A non-green verdict is a **critical event: it warns, it never blocks.** Render it in the prompt's critical-events area carrying `/test`'s classification and the failing test names, then let the user choose. Per `wf-git-workflow.md` this prompt is the last backstop before main in a repo without CI, so the warning has to be visible — but the user decides, not the skill.

If `/test` reports `baseline: none` its classification is degraded (no `TEST REGRESSION` / `NEEDS REVIEW` / `TEST DRIFT` split — every failure reads as `TEST FAILURE`). Say so in the warning rather than presenting the rows as authoritative. `/test` no-ops gracefully in repos with no test config.

### Audit branch — visibility check

Show the **Audit branch** option in the merge prompt only when:

- the rebase script's `commitsAhead` is **≥ 5** (after the branch-from-main sub-flow: 1, with `rebaseTarget` = `main`), OR
- `git diff --name-only <rebaseTarget>..HEAD` returns **≥ 20** files,

AND `git log -1 --format=%s <rebaseTarget>..HEAD` does NOT start with `[Refac]`, matched case-insensitively so pre-rename `[REFAC]` commits still count (user hasn't audited recently).

### Merge prompt (numbered list)

Plain numbered list. Critical-event warnings, if any, appear above the prompt as plain text.

```text
Rebase complete. Build passing.

[<critical events, one per line, if any>]

[(1) Audit branch  — if visible]
(N) Squash
(N+1) Fast-forward
(N+2) Merge
```

Numbering: when Audit is shown it's `(1)`; otherwise the list starts at Squash with `(1)`.

- **Audit branch** — invoke `/audit-branch`. After it returns, loop back to this prompt. If user applied fixes, the new tail commit is `[Refac]`-tagged → Audit hides on the next round.
- **Squash** — invoke `/squash`. Then `pwsh -NoProfile -File "$HOME/.claude/skills/rebase-on-main/scripts/git-merge-cleanup.ps1" -Branch <branch> -Mode ff`. If `/squash` cancelled, loop back.
- **Fast-forward** — `pwsh -NoProfile -File "$HOME/.claude/skills/rebase-on-main/scripts/git-merge-cleanup.ps1" -Branch <branch> -Mode ff` (no merge commit).
- **Merge** — `pwsh -NoProfile -File "$HOME/.claude/skills/rebase-on-main/scripts/git-merge-cleanup.ps1" -Branch <branch> -Mode merge` (PR-style `--no-ff`).

In a worktree, `ExitWorktree` (keep) first and run the cleanup script from `mainRepoRoot`: it checks out `main` there, merges, then removes the worktree before deleting the branch.

Freeform text: words like "cancel" / "exit" / "stop" / "leave" → report "Rebase complete, not merged. Branch left as-is." and stop. No revert; user can `git reset --hard ORIG_HEAD` if desired. Other freeform text → interpret intent or ask for clarification.

Loop until a terminal action.

## Summary

Report: branch name, commits rebased, conflict count, build status, merge mode used (if merged), worktree cleanup status.
