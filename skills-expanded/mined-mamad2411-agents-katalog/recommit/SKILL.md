---
name: recommit
description: Reshape the commits a branch carries on top of its target branch into a clean, logical sequence without changing the final committed tree, then stop before any push. Use when a branch needs presentable history before review or merge, when iterative work left fixups, WIP commits, or interleaved refactors, when another skill needs clean commits, or when the user says "recommit" or asks to tidy the git history.
---

# Recommit

Rewrite the commits after a branch's merge base into a sequence where each commit tells
one story and stands on its own. Preserve the final committed tree and leave the updated
branch local. This skill reshapes history; it does not edit code.

Do not use this skill to change behavior, to rewrite commits that the target branch
already contains, or on a branch that other people build on without coordination.

## Contract

- Start and end with a clean Git-visible working tree.
- Rewrite only commits after the confirmed merge base.
- Preserve the exact committed tree from the original branch tip.
- Show the proposed sequence and the recovery point before the rewrite.
- Stop before every push.

## Workflow

### 0. Pin the safe range

Require a named branch and a clean Git-visible working tree:

```bash
git branch --show-current
git status --porcelain=v1 --untracked-files=all
```

Stop when the branch name is empty or the status output is not empty. A clean start makes
the recorded branch tip a complete recovery point. When the tree is dirty because review
fixes are still uncommitted, tell the user that `git commit --fixup=<sha>`, or `git absorb`
when it is installed, turns them into `fixup!` commits that this skill folds.

Determine the target from PR or MR tracker metadata when it is available, and refresh its
remote-tracking ref when a remote exists. Without tracker metadata, use `origin/HEAD`.
Ask the user only when these sources are absent or disagree.

Validate the target and record these values:

```bash
git rev-parse --verify <TARGET_REF>^{commit}
git rev-parse HEAD
git rev-parse HEAD^{tree}
git merge-base <TARGET_REF> HEAD
```

Call the target ref `TARGET_REF` and the outputs `ORIG`, `ORIG_TREE`, and `MERGE_BASE`;
use the recorded literal values in later commands so they survive separate tool calls.
Inspect the range shape (step 1 reads the full diff):

```bash
git log <MERGE_BASE>..<ORIG> --oneline
git diff <MERGE_BASE>..<ORIG> --stat
```

The step is complete when the target is known, the range is non-empty, the starting
state is clean, and all four recorded values are available.

### 1. Design the commit sequence

Read the complete diff of `MERGE_BASE..<ORIG>` and the existing commits. Then write the
proposed commits in order. For each commit, state its title, its owned files or hunks, and
the checks that validate it.

- Give each commit one coherent purpose, independently buildable and testable.
- Put behavior-preserving preparation before the behavior that uses it. A refactor that
  makes the change easy lands first.
- Give a standalone improvement its own commit. A bug fix or UX fix that justifies itself
  without the feature is easier to review and revert alone.
- Keep infrastructure with its first user. A commit that adds a mechanism nothing calls
  yet is dead code on arrival.
- Put a dependency before the commit that uses it.
- Keep generated files (lockfiles, translations, snapshots) with the change that requires
  them.
- Combine changes when a split would make either commit invalid. Artificial atomization
  is as bad as a grab bag.

The step is complete when every changed path and hunk belongs to exactly one proposed commit
and every proposed commit has a validation command or an explicit reason that none exists.

### 2. Show the plan

Show the confirmed target, `MERGE_BASE..<ORIG>`, the complete proposed sequence, and the
recovery command `git reset --hard <ORIG>`. The rewrite changes only local history and
that one command reverts it, so continue without waiting; the push in step 5 is the
action that needs permission.

### 3. Rebuild the history

Read [REBUILD.md](REBUILD.md) and use the method that matches the planned sequence. The
step is complete when the local history matches the planned sequence and all final changes
are committed.

### 4. Verify the result

Check the state invariants from the Contract:

```bash
test "<ORIG_TREE>" = "$(git rev-parse HEAD^{tree})"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

Then use the temporary-worktree procedure in [REBUILD.md](REBUILD.md) to run the planned
checks on every commit in `MERGE_BASE..HEAD`. Remaining changes from later commits must not
be visible during an earlier commit's checks.

If an invariant or check fails, restore the clean starting point with
`git reset --hard <ORIG>`, confirm that status is clean, and report the failed check.
Recovery restores the recorded starting point, so it needs no separate permission.

The step is complete only when both invariants and every planned per-commit check pass.

### 5. Stop

Show `git log <MERGE_BASE>..HEAD --reverse --oneline`, the saved `ORIG`, and the checks that
passed. State that the branch is local and that updating its PR or MR requires
`git push --force-with-lease`. Ask for explicit final permission immediately before that
push. Do not push as part of this skill.

## Worked example

A "Language setting" PR had two commits: a `_create_combo` refactor, then one grab-bag
`feat` commit that bundled a generic dialog auto-sizing improvement, a `note` caption
mechanism, and the language feature with 20 generated translation files. The planned
sequence:

1. `refactor(settings): extract _create_combo` holds the behavior-preserving preparation.
2. `feat(settings): fit the dialog height to the active tab` holds the standalone UX fix,
   split out with cumulative hunk staging.
3. `feat: add a Language setting` holds the feature, the `note` mechanism (nothing used it
   until here), and the generated translations.

The final tree matched `ORIG_TREE`, every commit passed lint and type checks in the
temporary worktree, and the branch stayed local with the force-push left to the user.
