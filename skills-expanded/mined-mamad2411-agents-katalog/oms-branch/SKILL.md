---
name: oms-branch
description: Use when discovering, starting, switching, or deleting a branch inside an `oms/<alias>/` submodule — `oms branch list` to inspect choices, `oms branch switch` for local branches, `oms branch checkout` for remote branches, and `oms branch delete` for safe local deletion.
metadata:
  author: oh-my-space
  version: "1.0.0"
---

# Choose the right branch command inside a submodule

Branching happens inside a submodule (`oms/<alias>/`), which is its own Git repository. Picking the wrong command can leave the submodule in detached HEAD, where new commits are not on any branch and the root pointer cannot be recorded cleanly.

## Scope guardrail (applies before any Git work)

- Run `oms status --json` before Git work involving `oms/` to read root versus submodule state.
- Treat each `oms/<alias>/` directory as a separate Git repository.
- Use `oms` commands for scoped submodule workflows; do not guess root repository versus submodule Git scope.
- Do not create root commits for existing submodule pointer updates unless the user explicitly runs `oms record <alias>`.

## Switch versus checkout

- Run `oms branch list <alias>` to discover local and declared-remote branch choices before selecting an operation. It prepares safe existing registration and refreshes declared remotes automatically.
- `oms branch switch <alias> <branch>` starts or moves to a LOCAL branch, creating it locally if it does not exist yet. No remote is required. Use this to begin new work.
- `oms branch checkout <alias> <branch>` fetches `origin` and checks out an existing REMOTE branch (`origin/*`) as a local tracking branch. Use this to continue work that already exists on the remote.

## Avoid detached HEAD

Both commands attach HEAD to a branch. Prefer them over a raw `git checkout <sha>` inside the submodule, which detaches HEAD. If `oms status --json` shows a submodule with no branch (detached), attach one with `oms branch switch` before committing.

## Delete a LOCAL branch

- `oms branch delete <alias> <branch>` removes one LOCAL branch inside a submodule with a safe delete. It is local-only: it never deletes a remote branch or a remote-tracking ref, and never touches the root pointer. To remove a branch on the remote, use plain Git against the remote instead — this command does not do that.
- Deleting an unmerged branch is refused by the safe delete; force it with `oms branch delete <alias> <branch> --force` only when losing its unmerged commits is intended. Force still cannot delete the current branch or a baseline branch.
- Omit the alias or branch to choose interactively; protected branches (current and baseline) are shown but not selectable.
- Do not `cd` into `oms/<alias>/` and run raw `git branch -d/-D`; the command resolves and protects baseline branches for you.

These instructions were written against `oms status --json` schemaVersion 1. If `oms status --json` reports a different schemaVersion, defer to `oms status --help` for exact field semantics. Defer branch inventory fields, preparation, freshness, and exit behavior to `oms branch list --help`; defer remaining flag detail to `oms branch switch --help`, `oms branch checkout --help`, and `oms branch delete --help`.
