---
name: git-workflow
description: Uses Git safely and cleanly - atomic commits with clear messages, branching, rebase vs merge, conflict resolution, pull request descriptions, and recovering from mistakes such as lost commits, bad merges, commits on the wrong branch, or a committed secret. Use when committing, writing commit messages, branching, rebasing, merging, resolving conflicts, preparing a pull request, undoing changes, cleaning history, or when someone says they broke their repository.
license: MIT
---

# Git Workflow

History is shared infrastructure. Keep commits small and explainable, never rewrite history other people have pulled, and know how you will get back (the reflog, a backup branch) before running anything destructive.

## Safety rules

Stop and get explicit confirmation from the user before running any of these. Say exactly what could be lost.

| Command | Risk |
|---|---|
| `git push --force` / `--force-with-lease` | Rewrites the remote branch; others' commits can be lost |
| `git reset --hard` | Permanently discards uncommitted changes |
| `git clean -fd` (or `-fdx`) | Permanently deletes untracked (and ignored) files |
| `git restore <path>` / `git checkout -- <path>` | Permanently discards uncommitted changes in those files |
| `git branch -D` / `git push origin --delete <branch>` | Deletes a branch; the remote one may be unrecoverable for you |
| `git stash drop` / `git stash clear` | Removes stash entries (recovery is possible but awkward) |
| `git rebase` on a branch others use | Rewrites shared history |
| `git filter-repo` or any history rewrite | Changes every affected commit ID; all clones must be reset |

Before a risky operation:

1. Run `git status` and `git stash list` and read the output.
2. Create a backup ref: `git branch backup/before-rebase` (any clear name).
3. Prefer the safer variant: `--force-with-lease` over `--force`, `git reset --keep` over `--hard`, `git revert` over rewriting pushed history.

Also: never skip hooks with `--no-verify` unless the user asks, and never push, open pull requests or delete remote branches unless the user asked for it.

## Commits

- **One logical change per commit.** Each commit should build and pass tests, so `git bisect` and `git revert` work cleanly.
- **Stage deliberately.** Name the files: `git add src/orders/refund.ts tests/refund.test.ts`. Avoid `git add .` / `git add -A` unless you have read `git status` and every change belongs in the commit. (`git add -p` stages parts of files but is interactive; use it only in an interactive terminal.)
- **Review what you are committing:** `git diff --cached`. Look for secrets, debug output, generated files and unrelated changes.
- **Write the message:**

```text
<summary: imperative mood, about 50 chars, at most 72>

<body: what changed and why, not how. Wrap at 72. Mention
trade-offs, alternatives rejected, and anything surprising.>

<footer: Refs #123, Co-authored-by: ..., BREAKING CHANGE: ...>
```

- Imperative summary: "Add retry with backoff to payment client", not "Added retries" or "fix stuff".
- **Follow the repository's convention first.** Check `git log --oneline -20` and any commitlint or contributing config. If the project uses [Conventional Commits](https://www.conventionalcommits.org/), use its types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, with `!` or a `BREAKING CHANGE:` footer for breaking changes.
- Do not commit build output, dependencies, local environment files or editor folders; check `.gitignore` covers them.

## Branching

| Model | Fits | Rules |
|---|---|---|
| **Trunk-based** (short-lived branches, feature flags) | Continuous delivery, most product teams | Branches live hours to a couple of days; main is always releasable; unfinished work hides behind flags |
| **Feature branch + pull request to main** (GitHub flow) | Most web and service projects | Same as above, with review on every PR; deploy from main |
| **Release branches** (and Gitflow-style models) | Several supported versions, scheduled releases, mobile or on-premises software | Fixes land on main and are cherry-picked to release branches (or the reverse, consistently); more merge overhead |

Name branches the way the repository already does (for example `feat/refund-retries`, `fix/1234-null-org`).

## Rebase or merge

| Situation | Do this |
|---|---|
| Update your own, unshared feature branch with main | `git fetch origin` then `git rebase origin/main` (or `git merge origin/main` if the team prefers merge commits) |
| The branch is shared or others build on it | Merge (`git merge origin/main`); do not rebase |
| Tidy your own commits before review | Make fixup commits with `git commit --fixup <sha>`, then `GIT_SEQUENCE_EDITOR=: git rebase -i --autosquash origin/main` (the empty editor accepts the generated plan non-interactively). Or `git reset --soft origin/main` and recommit in clean steps. |
| Push after rebasing your own branch | `git push --force-with-lease --force-if-includes` (Git 2.30+), after confirmation |
| Integrate a PR into main | Use the repository's setting: squash merge, rebase merge or merge commit. Do not change it per PR without agreement. |

