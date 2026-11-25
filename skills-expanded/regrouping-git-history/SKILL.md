---
name: regrouping-git-history
description: Rebuild a tangled feature branch into a small set of reviewer-friendly logical commits while preserving its final tree byte-for-byte. Use when asked to regroup, squash, tidy, or rewrite a branch with many interleaved feature, fixup, review, merge, or formatting commits. Resolve the actual PR base, plan groups with the user, reconstruct commits in an isolated temporary worktree, verify identical tree IDs, preserve named recovery refs, and require a second confirmation before an exact force-with-lease push.
---

# Regroup a branch safely

Announce that this skill is reorganizing history into logical commits. The invariant is strict: the rebuilt branch's final tree must have the same Git tree ID as the original branch. This workflow changes commit grouping only.

History rewriting and force-pushing are destructive operations. Follow every gate below. Never use `git reset --hard`, never rebuild directly in the user's worktree, and never delete the recovery ref automatically.

## Decide whether regrouping is justified

Use a lighter method when appropriate:

- Use autosquash for clean `fixup!` or `squash!` commits.
- Use a small interactive rebase for a handful of commits with one concern.
- Let squash-merge flatten history when the team does not need a narrative branch history.
- Stop if others are actively committing to the branch.

Use this workflow for a substantial branch with multiple tangled concerns where readable commits materially improve review or later bisection.

## Verify repository state and resolve the base

Inspect the exact repository, current branch, status, remotes, upstream, and PR before acting. Require a named local branch; stop on detached HEAD.

Do not infer the base from `@{upstream}`. That normally points to the remote feature branch. Resolve the PR base through the installed `github:github` skill or a bounded `gh pr view --json baseRefName,headRefName,isCrossRepository` query. If there is no PR, ask the user to name the intended base.

Fetch only the required remote refs. Set:

- `REGROUP_BRANCH`: verified current branch;
- `REGROUP_REMOTE`: verified remote that owns the feature branch;
- `REGROUP_BASE_REF`: verified remote base ref;
- `REGROUP_MERGE_BASE`: `git merge-base HEAD "$REGROUP_BASE_REF"`;
- `REGROUP_ORIGINAL_OID`: original `HEAD`;
- `REGROUP_ORIGINAL_TREE`: `git rev-parse "$REGROUP_ORIGINAL_OID^{tree}"`.

List the bounded range `REGROUP_MERGE_BASE..REGROUP_ORIGINAL_OID`. Confirm that every commit intended for rewriting is in the range.

Do not stash user changes. Require a clean tracked and untracked worktree before later synchronizing the local branch. If the worktree is dirty, stop and ask the user to commit, stash, or remove their own changes.

## Plan the narrative

Read commit patches and intent, not only subjects. Propose two to five groups such as toolchain, feature behavior, migration/refactor, documentation, or mechanical formatting. Put a pure mechanical formatting group last.

Build one exact path list per group and compare their union with:

```bash
git diff --name-only "$REGROUP_MERGE_BASE" "$REGROUP_ORIGINAL_OID"
```

Every changed path must be accounted for. Identify overlap paths whose history must be split across groups. For each overlap, inspect its bounded file history and choose an original commit representing the required intermediate state. If no commit cleanly represents it, plan a deliberate patch in the temporary worktree.

Show the user:

- base and merge-base;
- original commit range;
- proposed groups, messages, and path ownership;
- overlap paths and intermediate source commits;
- exact branch that would eventually be force-pushed.

Require explicit confirmation before creating commits. In Plan mode, `request_user_input` may collect it; otherwise return the plan as a final response and wait.

## Create named recovery refs

After confirmation, create a unique backup tag pointing at the original OID. Include a sanitized branch name and abbreviated original OID so concurrent or prior runs cannot collide. If the ref already exists, stop and investigate.

Keep the backup tag until CI passes and the user explicitly approves deleting it. Do not push it unless the user asks.

Create a separate temporary rebuilt-head ref under `refs/heads/regroup-build/`. This will keep reconstructed commits reachable after the temporary worktree is removed.

## Rebuild in an isolated temporary worktree

Create a task directory with `mktemp -d`, then add a worktree at a non-existent child path:

```bash
git worktree add --detach "$REGROUP_WORKTREE" "$REGROUP_MERGE_BASE"
```

All restore, staging, commit, and status commands must use `git -C "$REGROUP_WORKTREE"`. Never switch, reset, stage, or edit the user's current worktree.

For a group whose paths should take their final state, restore from the backup tag into both index and worktree:

