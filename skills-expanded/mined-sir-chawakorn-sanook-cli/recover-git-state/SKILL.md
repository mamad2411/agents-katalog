---
name: recover-git-state
description: Recovers lost or broken git state — restores dropped commits/branches/stashes via reflog and fsck, pins a regression with git bisect, and safely undoes a bad reset/rebase/merge with revert or reset --soft/--mixed/--hard — without destroying still-recoverable objects.
when_to_use: Work appears gone after a reset --hard, bad rebase, deleted branch, dropped stash, or detached HEAD, or you need to pin which commit introduced a bug. NOT intentional history editing (rewrite-git-history), conflict-marker resolution (resolve-merge-rebase-conflict), or diagnosing a non-git code failure (debug-root-cause).
---

## When to Use

Reach for this when work *appears* gone or HEAD landed somewhere wrong — the commits almost always still exist as unreachable objects:

- "I lost my commits" / "my branch is empty" after a `reset --hard`, bad `rebase`, or force-fetch
- "I deleted the wrong branch" (`git branch -D feature`)
- "I'm in detached HEAD and made commits — did I lose them?"
- "I `git stash drop`'d / `stash pop`'d into a conflict and lost a stash"
- "Which commit broke this?" — a regression to pin across a known-good..bad range
- A merge/rebase/`reset` made things worse and you want it back exactly as it was

NOT this skill:
- *Intentionally* rewriting history (squash, reword, rebase to clean up, strip a secret) → rewrite-git-history
- Resolving the conflict markers from an in-progress merge/rebase/cherry-pick → resolve-merge-rebase-conflict
- The code itself is failing (test/crash/wrong output) and git history is fine → debug-root-cause
- The file was never committed and isn't in any stash → git can't recover it; check editor local history / backups

## Steps

1. **STOP and snapshot before touching anything.** Recovery commands can themselves overwrite refs. Freeze current state so you can't make it worse:
   ```bash
   git stash list; git status; git log --oneline -5   # what do we actually have?
   git branch _backup_$(date +%s)                       # pin current HEAD as a named ref
   ```
   Never run `reset --hard`, `checkout`, `rebase`, or `gc` until you've located the SHA you want back.

2. **Find the lost SHA — reflog is the safety net.** Every move of HEAD (and of each branch) is logged for ~90 days, even after `reset --hard` or branch deletion:
   ```bash
   git reflog                       # every HEAD move: HEAD@{0}, HEAD@{1}, ...
   git reflog show feature          # moves of one branch ref specifically
   git reflog --date=relative | grep -iE 'commit|reset|rebase|checkout'
   ```
   The entry *just before* the bad operation is your target (e.g. `HEAD@{2}` = "before the reset"). Copy its SHA.

3. **Recover by creating a ref — never `checkout` a loose SHA bare.** Pick the action by what you lost:

   | Lost | Command | Note |
   |---|---|---|
   | A deleted branch | `git branch feature <sha>` | `<sha>` from `git reflog show feature` or `fsck` |
   | Commits after a `reset --hard` | `git reset --hard HEAD@{1}` | moves current branch back; **discards** anything since |
   | Commits, but keep current work | `git branch rescue <sha>` | safe — inspect/`cherry-pick` from `rescue`, then delete it |
   | Detached-HEAD commits | `git branch keep <sha>` *before* you `checkout` away | bare checkout-away orphans them |

   Default to `git branch rescue <sha>` — it's non-destructive. Use `reset --hard HEAD@{n}` only when you're sure everything after it is garbage.

4. **Recover a dropped/popped stash via fsck.** A dropped stash isn't in `reflog` but lives as an unreachable commit:
   ```bash
   git fsck --no-reflog --unreachable | grep commit | awk '{print $3}' \
     | xargs -I{} git log -1 --format='%H %ci %s' {} | grep -i 'WIP on'
   git stash apply <sha>            # or: git branch stash_recovered <sha>
   ```
   A stash commit's subject starts with `WIP on <branch>:`. `git fsck --lost-found` also drops them under `.git/lost-found/`.

5. **Undo by audience: published → `revert`, local → `reset`.** This is the one rule that prevents a second disaster:

   | Situation | Use | Why |
   |---|---|---|
   | Bad commit already pushed / shared | `git revert <sha>` | adds an inverse commit — no history rewrite, safe for collaborators |
   | Local mistake, want it gone | `git reset` (see below) | rewrites your local branch; never on shared history |

   `reset` mode, decided by where you want the changes to land:
   - `--soft HEAD~1` → undo the commit, keep changes **staged** (re-commit cleanly)
   - `--mixed HEAD~1` (default) → undo commit, keep changes in **working tree**, unstaged
   - `--hard HEAD~1` → undo commit **and discard** the changes — destructive; only after step 1's backup

