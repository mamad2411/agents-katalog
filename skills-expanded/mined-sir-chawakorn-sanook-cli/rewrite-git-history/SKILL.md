---
name: rewrite-git-history
description: Rewrites git history safely — interactive rebase (squash/split/reorder/reword/edit), amend, and git filter-repo/BFG to purge a committed secret or large file — using force-with-lease and explicit shared-branch safeguards.
when_to_use: Cleaning up a feature branch before merge, purging a committed secret or large blob from all history, or splitting/squashing commits. Distinct from git-commit-pr (normal commit/PR), resolve-merge-rebase-conflict (fixing conflicts), and recover-git-state (recovering lost commits).
---

## When to Use

Reach for this skill when you must **change commits that already exist**, not create new ones:

- "Squash these 6 WIP commits into one before merging"
- "Reword that commit message / fix the author/email on old commits"
- "Split this giant commit into logical pieces"
- "Reorder / drop a commit from my branch"
- "I committed an API key / `.env` / a 400 MB binary — scrub it from the whole history"
- "Amend the last commit, I forgot a file"

NOT this skill:
- Writing a normal commit message or opening a PR on un-rewritten work → git-commit-pr
- A rebase/merge that stopped on `CONFLICT` markers → resolve-merge-rebase-conflict
- Lost a commit/branch after a bad rebase/reset, need it back → recover-git-state
- Moving plaintext secrets into a vault, rotating, or scanning for leaks → secrets-management (run *after* the purge here)

## Steps

1. **Apply the golden rule first — is this branch shared?** Rewriting changes every downstream SHA; anyone who pulled the old history gets a divergent tree and can re-push the secret you deleted.

   | Branch state | Rewrite? | How to push |
   |---|---|---|
   | Local-only, never pushed | Yes, freely | normal `git push` (first push) |
   | Pushed, **only you** pull it (personal feature branch) | Yes | `git push --force-with-lease` |
   | Shared / `main` / release / others have pulled | **No — coordinate first** | announce → everyone stops → rewrite → `--force-with-lease` → everyone re-clones or `git reset --hard origin/<branch>` |

   Default: rewrite only local/unshared branches. For `main`, the answer is almost always "don't" — the only exception is purging a secret, and then only with team sign-off.

2. **Record the safety net before touching anything.** Copy the current tip so you can undo: `git rev-parse HEAD`, and confirm `git status` is clean — stash or commit dirty work first; rebase refuses to start otherwise. The reflog (`git reflog`) keeps the old tip ~90 days regardless, but a written-down SHA is faster.

3. **Interactive rebase for squash/reword/reorder/drop/edit.** Rebase the commits *since* the base, not your whole history:

   ```bash
   git rebase -i origin/main      # or: git rebase -i HEAD~5
   ```
   In the todo editor, set the verb on each line (top = oldest), and **reorder by moving whole lines**:

   | Verb | Effect |
   |---|---|
   | `pick` | keep as-is |
   | `reword` | keep changes, edit the message |
   | `edit` | stop here to amend content or split (step 4) |
   | `squash` | fold into the commit above, **combine both messages** |
   | `fixup` | fold into the commit above, **discard this message** (use for "oops typo" commits) |
   | `drop` | delete the commit entirely (or just delete the line) |

   Save and close. Resolve any conflicts (→ resolve-merge-rebase-conflict), then `git rebase --continue`. Abort cleanly at any point with `git rebase --abort` — it restores the pre-rebase tip exactly.

4. **Split one commit into several.** Mark it `edit` in the rebase todo; when rebase stops on it:
   ```bash
   git reset HEAD^          # un-commit, keep changes in working tree (mixed reset)
   git add -p               # stage hunk-by-hunk for the first piece
   git commit -m "first logical change"
   git add -p && git commit -m "second logical change"   # repeat until clean
   git rebase --continue
   ```
   `git reset HEAD^` (mixed) keeps your work in the tree; never `--hard` here or you lose it.

5. **Amend only the last commit** (no rebase needed): `git commit --amend` (edit message + fold staged changes), or `git commit --amend --no-edit` to silently add forgotten files. If already pushed to your own branch, follow with `git push --force-with-lease`.

6. **Purge a file/secret across ALL history — `git filter-repo` (preferred, BFG fallback).** `git filter-branch` is deprecated and slow; do not use it.
   ```bash
   pip install git-filter-repo        # or: brew install git-filter-repo
   # Remove a path everywhere (history rewritten in place):
   git filter-repo --path config/secrets.yml --invert-paths
   # Or redact a literal string/regex from every blob:
   printf 'AKIAIOSFODNN7EXAMPLE==>REDACTED\n' > replacements.txt
   git filter-repo --replace-text replacements.txt
   ```
   BFG alternative for big blobs: `bfg --delete-files '*.zip'` or `bfg --replace-text replacements.txt`, then `git reflog expire --expire=now --all && git gc --prune=now --aggressive`. `filter-repo` runs that cleanup for you and removes the `origin` remote on purpose — re-add it before pushing.