```bash
git -C "$REGROUP_WORKTREE" restore \
  --source="$REGROUP_BACKUP_REF" \
  --staged \
  --worktree \
  --pathspec-from-file="$REGROUP_GROUP_FILE"
```

For an earlier state of an overlap path, use the verified intermediate commit as `--source`. In the later group, restore that path from the backup tag to reach its final state.

Path-list files must contain exact repository-relative paths, one per line. Reject paths containing newlines instead of passing them through line-based pathspec files. Do not use `$(cat ...)`, wildcard expansion, or unquoted path loops.

Commit each group with its agreed message. After every commit:

- inspect `git status --short` in the temporary worktree;
- confirm the intended diff and commit paths;
- stop on stranded renames, untracked files, hook modifications, or unexpected content.

Do not use `--no-verify` automatically. If a hook fails, diagnose whether it found a real defect or only a transient intermediate-state constraint, then stop and ask the user before bypassing it.

After the last group, the temporary worktree must be clean. Record `REGROUP_REBUILT_OID` from its `HEAD`, then protect it before removing or abandoning the worktree:

```bash
REGROUP_REBUILT_OID=$(git -C "$REGROUP_WORKTREE" rev-parse HEAD)
git update-ref "$REGROUP_REBUILT_REF" "$REGROUP_REBUILT_OID"
```

## Prove byte equivalence

Record:

```bash
git rev-parse "$REGROUP_BACKUP_REF^{tree}"
git rev-parse "$REGROUP_REBUILT_REF^{tree}"
git diff --exit-code "$REGROUP_BACKUP_REF" "$REGROUP_REBUILT_REF"
```

The tree IDs must be identical and the diff command must exit zero. Also inspect the rebuilt bounded log and commit-level diffs.

If any check fails, do not push and do not move the current branch. Stop with the original branch and backup tag untouched. Report the temporary worktree and rebuilt ref for inspection. Abandoning a failed temporary reconstruction is the rollback; a hard reset is never needed.

Do not modify `.git-blame-ignore-revs` in this workflow. That would change the final tree and violate the invariant. Offer it only as a separate, explicitly authorized follow-up change.

## Confirm and push with an exact lease

Fetch the exact remote feature branch immediately before pushing. Record its current object ID as `REGROUP_EXPECTED_REMOTE_OID`. If it differs from the remote OID observed during planning, stop because the branch changed.

Show the user:

- original and rebuilt commit narratives;
- matching original and rebuilt tree IDs;
- exact remote and branch;
- expected remote OID;
- exact force-with-lease command.

Require a second explicit confirmation before the push. Then push the rebuilt ref with an exact lease:

```bash
git push \
  --force-with-lease="refs/heads/$REGROUP_BRANCH:$REGROUP_EXPECTED_REMOTE_OID" \
  "$REGROUP_REMOTE" \
  "$REGROUP_REBUILT_OID:refs/heads/$REGROUP_BRANCH"
```

If the remote branch does not yet exist, do not invent a zero-OID lease. Explain that a normal new-branch push is sufficient and ask before changing the command.

The execution environment may require an escalated approval for the force-push. Request it through the execution tool with the exact target shown above.

## Synchronize local state without reset

After a successful push, re-verify that the user's worktree is clean and that its current tree still equals `REGROUP_ORIGINAL_TREE`. Move the checked-out branch ref with a compare-and-swap update:

```bash
git update-ref \
  "refs/heads/$REGROUP_BRANCH" \
  "$REGROUP_REBUILT_OID" \
  "$REGROUP_ORIGINAL_OID"
```

This must fail rather than overwrite the branch if its OID changed. Because the original and rebuilt tree IDs are equal, index and worktree should remain clean. Verify `HEAD`, status, and upstream afterward.

Remove only the exact registered temporary worktree with `git worktree remove` after it is clean and its rebuilt commits are protected by the rebuilt ref. Remove the known-empty parent directory with `rmdir`. Do not recursively delete an unresolved worktree.

## Retain recovery until CI passes

Monitor the relevant CI checks if requested. Keep both the original backup tag and rebuilt-head ref while validation is pending or failing.

After CI is green, report the recovery refs and ask whether the user wants them deleted. Delete only those exact refs after explicit confirmation. Never run broad ref cleanup.

## Hard rules

- Never use `git reset --hard`.
- Never stash, discard, or overwrite user changes.
- Never rebuild in the user's current worktree.
- Never force-push without matching tree IDs, a fresh exact lease, and explicit confirmation.
- Never delete the only named recovery point automatically.
- Never change repository contents as part of a history-only regrouping.
