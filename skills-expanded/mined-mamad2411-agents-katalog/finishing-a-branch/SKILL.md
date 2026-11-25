---
name: finishing-a-branch
description: "Wrap up finished code work safely: confirm the tests pass, then let the Commander choose to merge it, open a pull request, or keep it for later. Nothing is deleted or overwritten without the Commander's clear go-ahead."
license: MIT
metadata:
  title: "Finishing a Branch"
  category: "Engineering"
  author: "Jesse Vincent"
---

# Finishing a Branch

## Overview

**Core principle:** verify tests → detect the environment → present the options → carry out the choice → clean up.

Use this when the implementation on a branch is complete and the question is how to integrate it. The integration decision belongs to the Commander; your job is to make it safe and easy.

All commands run through `shell.exec` (tests through `verify.run`). On Windows `shell.exec` runs `cmd.exe`, so do not rely on shell variables: run each git command, read its output, and carry the values yourself. To run from another folder, pass that folder as `cwd`; do not `cd` with absolute paths.

If the project has its own written merge rules (a contributing guide, a repo protocol file), those rules win over this menu. Read them first.

## Step 1: Verify tests

Run the project's full test suite with `verify.run` (`cmd`: `npm test`, `cargo test`, `pytest`, `go test ./...`, or whatever the project uses). Read the whole result.

**If tests fail**, report the failures and stop. The menu comes only after a green suite:

```
Tests failing (<N> failures). Must fix before completing:

[the failures]
```

**If tests pass:** continue to Step 2.

## Step 2: Detect the environment

Run these and write down the answers now, while you are still inside the workspace (Step 5 moves to another folder, and Step 6 needs these values):

| Command | You learn |
|---------|-----------|
| `git rev-parse --absolute-git-dir` | GIT_DIR |
| `git rev-parse --path-format=absolute --git-common-dir` | GIT_COMMON |
| `git rev-parse --show-toplevel` | WORKTREE_PATH (this workspace) |
| `git branch --show-current` | the branch name; empty means a detached HEAD |
| `git worktree list` | the first line is the main repo root (MAIN_ROOT) |
| `git status --porcelain` | uncommitted work; commit it or ask before going on |

This decides which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| GIT_DIR equals GIT_COMMON (normal repo) | Standard 3 options | No worktree to clean up |
| GIT_DIR differs, named branch | Standard 3 options | Depends on who made the worktree (Step 6) |
| GIT_DIR differs, detached HEAD | Reduced 2 options (no merge) | Managed from outside: leave it in place |

## Step 3: Determine the base branch

The base branch is whatever this work forked from, usually named in the plan, the conversation, or the branch's upstream. If it is not already known, ask: "This branch split from <your best guess> - is that correct?" Confirm before merging: a merge into the wrong base is expensive to undo.

## Step 4: Present the options

**Normal repo, or a worktree on a named branch. Present exactly these 3 options:**

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)

Which option?
```

**Detached HEAD. Present exactly these 2 options:**

```
Implementation complete. You're on a detached HEAD (externally managed workspace).

