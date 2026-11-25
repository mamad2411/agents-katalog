---
name: session-sync
description: "Brings every worktree of the current repository up to date with its base branch without a local force push, choosing per branch: fast-forward, local rebase if never pushed, forge-side rebase if a request is open, or skip. Use when the session-start hook reports BEHIND origin/<base>, or when feature worktrees have drifted. Skips dirty trees and branches ahead of or diverged from their remote, never resets one that moved mid-rebase, and reports one closed-status row per worktree. Not for landing a branch (use github-workflow:pr-lifecycle or gitlab-workflow:mr-lifecycle). Claude Code only."
disable-model-invocation: true
allowed-tools: Bash(git fetch origin --prune), Bash(git worktree list --porcelain), Bash(git symbolic-ref --quiet refs/remotes/origin/HEAD), Bash(git show-ref --verify --quiet *), Bash(git config --get *), Bash(git rev-list --count *), Bash(git rev-parse --verify --quiet *), Bash(git merge-base --is-ancestor *), Bash(git remote get-url origin), Bash(sleep 10)
license: MIT
---

# Session sync

Bring every worktree of the current repository current with its target branch **without a local
force push**. This is the remediation for the `session-start` hook reporting `BEHIND origin/<base>`,
and for the slow drift across a handful of long-lived feature worktrees.

The safety thesis: a bulk sweep is the worst place to rewrite remote branches. You are operating on
branches you are not thinking about, several at a time, and one bad lease damages a branch you never
meant to touch. So the route for each branch follows from *how it is published*, and wherever a route
exists that needs no local rewrite of a published branch, the sweep takes it. The `pre-bash` hook in
this plugin blocks force pushes to protected branches independently; the two agree by design, and
this skill does not rely on the hook.

The pre-approved commands are read-only. Every command that changes a branch — `pull --ff-only`,
`rebase`, `reset --hard`, and the forge rebase — asks the user first, so each rewrite is confirmed.

## Invariants

- The only push to a published branch is the one the forge makes with its own permission.
- A worktree with any uncommitted or untracked file is left exactly as it is.
- `reset --hard` runs only on a worktree just confirmed clean whose branch tip is contained in the
  remote tip recorded before the forge rebase, so every local commit is already in what the forge
  rebased. A fact that cannot be established counts as "do not touch".
- Shell variables do not persist between Bash calls, so any value carried from one step to a later
  one (such as the recorded remote tip) is written into the later command literally.
- A conflicting rebase is aborted, and the user gets one command to run.
- Each branch is compared with its **target**: the value of `branch.<branch>.releasetrainbase` when
  that key is set (a `release-train` worker branch, cut from `release/<slug>`), otherwise the
  repository base. Rebasing a release-train branch onto the default branch would pull in commits it
  was never cut from.

## Statuses

Every worktree gets exactly one of these. The same list is used in the procedure and the report.

| Status | Meaning | What the user does |
| --- | --- | --- |
| `current` | 0 commits behind its target | Nothing |
| `ff-only` | Base checkout fast-forwarded | Nothing |
| `ff-refused` | Base checkout has commits of its own, so `--ff-only` refused | Inspect those commits; they were not meant to be on the base |
| `rebased-local` | Never-pushed branch rebased locally onto its target | Nothing |
| `rebased-server` | Forge rebased the published branch; local worktree resynced | Nothing |
| `rebase-pending` | Forge accepted the rebase but it had not landed within the poll cap | Re-run later, or check the request page |
| `local-moved` | Forge rebase landed, but the local branch was no longer contained in the recorded remote tip, or the tree was no longer clean, so it was not reset | Compare `<branch>` with `origin/<branch>` and reconcile by hand |
| `skipped-dirty` | Uncommitted or untracked files present | Run the printed command |
| `skipped-detached` | Detached HEAD; no branch to sync | Nothing, or check out a branch |
| `unpushed-commits` | Published branch is ahead of its remote, and the remote has nothing the branch lacks | Push, then re-run |
| `diverged` | Published branch and its remote each have commits the other lacks (for example a `release-train` worker rebased after its backup push) | Inspect both sides; publishing needs `--force-with-lease`, a deliberate single-branch act |
| `no-request` | Published, but no open pull or merge request | Open one, or rebase deliberately by hand |
| `no-forge-cli` | Forge not recognized, or `gh`/`glab` not installed or not authenticated | Install and authenticate the CLI, then re-run |
| `no-permission` | Forge refused the rebase for lack of push permission on the branch | Ask the branch owner |
| `conflict` | Rebase hit conflicts (local or on the forge) | Run the printed command and resolve |
| `error` | Forge rebase command failed for another reason (network, server error, expired token, a pre-receive hook) | Read the printed forge message, fix the cause, then re-run |
| `unknown` | Behind-count could not be computed (e.g. the target has no `origin/` ref) | Check the target branch name and the fetch |

