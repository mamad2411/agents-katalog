---
name: todo-push
description: Use when the user invokes /todo-push, says "ship this", "push this up and merge it", "checkout from main, commit, push, create PR, merge to main", or describes the full branch-to-merge git workflow (not a single git step). Works in any repo, not just the hub.
---

# todo-push — branch, commit, push, PR, merge

One shot: take whatever is uncommitted on the current branch, land it on `main` via a
real PR. Sequence: checkout a branch off main → run tests → commit → push →
`gh pr create` → `gh pr merge --merge` → back on main.

This skill executes a shipping decision that's already been made. If the user is at
"implementation is done — now what?" and `superpowers:finishing-a-development-branch`
is installed, run that first — it walks the merge/PR/cleanup choice; this skill is the
execution arm for its "PR and merge" outcome.

## Execution tier

Use the **fast** tier from [`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md). Delegate to a
general-purpose subagent with shell and GitHub CLI access when the host supports it;
otherwise execute inline. The invoking session must wait for the shipping result before
continuing. Select the fast tier's resolved host model only when
the host supports per-dispatch model selection. Never invent unsupported parameters.

## Warm-start the subagent — the speed lever

The subagent starts with **zero conversation history**. The slow part of a cold handoff
isn't the git commands — it's the subagent re-running `git status` / `git diff` /
`git log` / base-branch detection / test-command discovery, round-trips whose answers
**you (the calling session) usually already have**, because `/todo-push` is almost always
invoked right after you did the work.

So before invoking, **prepend to the prompt whatever you already know**, so the worker
*executes* instead of *investigates*:

- what changed and the rough scope (you likely just edited these files)
- the intended branch name and commit intent (why the change exists)
- the base branch (`main`/`master`) if you already know it
- the repo's test command (from AGENTS.md, CLAUDE.md, Makefile, or package.json)
- anything the user just told you — target repo path, a split/bundle decision, "skip tests"

Rule: pass what is **already in context**; do not run expensive fresh discovery only to
feed the worker. If it is a cold invoke and you genuinely know nothing, pass the repo
path and let the worker discover the missing facts.

## Dispatch contract

Dispatch one general-purpose worker with shell and GitHub CLI access. Its prompt is the
**warm-start context** above followed by the **standard task text** below as one
self-contained string. The worker may have no conversation history, so include every
fact it needs. Wait for its result before taking the next step.

## Handling a NEEDS_DECISION return

The worker has no channel to the user, so it never asks questions. If its result starts
with `NEEDS_DECISION:`, it stopped before mutating anything. The invoking session must
ask the user through the host's structured choice prompt when available, using the
worker's proposed groupings as options. Fold the answer into the prompt and dispatch the
same task again. Never resolve the decision yourself.

## The task text to give the subagent

```
Ship the current uncommitted changes in this git repo end-to-end: branch off main,
commit, push, open a PR, merge it, and land back on main.

Context the caller already gathered may be prepended above this task. Trust it — a quick
`git status` sanity-check is fine, but don't re-derive from scratch what's already stated
(scope, branch name, base branch, test command). Only investigate what's missing.

1. Verify repo state.
   - Detect worktree mode first: if the path printed by `git rev-parse --git-dir`
     contains `/worktrees/`, you are in a LINKED WORKTREE. Worktree mode changes
     steps 3, 7, and 8 below — follow the "worktree:" variant wherever one is given.
   - `git status` — if already on a non-main branch with the intended changes, skip
     checkout. If on main with uncommitted changes, that's the normal case.
   - Confirm the base branch name (`git symbolic-ref refs/remotes/origin/HEAD` or
     `git remote show origin`) — usually main, occasionally master. Skip this if the
     prepended context already names the base branch.
   - Pre-flight before mutating anything: `gh auth status` succeeds and an `origin`
     remote exists (`git remote -v`). If either fails, stop and report it now —
     don't branch/commit only to discover at push time that the PR can't be opened.

2. Run tests before committing anything, using whatever this repo defines
   (make test, npm test, cargo test, pytest, etc — check AGENTS.md/CLAUDE.md/README/Makefile/
   package.json for the right command, or use the command named in the prepended
   context). Keep it cheap: if the diff clearly touches only a subset of
   packages/workspaces and the tooling supports scoping (e.g. `go test ./pkg/...`,
   `npm test -w <pkg>`), run the scoped subset instead of the full suite and say which
   scope you ran. If the task text says tests were already run or to skip them, skip and
   note that in the PR test plan (unchecked). If tests fail, stop and report the failures
   — do not commit broken code. If the repo has no test command, say so and continue.

3. Create the branch from the base branch: `git checkout -b <descriptive-name> <base>`.
   Name it from what the diff actually does (fix/..., feat/..., chore/...), not a
   generic name — use the name in the prepended context if given, else read the diff.
   - worktree: the worktree was almost always created with `git worktree add -b <branch>`,
     so you are already on a dedicated feature branch — skip the checkout. If the
     current branch name is generic, `git branch -m <descriptive-name>` is fine.

4. Stage deliberately, not blindly. Review `git status` and `git diff` before staging.
   Exclude build artifacts, plan output, or local scratch files that aren't gitignored
   but also aren't meant to be committed (e.g. .tfplan files, .DS_Store, editor swap
   files) — call these out rather than silently dropping them. Stage files by name;
   avoid `git add -A`/`git add .` when the working tree has anything ambiguous in it.

