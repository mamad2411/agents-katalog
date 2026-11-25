---
name: workspace-isolation
description: "Use before approved implementation plans or substantial feature/fix work when workspace isolation, branch provenance, setup baseline, or worktree safety must be decided."
---

# Workspace Isolation

Use this before substantial implementation starts. The goal is to protect the user's current checkout and create baseline evidence without fighting the runtime.

## Ownership

- Top-level session or PM/coordinator owns isolation decisions.
- Specialists may request this skill through `NEEDS_CONTEXT` when the packet lacks workspace, branch, or baseline facts.
- Do not create, remove, or rewrite worktrees as a delegated specialist unless PM explicitly assigned that setup task.

## Flow

1. Detect current state:
   - `git rev-parse --show-toplevel`
   - `git rev-parse --git-dir`
   - `git rev-parse --git-common-dir`
   - `git rev-parse --show-superproject-working-tree`
   - `git branch --show-current`
   - `git status --short`
2. If `git-dir` and `git-common-dir` differ and the repo is not a submodule, treat the checkout as already isolated. Record path, branch or detached state, and skip worktree creation.
3. Prefer runtime-native workspace/worktree tools when available. Do not use manual `git worktree` when the host runtime owns isolation.
4. Manual worktree fallback is allowed only when the user already authorized implementation or isolation and the target directory is safe:
   - Prefer an existing ignored `.worktrees/` directory.
   - Otherwise prefer an existing ignored `worktrees/` directory.
   - If no ignored project-local directory exists, return `NEEDS_USER_INPUT` with options: add an ignored `.worktrees/`, use a user-named location, or work in place.
5. Run the smallest project setup and baseline checks from `.github/instructions/project.instructions.md`. If those commands are unknown or fail, report the blocker before implementation.

## Safety Rules

- Never add `.gitignore`, create external directories, or run network-heavy setup unless authorized by PM/top-level flow and tool permissions.
- Never delete a worktree here. Cleanup belongs to `development-branch-closeout`.
- Do not treat a submodule as an isolated worktree.
- If sandbox or permissions block isolation, record `isolation_status=blocked` and continue only if PM chooses work-in-place or stops the task.

## Output

Return or record these fields in the PM packet:

- `workspace_path`
- `branch_state`
- `isolation_status`: `already_isolated | created | work_in_place | blocked`
- `baseline_commands`
- `baseline_result`
- `next_owner`