## Procedure

1. **Resolve the repository base.** Ask the remote first, since a repository whose default is
   `develop` or `trunk` has no local `main`:

   ```sh
   git symbolic-ref --quiet refs/remotes/origin/HEAD    # -> refs/remotes/origin/<base>
   ```

   Strip the `refs/remotes/origin/` prefix. If it is unset, try `main`, then `master`:

   ```sh
   git show-ref --verify --quiet refs/remotes/origin/main
   git show-ref --verify --quiet refs/remotes/origin/master
   ```

   If neither exists, stop and report that no base branch could be resolved, rather than picking one.

2. **Fetch once:** `git fetch origin --prune`.

3. **Enumerate worktrees:** `git worktree list --porcelain`. Read the `worktree <path>` and
   `branch refs/heads/<name>` pairs; an entry with `detached` is `skipped-detached`.

4. **Gather every fact for a worktree before deciding anything.** Branch refs and config are shared
   across worktrees, so only the dirty check needs `-C`:

   ```sh
   git config --get "branch.<branch>.releasetrainbase"       # set -> that is <target>; unset -> <base>
   git rev-list --count "<branch>..origin/<target>"          # behind; an error -> unknown
   git -C "<path>" status --porcelain                         # any output, untracked included -> dirty
   git rev-parse --verify --quiet "refs/remotes/origin/<branch>"   # resolves -> published
   git rev-list --count "origin/<branch>..<branch>"          # published only: ahead of its own remote
   git rev-list --count "<branch>..origin/<branch>"          # published only: remote-only commits
   ```

5. **Pick the route**, first match wins:

   | Facts | Route | Status |
   | --- | --- | --- |
   | behind-count errored | none | `unknown` |
   | behind is 0 | none | `current` |
   | dirty, not published | none; print `git -C "<path>" stash -u && git -C "<path>" rebase origin/<target> && git -C "<path>" stash pop` | `skipped-dirty` |
   | dirty, published | none; print `commit or stash in "<path>", then re-run session-sync` | `skipped-dirty` |
   | branch is the base, in its own checkout | `git -C "<path>" pull --ff-only origin <base>` | `ff-only` or `ff-refused` |
   | not published | local rebase, step 6 | `rebased-local` or `conflict` |
   | published, ahead > 0 and remote-only > 0 | none | `diverged` |
   | published, ahead > 0 | none | `unpushed-commits` |
   | published, ahead is 0 | forge rebase, step 7 | see step 7 |

   A dirty published branch gets no rebase command, because rebasing it locally would make its next
   push a force push; the forge route on a later run needs no rewrite.

   On `ff-refused`, report it and stop for that worktree. A plain `git pull` would invent a merge
   commit on the base, and a reset would discard the commits you need to look at.

6. **Local rebase** (never-pushed branches only; nothing remote exists to rewrite):

   ```sh
   git -C "<path>" rebase "origin/<target>"
   ```

   If it stops on a conflict, run `git -C "<path>" rebase --abort` and record `conflict`.