5. Commit with a message that explains why, not just what — read the actual diff
   content to write this, don't guess from file names. Follow the message style in the
   repo's own recent `git log` if visible.

6. Push and open the PR:
   `git push -u origin <branch>`
   `gh pr create --title "<short title>" --body "<summary + test plan>" --base <base>`
   PR body needs a `## Summary` (bullets of what changed and why) and a `## Test plan`
   (checklist — check what you actually ran, leave unchecked what you didn't, e.g.
   infra changes needing a live terraform plan/deploy to fully verify).

7. Merge: `gh pr merge --merge --delete-branch`. Use a real merge commit unless
   AGENTS.md, CLAUDE.md, or the repo's recent merged PRs show a consistent squash/rebase pattern —
   follow that instead and say so.
   - Conflict / behind main (common when a parallel session merged first): if the
     merge fails as not-mergeable, or `gh pr view <branch> --json mergeStateStatus -q
     .mergeStateStatus` returns `DIRTY`/`BEHIND`, sync the branch and retry — never
     force past it:
     ```
     git fetch origin <base>
     git rebase origin/<base>          # in this branch's checkout/worktree
     # mechanical conflicts only: resolve the files, `git rebase --continue`
     git push --force-with-lease
     ```
     then re-run the same `gh pr merge`. If the rebase conflict is non-mechanical (a
     real semantic overlap with what the other session landed), STOP: `git rebase
     --abort`, report the conflicting files, and let the user decide — never guess a
     resolution, never `--admin`/force-merge. This is the step that keeps concurrent
     sessions from clobbering each other on main.
   - worktree: if the task text says to stop at the PR (an orchestrator owns the
     merge queue), skip this step entirely and return the PR URL as the result.
     Otherwise merge with `gh pr merge --merge` and NEVER pass `--delete-branch` —
     the local branch is checked out by this worktree, so the delete fails
     (`error: cannot delete branch ... used by worktree`).

8. Land back on main: `gh pr merge` merges server-side via the API only — it does NOT
   update your local `<base>` or working tree. Sync explicitly:
   `git checkout <base> && git pull --ff-only`, then confirm with
   `git branch --show-current` and `git status`.
   - worktree: NEVER `git checkout <base>` here — git refuses because <base> is
     checked out in the primary working copy (`fatal: '<base>' is already used by
     worktree ...`). Instead find the primary copy (first path in
     `git worktree list`) and update it: `git -C <primary> pull --ff-only` if it is
     on <base> and clean, else just `git fetch origin <base>`. Do NOT remove the
     worktree you are standing in; report the cleanup commands instead, to run from
     the primary copy: `git worktree remove <this-path> && git branch -d <branch>`.

9. Report: PR link, what got merged, and what (if anything) was deliberately left out
   (like stray plan files) and why.

Judgment calls:
- Unrelated changes bundled in the working tree (e.g. an app bugfix + an unrelated
  infra edit): you cannot ask the user directly. Stop BEFORE branching or committing
  and return a message starting with the literal line `NEEDS_DECISION: split-or-bundle`
  followed by the proposed groupings (files per group, one-line rationale each).
  Do not proceed on your own. If the task text already states a split/bundle decision,
  follow it without stopping.
- No uncommitted changes: nothing to ship — say so instead of inventing a no-op
  branch/PR.
- Branch protection / required reviews block the merge: don't force-merge — report the
  blocker and stop (--admin is a deliberate override, never a default).
- Never `git clean` or delete untracked files to "clean up" — leave them out of the
  commit and mention them instead.

Run fully autonomously — no pausing for confirmation between steps (the single
exception is the NEEDS_DECISION early return above) — but narrate briefly as you go
(branch name, PR link, merge result) and return a final summary.
```
