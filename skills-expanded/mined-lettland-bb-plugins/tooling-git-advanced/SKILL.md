---
name: tooling-git-advanced
description: Use when reaching for git's deeper toolset — bisect, rerere, worktree, reflog, sparse checkout, shallow clone, and commit signing.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: tooling
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [tooling-shell-fish, tooling-fzf, tooling-jq, tooling-ripgrep, using-git-worktrees, debugging, root-cause]
---

# Git — Beyond `add`, `commit`, `push`

Git's headline commands cover 90% of daily work. The remaining 10% are what get you out of trouble — a regression you can't reproduce, three feature branches in parallel, a corrupted index, a rebase that ate your work. Know these before you need them.

**Core principle:** Git almost never loses data; it just stops referencing it. Most "I lost my work" situations are recoverable via `reflog`. Stay calm before reaching for destructive recovery.

## `git bisect` — binary search for the bad commit

When `main` worked yesterday and is broken today, bisect finds the offending commit in `log2(N)` steps.

```sh
git bisect start
git bisect bad                 # current HEAD is broken
git bisect good v1.4.0         # known-good ref
# git checks out the midpoint; test it
git bisect good                # or: git bisect bad
# ... repeat until ...
# abc1234 is the first bad commit
git bisect reset               # return to your branch
```

**Automate it** when the test is scriptable:

```sh
git bisect start HEAD v1.4.0
git bisect run ./scripts/repro.sh   # exit 0 = good, 1–127 (≠125) = bad, 125 = skip
```

The script does the work; you walk away with the SHA. Works against any reproducible failure — performance regression, test failure, broken build.

## `git reflog` — your undo log

Every move of `HEAD` or a branch tip lands in the reflog. 90 days by default.

```sh
git reflog                                    # recent HEAD movements
git reflog show feature-branch                # per-branch
git reset --hard HEAD@{2}                     # rewind to the state 2 moves ago
```

If you `reset --hard` over uncommitted work, reflog won't save you (working tree wasn't committed). If you `reset --hard` over committed work, **it will**.

## `git worktree` — multiple branches checked out at once

Switching branches mid-stash is a tax. Worktrees let you have several branches checked out as sibling directories sharing one `.git`.

```sh
git worktree add ../myrepo-hotfix hotfix-branch
cd ../myrepo-hotfix
# work, commit, push, then:
cd ../myrepo
git worktree remove ../myrepo-hotfix
git worktree prune
```

Each worktree has its own index and HEAD; commits land in the same repo. Use for: parallel review of two PRs, running long tests on `main` while developing on a branch, build caches per-branch. See `Skill(using-git-worktrees)` for the workflow pattern.

## `git rerere` — remember conflict resolutions

If you rebase the same branch repeatedly (long-running feature against fast-moving `main`), you'll hit the same merge conflicts. `rerere` records your resolution once and replays it.

```sh
git config --global rerere.enabled true
```

Set it and forget it. The next time the same hunk-pair conflicts, git applies your earlier resolution silently. Check `git rerere status` to see what's been remembered.

## `git sparse-checkout` — partial working tree

For monorepos where you don't want the whole tree on disk:

```sh
git clone --filter=blob:none --no-checkout <url> repo
cd repo
git sparse-checkout init --cone
git sparse-checkout set apps/web libs/shared
git checkout main
```

Cone mode is the fast path (whole-directory inclusions). Non-cone supports gitignore-style patterns but is slower. Combined with `--filter=blob:none` (partial clone), you fetch blobs on demand.

## `git clone --depth=N` — shallow clones for CI

Default clones fetch full history (megabytes to gigabytes for old repos). Shallow clones fetch only the last N commits.

```sh
git clone --depth=1 <url>                     # tip only
git clone --depth=50 --no-single-branch <url> # last 50 commits, all branches
```

CI is the prime user. **Don't shallow-clone for actions that need history** — `set-commits --auto` (Sentry), changelog generation, blame. Use `fetch-depth: 0` in `actions/checkout` for those.

## Commit signing — provenance

GPG and SSH signing both work. SSH signing is the path of least resistance — same key as your push auth.

```sh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global gpg.format ssh
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

Add the key to GitHub/GitLab as a **signing key** (separate from auth key in some setups). Require signed commits on `main` via branch protection. Now every commit on `main` carries cryptographic provenance.

## `git stash` — but better

`git stash` is fine; `git stash push -u -m "WIP: extracting validator"` is better. Always:

- `-u` to include untracked files (default leaves them behind)
- `-m` so the stash list is readable later
- `git stash show -p stash@{2}` to peek
- `git stash pop` to apply + drop; `git stash apply` to apply + keep

For more than two stashes in flight, switch to a throwaway branch — stashes are stack-shaped and easy to lose.

## `git log` — the queries you actually need

```sh
git log --oneline --graph --decorate --all          # tree view
git log -S "addUser" --source --all                 # commits that touched the string "addUser"
git log -G "regex" --                               # regex search across diffs
git log --grep="fixes #1234"                        # commit message search
git log main..feature --no-merges                   # commits on feature not on main
git log -- path/to/file                             # history of one file
git log --follow -- path/to/file                    # follow renames
```

`-S` (pickaxe) is the killer query for "when did this function appear/disappear." Faster than `git blame` for non-trivial archaeology.

## Disaster recovery

| Situation                                      | Fix                                                                                                           |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `git reset --hard` over committed work (LOCAL) | `git reflog`, `git reset --hard HEAD@{1}`                                                                     |
| Same, on a PUSHED branch                       | Use `git revert <sha>...<sha>` to produce a forward-fixing commit — DO NOT reset+force-push on shared history |
| Force-pushed over a branch                     | Coworker still has it: `git fetch <them> branch:branch`                                                       |
| Bad merge committed                            | `git revert -m 1 <merge-sha>` (don't reset on shared branches)                                                |
| Detached HEAD with new commits                 | `git branch save-me HEAD` before checking out elsewhere                                                       |
| Corrupted index                                | `rm .git/index && git reset`                                                                                  |

## Anti-patterns

- `git push --force` on shared branches — use `--force-with-lease --force-if-includes` (Git 2.30+; closes the fetch-then-lease race) at minimum, prefer never
- `git pull` without knowing if it's merge or rebase — set `pull.rebase=true` or `pull.ff=only`
- Shallow clone in CI then trying to generate a changelog — silently truncated
- `rerere` enabled on long-shared branches with multiple authors — replays your resolutions on conflicts you didn't see; enable only on personal/feature branches
- Storing creds in URLs (`https://user:token@host/...`) — appears in `git remote -v`, shell history, process table. Use `git config credential.helper` (`osxkeychain`, `libsecret`, `manager`, or `cache`), SSH keys, or `GH_TOKEN`/`GITHUB_TOKEN` env vars consumed by `gh`/`glab`
- `--no-verify` to skip pre-commit hooks "this once" — almost always wrong

## Hand-off

For worktree-driven workflows, `Skill(using-git-worktrees)`. For shell-side ergonomics (aliases, abbreviations), `Skill(tooling-shell-fish)`. For interactive history browsing with preview, `Skill(tooling-fzf)`. For investigating why a commit landed the way it did, `Skill(debugging)` and `Skill(root-cause)`.
