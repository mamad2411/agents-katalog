---
name: resolve-merge-rebase-conflict
description: Resolves non-trivial merge, rebase, and cherry-pick conflicts by reading both sides' intent and combining hunks — handling rename/delete/add-add/binary conflicts, enabling rerere for repeats, and verifying the result builds and tests green rather than just clearing markers.
when_to_use: A merge/rebase/cherry-pick halts on conflicts (large or semantic), or the same conflict keeps recurring. Not clean commits/PRs (git-commit-pr), intentional history editing (rewrite-git-history), or recovering lost work (recover-git-state).
---

## When to Use

- "`git merge`/`git rebase`/`git cherry-pick` stopped with conflicts and I need to finish it correctly."
- "Big conflict across many files after a long-lived branch — which side wins where?"
- "The same conflict keeps coming back every rebase."
- "`<<<<<<<`/`=======`/`>>>>>>>` markers everywhere and the two sides changed the *same* logic differently."
- "rename/rename, modify/delete, add/add, or a binary asset conflicted and `--ours`/`--theirs` isn't obvious."

NOT this skill:
- Writing the commit message / opening the PR once the tree is clean → git-commit-pr
- Deliberately reshaping history (squash, reorder, split, drop commits) when there's no conflict to resolve → rewrite-git-history
- A rebase/merge that ate your work, detached HEAD, or you need a commit back via reflog → recover-git-state

## Steps

1. **Identify the operation first — `ours`/`theirs` MEANING FLIPS.** The same flag points opposite directions depending on what's running. Check `git status` (it names the op) before touching anything:

   | Operation | `HEAD` / `--ours` is | `MERGE_HEAD` / `--theirs` is | Mental model |
   |---|---|---|---|
   | `git merge X` | your current branch | the branch X you're merging in | ours = where you are |
   | `git rebase X` | **X (upstream)** — replayed onto | **your commit** being reapplied | **inverted**: "ours" is the base you're moving onto, "theirs" is your own change |
   | `git cherry-pick C` | your current branch | commit C being applied | like merge |
   | `git revert C` | your current branch | the inverse of C | like merge |

   In a rebase, blindly taking `--ours` throws away *your own* work. Never run `checkout --ours/--theirs` on autopilot during a rebase.

2. **Turn on zdiff3 so you can see the base.** Default `merge` style hides the common ancestor, so you can't tell which side actually changed what:

   ```sh
   git config --global merge.conflictStyle zdiff3   # adds a ||||||| base section between the two sides
   git config --global rerere.enabled true          # record+replay resolutions (step 7)
   ```

   With zdiff3 a hunk shows `<<<<<<< ours` / `||||||| base` / `======= theirs` / `>>>>>>>`. Compare each side *against base*: the side that differs from base is the one that changed; if both differ, you must merge them by hand.

3. **Survey the whole conflict before editing one file.** `git status` lists unmerged paths; `git diff --diff-filter=U` shows only conflicted hunks. Classify each path: content conflict, or a *tree* conflict (rename/delete/add). Resolve content hunks by **intent**, not by picking a side:
   - If both sides differ from base, you almost always want **both changes combined**, not one discarded. Read what each side was trying to do, write the union that satisfies both, delete all markers.
   - Only take one side wholesale when the other is genuinely superseded (e.g. theirs deleted a function ours merely reformatted).
   - For a single file you've decided entirely belongs to one side: `git checkout --ours -- <path>` / `--theirs -- <path>` (remember the rebase flip), then `git add <path>`.

4. **Handle tree conflicts deliberately — markers won't appear:**
   - **modify/delete** (`deleted by us`/`deleted by them`): git can't merge a hunk into a missing file. Decide: keep the file and reapply the other side's change (`git add <path>`), or honor the delete (`git rm <path>`). Default: keep it if the surviving side still calls into it.
   - **rename/rename** (same file renamed to two names, or both edited one rename): git leaves multiple paths. Pick the intended final name, move the merged content there, `git rm` the stray path, `git add` the keeper.
   - **add/add** (both branches created the same path with different content): treat exactly like a content conflict — merge the two versions into one file, `git add`.
   - **binary / generated** (images, lockfiles, compiled assets): no line merge possible. Choose a side on purpose — `git checkout --theirs -- yarn.lock && git add yarn.lock` — then **regenerate** rather than trust either copy (e.g. re-run `yarn install` / `npm install` and commit the result, never hand-stitch a lockfile).

5. **Continue, don't re-stage by hand at the end.** After every conflicted path is `git add`-ed (or `git rm`-ed):
   - merge → `git commit` (uses the prepared merge message)
   - rebase → `git rebase --continue`
   - cherry-pick → `git cherry-pick --continue`
   Repeat per replayed commit — a rebase can stop again on the next commit; resolve each in turn.

