---
name: codex-agent-worktree-setup
description: Use when creating new Codex threads, agents, or dev processes with isolated branch-bound worktrees; fixing Codex UI/thread/worktree coupling; repairing detached HEAD Codex worktrees; or protecting primary main/master worktrees while setting up branch-bound development agents.
---

# Codex Agent Worktree Setup

## Core Principle

Treat git isolation and Codex UI visibility as separate state that must be deliberately aligned.

A plain `git worktree add` creates git state only. It does not create a Codex-visible thread or agent. A Codex-created thread may create a managed worktree, but it still must be verified for cwd, branch, and detached HEAD state before any development begins.

## Decision Tree

```text
User asks for isolated git development only?
  -> Use normal git worktree flow.
  -> Do not claim a Codex agent/thread was created.

User asks for a new Codex process, agent, thread, UI-visible worker, or Codex-visible dev branch?
  -> Use Codex thread tools.
  -> Ensure the thread has its own worktree.
  -> Ensure that worktree is on the requested branch.

User asks why a branch/worktree is not visible in Codex?
  -> Explain that git branches/worktrees and Codex UI threads are different objects.
  -> Repair by creating or locating a Codex thread, not by only adding another git worktree.
```

## Main Worktree Guard

Before creating or repairing anything, identify the primary repository worktree and protect it.

- Never develop directly in a primary `main` or `master` worktree.
- Use the primary worktree only for read-only checks, branch reference creation, merges, rebases, pushes, or explicitly requested release work.
- If the primary worktree has uncommitted changes, stop and clarify ownership before changing refs or worktrees.
- If the target branch is already checked out in another worktree, stop and report that path. Do not remove or repoint it unless the user explicitly approves and the worktree is clean.
- Do not clean up `dev`, `dev1`...`dev9`, `codex/dev*`, or other agent branches unless the user explicitly approves.

## Preflight

Run these checks in the target repository before taking action. Keep the output in mind for final reporting.

```bash
pwd
git rev-parse --show-toplevel
git branch --show-current
git status --short --branch
git worktree list --porcelain
git show-ref --verify --quiet refs/heads/<branch>
git show-ref --verify --quiet refs/remotes/origin/<branch>
```

Interpretation:

- Local branch check exits `0`: local branch exists.
- Remote branch check exits `0`: `origin/<branch>` exists.
- Both branch checks fail: create a local branch ref before calling `create_thread`.
- Empty `git branch --show-current`: detached HEAD.
- `git worktree list --porcelain` shows the target branch under another `worktree`: branch is occupied.

## Codex-Visible Agent Flow

Use this flow when the user wants a Codex-visible process, agent, or thread.

1. Discover Codex thread/project tools if they are deferred.
   - Use the available tool discovery mechanism for `list_projects`, `create_thread`, `list_threads`, `read_thread`, and `set_thread_title`.
   - Do not substitute shell-only commands for these tools.

2. Locate the Codex project.
   - Call `list_projects`.
   - Match the requested project by path, name, or repository.
   - If no project matches, stop and report what projects were visible.

3. Ensure the target branch ref exists before thread creation.
   - If local `<branch>` exists, use it.
   - Else if `origin/<branch>` exists, create a local tracking or local branch ref without checking it out.
   - Else create a local branch ref from the requested base without checking it out:

```bash
# If origin/<branch> exists:
git branch <branch> origin/<branch>

# Otherwise, create from the requested base:
git branch <branch> <base>
```

4. Create the Codex thread.
   - Call `create_thread`.
   - Target must specify the project, an isolated worktree, and a branch starting state for `<branch>`.
   - If the tool returns a pending worktree setup id, report that state and verify once the worktree becomes available.

5. Confirm the thread exists.
   - Call `list_threads` and search for the created thread.
   - Call `read_thread` to inspect the thread cwd, project, and worktree path when available.
   - A git branch existing without a matching Codex thread is not enough.

6. Set a descriptive title.
   - Call `set_thread_title`.
   - Include branch, project, and responsibility.
   - Example: `dev9 OpenPet IM integration`.

## Branch And Worktree Verification

After creation or repair, verify both the primary worktree and the Codex-managed worktree.

In the primary worktree:

```bash
git branch --show-current
git status --short --branch
```

In the new Codex worktree:

```bash
git branch --show-current
git status --short --branch
```

Global check:

```bash
git worktree list --porcelain
```

Acceptance requires all three:

- Codex UI can find the thread.
- The thread cwd is an independent worktree, not the primary worktree.
- The worktree current branch is exactly `<branch>`, not detached HEAD.

## Detached HEAD Repair

If the Codex worktree is detached:

1. Confirm the Codex worktree is clean:

```bash
git status --short --branch
```

2. Confirm no other worktree occupies the target branch:

```bash
git worktree list --porcelain
```

3. If clean and unoccupied, switch inside the Codex worktree:

```bash
git switch <branch>
```

4. Re-run the verification commands.

If the worktree is dirty, stop and report the changed files. If the branch is occupied elsewhere, stop and report the occupying worktree path.

## Failure Handling

Use these outcomes instead of forcing progress:

| Situation | Required response |
| --- | --- |
| User wants Codex UI visibility but only a git branch/worktree exists | Create or locate a Codex thread; explain the distinction. |
| `create_thread` may fail because the branch does not exist | Create a local branch ref first with `git branch <branch> <base>`, without checking out main away from its branch. |
| Codex thread appears but cwd is the primary worktree | Treat setup as invalid; create or repair an isolated worktree before development. |
| Codex worktree is detached HEAD | Repair with `git switch <branch>` only after clean/unoccupied checks. |
| Target branch is checked out in another worktree | Stop and report the path; do not delete or steal the branch. |
| Primary worktree has uncommitted changes | Stop and clarify ownership. |
| Manual worktree blocks Codex binding | Remove only with explicit approval, after confirming it is clean and not user-owned. |

## Anti-Patterns

- Do not say "Codex agent created" after only running `git worktree add`.
- Do not start coding in a thread until cwd and branch are verified.
- Do not leave a Codex agent on detached HEAD.
- Do not switch the primary `main` or `master` worktree to the dev branch.
- Do not couple multiple agents to one worktree.
- Do not clean protected agent branches such as `dev/dev1..dev9` or `codex/dev*` without explicit approval.

## Compact Example

Request: "Create a dev9 Codex process, pin it to branch dev9, and do not touch main."

Expected handling:

1. Run preflight in `/Users/mango/project/codex/OpenPet`.
2. Confirm the primary worktree remains on `main` and is clean.
3. Check `dev9` local and `origin/dev9` refs.
4. If needed, create `dev9` from the requested base using `git branch dev9 <base>`.
5. Use `list_projects` to find OpenPet.
6. Use `create_thread` with OpenPet, isolated worktree, and `dev9` branch starting state.
7. Confirm with `list_threads` and `read_thread`.
8. In the new Codex worktree, verify `git branch --show-current` returns `dev9`.
9. If detached, repair with `git switch dev9` only after clean/unoccupied checks.
10. Rename the thread to something like `dev9 OpenPet IM integration`.
11. Report the thread id/name, worktree path, branch, and proof that primary OpenPet stayed on `main`.