7. **Forge rebase** (published, in sync with its remote). Identify the forge from
   `git remote get-url origin`: a GitHub host uses `gh`, a GitLab host uses `glab`. For any other
   host, ask the user which CLI applies; if none is installed or authenticated, record `no-forge-cli`
   and move on. Leave a missing CLI as that named gap: a local rebase plus a force push is the
   behaviour this skill exists to avoid.

   Before calling the forge, record the remote tip. The forge rebase replaces it with new commits,
   so this is the only record of what the local branch was in sync with:

   ```sh
   git rev-parse --verify --quiet "refs/remotes/origin/<branch>"   # note the SHA as <old-remote>
   ```

   | Forge | Command | No open request | Refused |
   | --- | --- | --- | --- |
   | GitHub | `gh pr update-branch "<branch>" --rebase` | "no pull requests found" → `no-request` | permission error → `no-permission`; conflict error → `conflict`; any other non-zero exit → `error` |
   | GitLab | `glab mr rebase "<branch>"` | "no open merge request" → `no-request` | permission error (403) → `no-permission`; "resolve all conflicts" (GitLab's conflict message) → `conflict`; any other non-zero exit → `error` |

   `--rebase` matters on GitHub: without it, `update-branch` merges the base into the branch.
   `glab mr rebase` waits on the server until GitLab reports the rebase finished, and exits non-zero
   with GitLab's message when it failed, so its exit code is the outcome. GitHub runs the rebase
   asynchronously. After either, poll until the fetched branch shows it, at most six times:

   ```sh
   git fetch origin --prune
   git merge-base --is-ancestor "origin/<target>" "origin/<branch>"   # exit 0 -> rebase landed
   sleep 10                                                           # between checks only
   ```

   The forge rebases onto the request's own target branch, so this check assumes that branch is
   `<target>`; if they differ, say so in the report. After six checks without success, record
   `rebase-pending` and print `gh pr view "<branch>"` or `glab mr view "<branch>"` for the user.

   When the rebase landed, resync the local worktree. The ahead count from step 4 no longer applies:
   the forge rewrote the commits, so the old local commits always count as ahead of the new remote.
   Instead, because time has passed, re-check that the tree is clean and that the local branch holds
   nothing beyond the recorded tip (write the SHA in literally):

   ```sh
   git -C "<path>" status --porcelain                        # must print nothing
   git merge-base --is-ancestor "<branch>" "<old-remote>"    # exit 0 -> every local commit was rebased
   ```

   Only when both hold:

   ```sh
   git -C "<path>" reset --hard "origin/<branch>"
   ```

   Record `rebased-server`. If either check fails, leave the worktree as it is and record
   `local-moved`.

8. **Hand conflicts back.** For each `conflict`, print exactly one line and leave that worktree:

   ```text
   cd "<path>" && git rebase origin/<target>   # resolve, then: git rebase --continue
   ```

   If the branch is published, the follow-up push after a hand-resolved rebase needs
   `git push --force-with-lease`, after a fresh `git fetch`. Print that as text for the user; the
   sweep may be partway through several worktrees, and rewriting a remote branch is a deliberate,
   single-branch act.

9. **Verify.** For every worktree that got `ff-only`, `rebased-local` or `rebased-server`, re-count:

   ```sh
   git rev-list --count "<branch>..origin/<target>"
   ```

   Expect 0 and put the result in the *After* column. A non-zero re-count means the target moved
   during the sweep; say so under the table and suggest re-running.

## Report

One row per worktree, then the printed commands:

```markdown
| Worktree | Branch | Target | Behind | After | Status |
| --- | --- | --- | --- | --- | --- |
| <path> | <branch> | <target> | <n> | <n or –> | <status from the table above> |

Commands to run yourself:
- <one line per skipped-dirty, conflict, error, rebase-pending, diverged, or local-moved row>
```

## Examples

<example>
A sweep over seven worktrees on a GitHub repository whose base is `main`:

| Worktree | Branch | Target | Behind | After | Status |
| --- | --- | --- | --- | --- | --- |
| ~/src/app | main | main | 3 | 0 | ff-only |
| .claude/worktrees/payments | feature/payments-retry | main | 4 | 0 | rebased-server |
| ~/src/app-config | feature/config-loader | main | 2 | 0 | rebased-local |
| ~/src/app-search | feature/search-index | main | 2 | – | skipped-dirty |
| ~/src/app-docs | feature/docs-nav | main | 1 | – | no-request |
| ~/src/app-auth | feature/auth-scopes | main | 3 | – | diverged |
| ~/src/app-cache | feature/cache-ttl | main | 2 | – | local-moved |

`feature/search-index` was never pushed, so its dirty worktree gets the stash-and-rebase line.
`feature/auth-scopes` was rebased locally after it was pushed, so its remote has commits it lacks;
the sweep leaves it for the user rather than pushing. `feature/cache-ttl` gained a commit while
the forge rebase was polling, so it is no longer contained in the recorded remote tip and is not
reset.
</example>

<example>
A worktree on `rt/q3-refactor/api` has `branch.rt/q3-refactor/api.releasetrainbase` set to
`release/q3-refactor`. Its target is `release/q3-refactor`, not `main`: it is 0 behind that target,
so the row is `current`, even though it is 40 commits behind `main`.
</example>

<example>
`origin` is a GitHub host, but `gh` is not installed. A published, in-sync branch is 5 behind.

Correct: record `no-forge-cli` and tell the user to install and authenticate `gh`. Wrong: rebase it
locally and push with a lease, because that is the bulk remote rewrite this skill exists to prevent.
</example>

<example>
On a GitLab repository, `glab mr rebase "feature/api-limits"` exits non-zero with
`Rebase failed: Rebase locally, resolve all conflicts, then push the branch.`, and
`glab mr rebase "feature/api-docs"` exits non-zero with `502 Bad Gateway`.

Correct: `feature/api-limits` is `conflict` and gets the rebase line; `feature/api-docs` is `error`,
and the report prints GitLab's message under "Commands to run yourself" with "re-run session-sync".
Wrong: `conflict` for the 502, which sends the user to resolve conflicts that do not exist.
</example>

## Notes

- Only worktrees of the **current** repository. Run it from anywhere inside it.
- Being behind the base is not an error and does not block a push; `current` and `no-request` rows
  usually need no action.
- Syncing a branch is not marking it ready; leave any draft flag on a request as it is.

## Surface

Claude Code only. It enumerates worktrees from disk and runs `git`, and Cowork has neither a
checkout nor a shell. There is no pasted-data fallback, because the input is the state of the working
trees themselves.
