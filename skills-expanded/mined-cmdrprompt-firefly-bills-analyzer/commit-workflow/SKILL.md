---
name: commit-workflow
description: "Use when creating branches, staging, or committing in a python-butler governed repository - including from an isolated worktree. Covers task branch naming, make branch-task, stage-current-task, commit-current-task, commit-output, merge-worktree, and the rules that forbid direct git commit. Keywords: commit, branch, stage, worktree, task branch, git."
---

# Commit workflow

All git write operations in a python-butler governed repository go through
`make` targets. Never run `git commit`, `git add` (outside the worktree
auto-fix flow below), `git push --force`, or any destructive git command
directly. If a required target is missing from the Makefile, stop and report
it instead of falling back to raw git.

## Branch discipline

- Every task runs on its own branch named `task/<NNN>-short-description`,
  where NNN is the TASK-ID zero-padded to 3 digits.
- Create or switch with `make branch-task f=TASK-XXX`. Never work on `main`.
- If the task branch is behind `main`, run `make sync-main` before coding.
  An out-of-date branch is a blocking condition.

## Which path applies: check the branch name, not how you were told you were invoked

Before committing, run `git branch --show-current` and decide from the
actual name - do not rely on being told you're "in a worktree" or "on a
task branch," since that framing can be wrong or ambiguous:

- Branch matches `task/<NNN>-...` -> you are on a real task branch, even if
  the work happened inside a subagent. Use "Committing on a task branch"
  below.
- Branch does NOT match `task/<NNN>-...` (e.g. an `agent-<hash>` worktree
  branch) -> use "Committing from an isolated worktree" below.

## Committing on a task branch

1. Run `make stage-current-task` - it auto-fixes (ruff, format, pymarkdown)
   and stages the files listed in the task file, including `CHANGELOG.md`.
2. Run `make commit-current-task` - it commits using the message on the
   task file's `**Commit:**` line.
3. If the commit message needs to change, edit the `**Commit:**` line in the
   task file first, then run `make commit-current-task`. Never pass a message
   with `git commit -m`.

With an explicit task ID: `make stage-task f=TASK-XXX` and `make commit-task`.
PR and merge: `make pr-current-task`, then `make merge-current-task`
(squash-merge and pull main) when the PR is conflict-free.

## Committing from an isolated worktree

Subagents spawned with `isolation: "worktree"` work on a temporary branch
that does NOT match `task/<NNN>-...`, so `stage-current-task` and
`commit-current-task` are unavailable there. If `git branch --show-current`
shows a `task/<NNN>-...` name instead, you are not in this situation - use
"Committing on a task branch" above, even if you were told you might be
running in a worktree. Otherwise:

1. Run the auto-fix steps yourself: `ruff check --fix .`, `ruff format .`,
   and pymarkdown fix, then `git add` the changed files.
2. Commit with `make commit-output f="<changed files>" m="wip(TASK-XXX):
   <short summary>"`, substituting the real TASK-ID. This is the only commit
   path guaranteed to work from a worktree branch. The wip message does not
   need to match the task file's `**Commit:**` line.
3. An uncommitted worktree is torn down with no branch returned - the work is
   silently discarded and cannot be recovered. Commit before finishing.
4. If `make commit-output` is not defined in the Makefile, ask the Workflow
   Guardian to add it before committing.

## Merging a worktree branch (coordinator side)

When a worker subagent returns a worktree branch name:

1. Run `make merge-worktree b=<branch>` - this squashes the worker's
   commit(s) into staged changes via `git merge --squash`.
2. Run `make commit-current-task` to create the single real commit using the
   task file's actual commit message.
3. If no branch is returned, or `make merge-worktree` reports nothing to
   squash, the worker failed to commit - perform the work directly in the
   main conversation instead.

## Safety rules

- Never use destructive git commands (reset --hard, force push, clean)
  unless the user explicitly requests it.
- Do not revert or discard unrelated dirty changes.
- Keep every commit scoped to its task.