7. **ROTATE the leaked secret — rewriting history does NOT un-leak it.** Anyone who cloned, any fork, any CI cache, and GitHub's own unreachable-commit cache still hold it. The history scrub is step 1 of 2; the real fix is: **revoke + reissue the key/token/password at the provider** (then → secrets-management). Treat the credential as compromised the moment it was pushed.

8. **Force-push with `--force-with-lease`, never bare `--force`.**
   ```bash
   git push --force-with-lease origin <branch>
   ```
   `--force-with-lease` refuses the push if the remote moved since your last fetch — it catches the case where a teammate pushed in the meantime, which bare `--force` would silently obliterate. For a full-history purge you must push every ref: `git push --force-with-lease --all && git push --force-with-lease --tags`.

## Common Errors

- **Force-pushing a shared/`main` branch without coordination.** Everyone else's next pull diverges, and someone re-pushes the deleted secret. Confirm the branch is unshared (step 1) or get explicit sign-off first.
- **Using bare `git push --force`.** Overwrites whatever is on the remote with zero safety check, including a teammate's just-pushed commits. Always `--force-with-lease`.
- **Thinking the rewrite removed the secret.** It only removed it from *your* refs. Forks, clones, CI caches, and GitHub's cached unreachable commits still expose it — rotate the credential (step 7). This is the single most common and most damaging mistake.
- **`git reset --hard HEAD^` when splitting a commit.** Discards the very changes you were trying to re-commit. Use `git reset HEAD^` (mixed) to keep them in the working tree.
- **Rebasing onto the wrong base** (`HEAD~10` swallows commits already on `main`). Rebase against the tracking base, e.g. `git rebase -i origin/main`, so you only touch your own commits.
- **Reordering by editing SHAs or text instead of moving whole lines.** The rebase todo is line-ordered; cut/paste entire lines to reorder. Editing a hash breaks the rebase.
- **`squash` when you meant `fixup`** (or vice versa). `squash` opens an editor to combine both messages; `fixup` drops the second message. Picking wrong leaves "WIP"/"typo" text in your final message.
- **Running `git filter-repo` on a dirty or non-fresh clone.** It refuses non-fresh clones by default for safety; work on a fresh `git clone` (or pass `--force` only when you understand why), and commit/stash everything first.
- **Forgetting `filter-repo` dropped the remote.** It removes `origin` deliberately so you can't push to the wrong place by reflex. Re-add it (`git remote add origin <url>`) before the force-push.
- **Letting purged objects linger.** After a manual `filter-branch`/BFG run, the blobs survive in reflog/packs until `git reflog expire --expire=now --all && git gc --prune=now`. Without it, `git cat-file` still serves the secret locally.

## Verify

1. **Target commits are correct.** `git log --oneline` (and `--stat`/`-p`) shows exactly the intended squash/split/reword/reorder — commit count and each message match the plan.
2. **No unintended commits dropped.** Diff the rewritten branch against the saved pre-rewrite SHA from step 2: `git range-diff <old-sha> HEAD` (or `git diff <old-sha> HEAD` to confirm the *tree* is identical when you only re-shaped messages/structure, not content). Cross-check `git reflog` for the old tip.
3. **Secret is gone from every ref, not just `HEAD`.** `git log --all -p -S 'AKIA'` returns nothing, and `git grep -I 'AKIA' $(git rev-list --all)` finds no hits across all history. For a removed path: `git log --all --oneline -- config/secrets.yml` is empty.
4. **No dangling reachable copy.** After cleanup, `git rev-list --objects --all | grep <blob-sha>` is empty and `git count-objects -v` shows the pack shrank.
5. **Credential actually rotated.** The old key returns 401/403 from the provider (not just deleted from git). If it still authenticates, you are not done.
6. **Remote matches and was pushed safely.** `git push --force-with-lease` succeeded (not refused), and `git log origin/<branch> --oneline` equals local. Teammates on a shared branch confirmed re-sync.

Done = intended commits are exactly reshaped with zero unintended drops (verified against the pre-rewrite SHA/reflog), the secret is absent from every ref and every history blob, the leaked credential is rotated and dead at the provider, and the push used `--force-with-lease` on a branch that was either unshared or coordinated.
