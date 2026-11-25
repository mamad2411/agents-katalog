---
name: git-add-commit-push
description: Commit this session's work with explicit paths and a structured message, and push only when the user asked for a push. Use when the user says "commit", "push", "commiter", "pousser" or "save changes".
allowed-tools: Bash(git:*), Bash(gh:*)
user-invocable: true
---

# Commit (and push when asked)

The project's own rules (AGENTS.md, CLAUDE.md) win over this skill: commit gate, branch policy, publication authorization.

## Context

- Branch: !`git branch --show-current`
- Status: !`git status --short`
- Diff summary: !`git diff HEAD --stat`

## Steps

1. Run the project's pre-commit gate when it defines one (for example typecheck, lint and test from `package.json`). Stop and report on failure.
2. Stage only the files this session changed, by explicit path: `git add -- <path> <path>`. Never `git add .`, `git add -A` or `git commit -a`: parallel sessions and worktrees can share the index and working tree, and a broad add has swallowed another session's work before.
3. Check that `git diff --cached --stat` lists exactly those files; unstage anything else.
4. Commit with the format below. A message given by the user becomes the subject; still add the body.
5. Push only when the user asked to push: `git push -u origin <branch>`. Never push straight to the default branch unless the user asked for it, and never force-push without an explicit request.
6. Report the commit hash, the files and the push target.

## Message format

Subject: `type(scope): summary`, 72 characters at most.

Body, one or two lines per section (the same sections make a PR description):

- What: the change.
- Why: the problem or decision behind it.
- Proof: checks run and their result; native or device verification, or "pending".
- Delivery: what is actually live (deploy, OTA, binary, migration, with ids) versus pending.
- Tracking: the tracked item and its new status, follow-ups. Omit when there is none.

End with the attribution lines the session or project specifies.

## Finishing a branch

When the user wants to wrap up a branch, run the gate, then offer: push and open a PR (default), keep the branch, merge locally, or discard (only after a typed confirmation). Never delete a branch or worktree another session may own.
