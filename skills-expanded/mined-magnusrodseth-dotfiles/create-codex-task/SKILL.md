---
name: create-codex-task
description: Creates a separate Codex task in a saved project, isolated worktree, local checkout, projectless directory, or ChatGPT Work cloud. Use when the user explicitly asks to create, start, or delegate work to a new Codex task.
---

# Create a Codex Task

Use "task" in user-facing text. Tool APIs may call it a thread.

## Requirements

Create a task only after an explicit user request. Do not treat ordinary work or a suggested follow-up as authorization.

Require an actionable initial prompt. Preserve the user's objective, constraints, relevant context, and completion criteria.

The skill requires the Codex app's `list_projects` and `create_thread` tools. If either tool is unavailable, explain that this host cannot create a Codex task.

## Resolve the destination

When the user names a project, repo, or directory, resolve it before project lookup:

```bash
~/dotfiles/.claude/skills/where-is/scripts/where-is.sh <name> --path-only
```

This is the canonical `where-is` resolver. Do not reimplement its search ladder.

- Exit 0: use the returned absolute path to match a saved project.
- Exit 2: show the candidates and ask the user which one. Never pick for them.
- Exit 1: say the directory was not found. Never invent a path.

Call `list_projects` and match the resolved path to the returned project `path`. Use that project's `projectId` and `isGitRepository`. A path that does not match a saved project cannot be used as a project target. Explain that it must first be saved as a Codex project, or offer a projectless task when that fits the request.

If the current task already identifies the exact saved project, path resolution is unnecessary. Still call `list_projects` to obtain its current ID and repository status.

Choose the target:

- Saved project: use `project`.
- Standalone work without a repository: use `projectless`.
- ChatGPT Work cloud: use only when explicitly requested.

For a saved project:

- Default to Worktree when `isGitRepository` is true.
- Default to Local when `isGitRepository` is false.
- Follow an explicit request to use Local or Worktree.
- Local runs directly in the saved project.
- Worktree creates an isolated checkout.

Ask one concise question only when the destination cannot be inferred safely.

## Select Worktree starting state

For Worktree:

- Omit `startingState` to start from the project default branch.
- Use `working-tree` when the user wants the current checkout, including uncommitted changes.
- Use `branch` for an explicitly named existing branch or ref.
- Set `onMissing: create-branch` only when the user explicitly requested that exact new branch name.
- Never invent a branch name.

## Model and reasoning

Omit `model` and `thinking` so the task inherits configured defaults.

Set either field only when the user explicitly requests an override. Use the models and reasoning efforts exposed by the current tool schema. Do not keep a static model list in this skill.

## Title

Infer a short, outcome-based title unless the user provides one.

## Create and confirm

Call `create_thread` with the resolved prompt, target, optional title, and explicit model or reasoning overrides.

Creation is asynchronous. When a ready `threadId` is returned, wait once for initial progress. A `clientThreadId` means Worktree setup is pending and cannot be passed to tools that require a ready thread.

Return the required created-task directive:

`::created-thread{threadId="..."}`

or, while setup is pending:

`::created-thread{clientThreadId="..."}`