6. **Know the three exits.** Don't thrash a bad resolution — bail and retry with a cleaner head:

   | Command | Effect | Use when |
   |---|---|---|
   | `--continue` | accept current resolution, proceed | you resolved correctly |
   | `--abort` | restore the pre-operation state exactly | resolution is going sideways; start over |
   | `--skip` | drop the current commit being applied (rebase/cherry-pick only) | this commit is already upstream / empty after resolution — **never** to dodge a hard conflict |

   `git merge --abort` / `git rebase --abort` / `git cherry-pick --abort` always returns you to safety. Prefer abort + a fresh attempt over forcing a tangled hunk.

7. **Let rerere kill the repeats.** With `rerere.enabled true` (step 2), git records each manual resolution and **auto-replays** it the next time the identical conflict appears — invaluable when rebasing a long branch onto a moving main, or re-running a merge. Inspect with `git rerere status`/`git rerere diff`; if rerere replayed a *wrong* prior resolution, `git rerere forget <path>` and redo it.

8. **Build and test BEFORE declaring done — clearing markers is not resolving.** A tree with zero markers can still compile to wrong behavior: you may have dropped one side's logic, or combined two valid hunks into a contradiction. Run the project's real build + test (`npm test`, `cargo build && cargo test`, `pytest`, `make`) on the resolved tree. Fix failures at the merge seams, not by weakening assertions. Only then commit/continue.

9. **Reduce future conflicts (avoidance > resolution).** Keep PRs small and short-lived; `git fetch && git rebase origin/main` (or merge main in) frequently so you resolve a little, often, against fresh base instead of a giant divergence later; agree on formatting (run the formatter on both sides) so whitespace/reflow doesn't manufacture conflicts.

## Common Errors

- **`checkout --ours`/`--theirs` during a rebase, expecting merge semantics.** The labels are inverted — `--ours` is upstream, `--theirs` is your own commit. Result: you silently delete your own changes. Confirm the op via `git status` first; in rebase, *theirs* is usually what you want to keep.
- **Committing with conflict markers still in the file.** `<<<<<<<`/`=======`/`>>>>>>>` left behind ship as literal source and break the build. Grep the whole tree before committing (see Verify) — don't trust your eyes per-file.
- **Default `merge` conflictStyle, guessing which side changed.** Without the `|||||||` base you can't see the common ancestor and pick wrong. Set `merge.conflictStyle=zdiff3` once, globally.
- **Blindly taking one side to "make it go away."** `checkout --theirs` on a content conflict where both sides added needed logic drops half the work with a clean exit code. Conflicts where both differ from base almost always want the *union*.
- **Treating modify/delete as nothing to do.** No markers appear, so it looks resolved — but you must explicitly `git add` (keep) or `git rm` (delete). Leaving it unstaged stalls `--continue`.
- **Hand-merging a lockfile or binary.** `package-lock.json`/`yarn.lock`/`Cargo.lock` and images can't be line-merged sanely. Pick a side, then regenerate (`npm install`) or re-export — a stitched lockfile installs a phantom dependency graph.
- **`git rebase --skip` to escape a hard conflict.** Skip *drops the entire commit*, silently losing that change. Only skip a commit already present upstream or empty after resolution; otherwise resolve it.
- **Declaring done at zero markers without building.** A syntactically clean merge can be semantically broken (dropped branch, double-applied change). Always run build + tests on the resolved tree.
- **rerere replaying a stale wrong resolution.** Once enabled it auto-applies your *previous* answer even if that answer was the bug. If an auto-resolved hunk looks off, `git rerere forget <path>` and redo.
- **Resolving one conflict in a multi-commit rebase and assuming you're done.** Rebase stops per commit; `--continue` may immediately halt on the next. Loop until `git status` reports no rebase in progress.

## Verify

1. **No markers anywhere:** `git grep -nE '^(<{7}|={7}|>{7}|\|{7})' -- ':!*.md'` returns nothing (also catches the zdiff3 `|||||||` base line). Empty output is mandatory.
2. **No unmerged paths:** `git status --porcelain` shows no `UU`/`AA`/`DU`/`UD`/`DD`/`AU`/`UA` entries; `git diff --diff-filter=U` is empty.
3. **Operation actually finished:** `git status` reports no merge/rebase/cherry-pick in progress (no `.git/MERGE_HEAD`, `.git/rebase-merge`, or `CHERRY_PICK_HEAD`).
4. **Build + tests green on the resolved tree** — the project's real commands (`npm test` / `cargo test` / `pytest` / `make`), not a marker check standing in for verification.
5. **Both sides' intended changes are present:** diff the result against each parent and confirm neither side's needed logic was dropped. For a finished merge: `git diff HEAD^1 HEAD` (your side) and `git diff HEAD^2 HEAD` (the merged-in side). For a rebase, `git range-diff @{upstream}...HEAD` shows your commits survived intact.
6. **rerere recorded reusable resolutions** (if conflicts may recur): `git rerere status` is clean and future identical conflicts auto-resolve.

Done = zero conflict markers, no unmerged paths, the operation is complete, build + tests pass on the resolved tree, and a diff against both parents confirms each side's intended change is present.