1. Push as new branch and create a Pull Request
2. Keep as-is (I'll handle it later)

Which option?
```

Present the menu as written: short, every option from the list above. Discarding the work is never on the menu; it happens only when the Commander asks for it in so many words (see "If the Commander asks to discard the work"). Wait for the answer.

In a run where nobody can answer (a scheduled run, a dispatched worker), do not choose for them: report "tests green, branch <name> kept as-is" and stop.

## Step 5: Carry out the choice

### Option 1: Merge locally

Run from MAIN_ROOT (pass it as `cwd`). Merge first, and verify success before removing anything:

```
git checkout <base-branch>
git pull
git merge <feature-branch>
```

Then run the test suite on the merged result, in MAIN_ROOT: `shell.exec` with `cwd` = MAIN_ROOT and the project's test command, reading the full output and the exit code.

If the tests fail on the merged result: stop, leave the worktree and the branch in place, and investigate (the `systematic-debugging` procedure fits). Nothing has been pushed, so the merge is local and recoverable.

Once the merged result is green: clean up the worktree (Step 6), then delete the merged branch:

```
git branch -d <feature-branch>
```

`-d` refuses to delete a branch that is not fully merged. If it refuses, stop and report; do not reach for `-D`.

Option 1 does not push. If the Commander also wants the merged base pushed, that is a separate, explicit request.

### Option 2: Push and create a pull request

```
git push -u origin <feature-branch>
```

From a detached HEAD, name the new branch on the remote instead: `git push origin HEAD:refs/heads/<new-branch>`.

Then create the pull request against <base-branch>: with the `gh` command line if it is installed and signed in (check `gh --version` and `gh auth status`), with the connected GitHub account's tools (find them with `tool.search`), or by giving the Commander the creation link most hosts print when you push. Follow the repo's pull request template and conventions if it has them. Report the pull request URL.

Keep the worktree. Review feedback gets fixed there.

### Option 3: Keep as-is

Report: "Keeping branch <name>. Worktree preserved at <path>."

### If the Commander asks to discard the work

This path exists only as the answer to an explicit request to throw the work away. List what would be lost (`git log --oneline <base-branch>..<feature-branch>`), then confirm first:

```
This will permanently delete:
- Branch <name>
- All commits: <commit list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for that exact word. When it arrives, work from MAIN_ROOT: clean up the worktree (Step 6), then force-delete the branch:

```
git branch -D <feature-branch>
```

## Step 6: Clean up the workspace

**Runs for Option 1 and for a confirmed discard only.** Options 2 and 3 always keep the worktree. Worktree removal must run from outside the worktree, so use `cwd` = MAIN_ROOT and the values you wrote down in Step 2.

**If GIT_DIR equals GIT_COMMON:** a normal repo, no worktree to clean up. Done.

**If WORKTREE_PATH is inside the repo under `.worktrees/` or `worktrees/`, and this job created it:** you own the cleanup. Use the path relative to MAIN_ROOT:

```
git worktree remove .worktrees/<name>
git worktree prune
```

(`prune` clears any stale registrations.)

**If removal is refused** ("contains modified or untracked files"): the worktree holds files that exist nowhere else, such as uncommitted plans, notes, or scratch work. Never add `--force` on your own initiative. Show the Commander what is at stake (run `git status --porcelain -uall` with `cwd` = WORKTREE_PATH) and ask:

```
Worktree removal refused - these files were never committed:

<file list>

1. Commit them to <branch> before cleanup
2. Move them into <main repo root>
3. Delete them (unrecoverable)

Which?
```

Carry out the choice, then remove the worktree.

**Otherwise:** the workspace belongs to the Commander or to whatever created it. Leave it in place and say where it is.

## Quick reference

| Option | Merge | Push | Keep worktree | Delete branch |
|--------|-------|------|---------------|---------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| Discard (explicit request only) | - | - | - | yes (force) |

## Common rationalizations

| Excuse | Reality |
|--------|---------|
| "Tests passed earlier this session" | Run the suite on the tree you are about to integrate. A green run only proves the tree it ran on. |
| "They obviously want it merged" | Integration is the Commander's decision. Present the menu and wait. |
| "They seem done with this feature - I'll offer to discard it" | The menu is complete as written. Discard happens only when the Commander asks for it in so many words. |
| "'Yeah, get rid of it' counts as confirmation" | Only the typed word `discard` authorizes deletion. |
| "The PR is up, so the worktree is clutter now" | Review feedback gets fixed in that worktree. It stays until the work lands. |
| "This other worktree looks stale - I'll clean it too" | Clean up only a worktree this job created under `.worktrees/` or `worktrees/`. Everything else belongs to someone else. |
| "Removal refused - `--force` is just finishing the cleanup" | The refusal means files exist only in that worktree. `--force` destroys them for good. Show the Commander and ask. |
| "The merged-result failure is probably flaky" | A failing merged result stops everything. Branch and worktree stay put while you investigate. |
| "The base branch is obviously main" | Confirm the fork point or ask. A merge into the wrong base is expensive to undo. |
| "The push was rejected - a force-push will fix it" | A rejected push means the remote moved. Investigate; force-push only on the Commander's explicit request. |

## Done means

The suite was green on the exact tree that was integrated, the Commander's chosen option was carried out and its result read back (the merge commit in `git log`, the pull request URL, or the kept branch name), and no branch, commit, worktree or uncommitted file was removed without the Commander's explicit word.

## Output

One short report: the test result, the option chosen, what now exists (merged commit, PR link, or kept branch and its path), and anything left in place for the Commander.

*Needs the WORKBENCH (shell.exec for git, verify.run for the tests). Pull requests use the `gh` command line or a connected GitHub account.*

Adapted for StarNet from finishing-a-development-branch (Jesse Vincent, obra/superpowers), MIT.
