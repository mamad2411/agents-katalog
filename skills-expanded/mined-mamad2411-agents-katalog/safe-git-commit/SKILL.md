---
name: safe-git-commit
description: Safely stage and commit project changes under the AI Git policy. Use when finishing large changes, preparing commits, or checking commit readiness.
license: MIT
compatibility: agent-skills
metadata:
  source: project-adapted from Git workflow skills and this repo's ADR #52
---

# Safe Git Commit

Use this skill before creating any commit for this project.

## Policy

- Large changes are auto-committed after verification.
- Minor changes are not auto-committed; explain why.
- Use Conventional Commits.
- Never use `--no-verify` unless the user explicitly approves and the commit message explains why.

## Required Checks

1. `git status --short`
2. `git diff` or a path-limited diff for intended files
3. `git log --oneline -10`
4. Relevant validation commands for the change

## Staging Rules

- Stage only files belonging to the current task, unless the user explicitly confirms a broader scope.
- Never stage `draft/` or `DRAFT/`.
- Never stage local private config, generated caches, or unconfirmed temporary files.
- If intended and unintended changes overlap in the same file, ask before staging whole files or use a precise patch workflow.

## Commit Workflow

1. Summarize intended commit scope.
2. Confirm no unrelated staged files exist.
3. Stage intended files.
4. Inspect `git diff --cached --stat`.
5. Commit with a concise Conventional Commit message.
6. Run `git status --short` after commit and report leftovers.

## Stop Conditions

- Unexpected user changes conflict with the current task.
- The only way to commit is to include unrelated changes and the user has not approved that scope.
- Validation fails and the failure is not explicitly accepted by the user.