6. **Restore working-tree files (not commits) with `git restore`.** Discarded edits or a wrong file version:
   ```bash
   git restore path/to/file              # revert working-tree file to HEAD (uncommitted edits gone)
   git restore --source=<sha> file       # pull one file's content from a specific commit
   git restore --staged path             # unstage only (keep working-tree edits)
   ```
   `git checkout -- file` is the old spelling; prefer `restore`.

7. **Pin a regression with `git bisect`.** Binary-search the first bad commit across a known-good..bad range:
   ```bash
   git bisect start
   git bisect bad                 # current HEAD is broken
   git bisect good v1.4.0         # last known-good tag/sha
   # git checks out the midpoint; test it, then mark good/bad and repeat
   git bisect good   # or: git bisect bad
   ```
   Automate it — let git drive every step with an exit-coded script:
   ```bash
   git bisect run ./test.sh       # script: exit 0 = good, 1..124 = bad, 125 = skip (untestable)
   ```
   When done it prints `<sha> is the first bad commit`. **Always** `git bisect reset` to return to your original HEAD.

8. **Run `git gc` only after you've recovered and verified.** Unreachable objects survive until garbage collection. Don't run `git gc --prune=now` or `git reflog expire` while a recovery is pending — that's what permanently deletes the SHAs you're hunting.

## Common Errors

- **`checkout`ing a loose SHA, making commits, then leaving — they're orphaned again.** Always `git branch <name> <sha>` *first*; commit onto a real ref.
- **`reset --hard HEAD@{1}` to "go back," wiping current uncommitted work.** `--hard` discards the working tree. Stash or `git branch _backup` first (step 1); use `git branch rescue` instead when unsure.
- **`reflog` is empty / "ambiguous argument".** You're in a fresh clone or a different repo — reflog is per-local-clone and not pushed. Use `git fsck --lost-found` to find unreachable commits by content instead.
- **`revert`ing a merge commit fails or reverts the wrong side.** Pass the parent: `git revert -m 1 <merge-sha>` (mainline = parent 1). Reverting a merge has its own re-merge gotcha; for shared history that's still safer than rewriting.
- **`stash pop` hit a conflict and you assumed the stash was lost.** A *conflicted* `pop` does **not** drop the stash — it's still in `git stash list`. Resolve, then `git stash drop`.
- **Ran `git gc` / `git reflog expire --expire=now --all` and now the SHA is gone.** Pruning deleted the unreachable objects. Recover the ref *before* any gc; check `.git/lost-found/` and cloned mirrors.
- **`bisect` mislabels because the build is broken at some midpoints.** Have the script `exit 125` (skip) for uncompilable commits so bisect routes around them instead of falsely marking bad.
- **Forgot `git bisect reset`.** You're left in detached HEAD on a midpoint commit, confusing later work. Reset returns you to the pre-bisect branch.
- **Using `reset` to undo *pushed* commits, then force-pushing.** Rewrites shared history and breaks teammates. On published commits use `git revert`; rewriting is rewrite-git-history's job, not a recovery.

## Verify

Recovery is complete and correct when:

1. **The recovered ref points at the right tree.** `git diff <known-good-sha> <recovered-ref>` is empty (or shows exactly the intended delta) — confirms you grabbed the right SHA, not a neighbor.
2. **The expected commits are reachable.** `git log --oneline <recovered-ref>` shows the commits that were "lost," and `git status` is clean (no surprise staged/modified files).
3. **A recovered stash applied cleanly.** `git stash show -p <sha>` matches the work you expected; after `apply` the files contain the WIP changes.
4. **An `undo` did what its audience requires.** After `revert`: a new inverse commit exists and `git log` history is intact (nothing rewritten). After `reset`: `git status` shows the changes in the intended state (staged for `--soft`, unstaged for `--mixed`, gone for `--hard`).
5. **Bisect named one culprit and cleaned up.** Output ended with `<sha> is the first bad commit`, `git show <sha>` plausibly explains the regression, and `git bisect reset` returned HEAD to the starting branch (`git status` confirms the original branch, not detached).
6. **Nothing was pruned mid-recovery.** No `git gc`/`reflog expire` ran before the ref was secured; the `_backup` branch from step 1 still exists as a fallback.

Done = the recovered commits/branch/stash are on a named ref whose tree matches the known-good SHA (`git diff` empty), any undo matched its published-vs-local audience (revert vs reset mode), and bisect (if used) named the first bad commit with `git bisect reset` leaving HEAD on the original branch.