`--force-with-lease` refuses to overwrite the remote branch if it moved since your last fetch. A background fetch (from an editor, for example) can defeat it, which is what `--force-if-includes` guards against.

## Resolving conflicts

1. `git status` lists the conflicted files.
2. Understand both sides before editing:
   - `git diff` shows the conflict hunks.
   - `git log --merge -p -- <file>` shows the commits on each side that touched the file.
   - During a **merge**, "ours" is your current branch and "theirs" is the branch being merged in. During a **rebase**, it is reversed: "ours" is the branch you are rebasing onto, and "theirs" is your commit being replayed.
3. Resolve by intent: keep both changes when both are needed. Never take one side wholesale without reading the other.
4. Remove every conflict marker. `git diff --check` reports leftover markers and whitespace errors.
5. Lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`, ...): do not hand-merge. Take one side, then rerun the package manager so it regenerates the lockfile from the merged manifest.
6. Build and run the tests before continuing.
7. `git add <file>`, then `git rebase --continue` or `git merge --continue`. To back out completely: `git rebase --abort` or `git merge --abort`.

For conflicts that keep recurring (long-running branches, repeated rebases), enable `git config rerere.enabled true` so Git reuses recorded resolutions.

## Pull request descriptions

Self-review the full diff first (`git diff origin/main...HEAD`). Keep PRs small: under about 400 lines of logic is reviewable in one sitting. Then describe it:

```markdown
## What
One or two sentences on the change.

## Why
The problem, with a link to the issue.

## How
Notable decisions and alternatives considered.

## Testing
Commands run, manual steps, screenshots or recordings for UI changes.

## Risk and rollout
Migrations, feature flags, backward compatibility, how to roll back.
```

## Large files

- Do not commit large binaries or datasets. Use Git LFS (`git lfs track "*.psd"`, then commit `.gitattributes`) or an artifact store.
- To find large objects in history (POSIX shell):

```bash
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1 == "blob"' | sort -k3 -n | tail -20
```

## A secret was committed

1. **Treat the secret as compromised as soon as it was pushed,** even if it was removed a minute later: clones, forks, CI logs and caches may have it. **Rotate or revoke it first.** That is the real fix. Tell the user immediately.
2. **Not pushed yet:** remove the secret from the files, move it to environment variables or a secret manager, add the file to `.gitignore`, and amend or redo the commit (`git reset --soft HEAD~1`, fix, recommit).
3. **Already pushed:** after rotating, decide with the user whether to rewrite history with `git filter-repo` (not `git filter-branch`). This needs a force-push and every collaborator must re-clone or reset. Hosting platforms may keep old commits reachable (pull request refs, caches); their support or docs describe how to purge them. Recipes are in [references/recovery-recipes.md](references/recovery-recipes.md).
4. **Prevent the next one:** a secret scanner in pre-commit and CI (for example gitleaks or trufflehog), and the hosting platform's push protection if available.

## Anti-patterns

- Messages like "WIP", "fix", "updates"; commits mixing refactoring, features and formatting.
- Rebasing or force-pushing shared branches, especially main.
- `git add .` without reading `git status`, committing `.env` files and build output.
- Resolving conflicts by accepting one side everywhere.
- Branches that live for weeks and then cannot be merged.
- Deleting and re-cloning the repository instead of using the reflog.
- Rewriting history to "remove" a leaked secret without rotating it.

## Done when

- Each commit is one logical change, builds, and has a clear imperative message that follows the repository's convention.
- No secrets, generated files or unrelated changes were committed.
- Conflicts are resolved with tests passing and no markers left.
- Every destructive or outward-facing command was confirmed by the user, with a backup ref in place first.

## References

- [references/recovery-recipes.md](references/recovery-recipes.md) — read when something went wrong: undoing commits, recovering lost work, fixing commits on the wrong branch, reverting merges, or rewriting history to remove a secret or large file.
