---
name: safe-git-ops
description: "Perform common Git operations safely with sandbox-aware failure handling. Use whenever the user wants to inspect or modify git state, especially for cherry-pick, merge, rebase, commit, branch, stash, or worktree workflows. Always use this skill when the user mentions a Git failure, conflict, cherry-pick, merge issue, worktree, branch checkout problem, lock file, permission denied, operation not permitted, or any case where a sandboxed agent might confuse an environment restriction with a real code conflict. Be proactive: if the task smells like Git state or Git write behavior, use this skill even if the user did not explicitly ask for a 'Git' workflow."
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Safe Git Ops

Help the user perform common Git operations without confusing sandbox failures, repository state issues, and real content conflicts.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── failure-modes.md
    └── worktrees.md
```

## Progressive Loading

- Always read `references/failure-modes.md`
- Read `references/worktrees.md` when the repo uses `git worktree`, when `.git` points to another directory, or when the user mentions multiple worktrees

## Core Behavior

- Separate preflight inspection from state-changing Git commands
- Distinguish sandbox or permission failures from merge conflicts
- Treat worktrees as a special case because they may write shared Git metadata outside the visible working directory
- Ask before destructive operations such as `reset --hard`, `checkout --`, deleting branches, or dropping stashes
- Prefer non-interactive Git commands
- When a write operation is blocked by the sandbox, explain that clearly and request escalation instead of guessing about conflicts
- When a network Git operation fails, distinguish network/sandbox access from authentication, Git remote, or repository problems before asking the user to change credentials
- Bias toward early activation: if the user reports a Git failure in vague language, assume this skill should own the diagnosis before any state-changing command runs

## Trigger Heuristics

Use this skill immediately when any of these show up:

- the user asks to run `git cherry-pick`, `merge`, `rebase`, `commit`, `stash`, `switch`, `checkout`, `branch`, or `worktree`
- the user says "Git failed", "merge broke", "cherry-pick is blocked", "there is a conflict", or "why did this repo get into this state"
- the agent sees error text involving:
  - `CONFLICT`
  - `index.lock`
  - `operation not permitted`
  - `permission denied`
  - `Could not resolve host`
  - `Could not read from remote repository`
  - `Connection timed out`
  - `Network is unreachable`
  - `.git/worktrees/`
  - `ORIG_HEAD`
  - `CHERRY_PICK_HEAD`
  - `branch is already checked out`

Do not wait until after a failed write to load this skill if the task is obviously Git-heavy.

## Misdiagnoses To Avoid

Never say any of the following unless Git actually proved it:

- "this is a merge conflict" when the error is really permission-related
- "this is just local to the current worktree" when the common git dir may be involved
- "Git is broken" when the real issue is dirty state, detached HEAD, or an in-progress operation
- "your token/SSH key/remote is broken" when the first failure is a sandboxed network or DNS failure
- "just rerun it" without saying whether the block is conflict, repo state, or sandbox

## Step 1 — Orient the Repository

Before any meaningful Git action, inspect the repository shape:

```bash
git rev-parse --show-toplevel
git rev-parse --git-dir
git branch --show-current
git status --short
```

If the user mentions worktrees or `.git` is a file rather than a directory, also inspect:

```bash
git worktree list
git rev-parse --git-common-dir
```

Summarize:

- repo root
- current branch
- whether the tree is dirty
- whether this is a worktree
- whether shared Git metadata lives outside the current directory

## Step 2 — Classify the Requested Operation

Handle the request as one of these categories:

- `inspect`: status, log, diff, branch list, remotes, worktree layout
- `network_inspect`: fetch, pull, push dry checks, ls-remote, submodule update, or any Git operation that contacts a Git remote
- `safe_write`: add, commit, cherry-pick, merge, rebase, stash, branch creation, worktree creation
- `destructive_write`: reset, checkout over local changes, clean, branch deletion, stash drop, force push

For `inspect`, run the command directly if sandbox rules allow it.

For `network_inspect`, expect sandboxed runtimes to block DNS or outbound connections unless network permission is granted.

For `safe_write`, do a preflight check first.

For `destructive_write`, require explicit user confirmation before executing.

## Step 3 — Preflight Before Any State-Changing Git Command

Before `safe_write` or `destructive_write`, gather enough context to avoid sloppy failure handling:

```bash
git status --short
git branch --show-current
git rev-parse --short HEAD
```

For `cherry-pick`, `merge`, or `rebase`, also inspect the target commit or branch first:

```bash
git log --oneline --decorate -n 5
git show --stat --summary <target>
```

For worktrees, inspect the shared metadata location:

```bash
git rev-parse --git-common-dir
```

If the command will likely write to shared Git metadata outside the sandboxed writable root, tell the user this before running it and be ready to request escalation.

If the user specifically asked for a worktree-scoped write operation such as `cherry-pick`, `merge`, or `commit`, explicitly mention before running it that worktrees may require writes under the common git dir rather than only the visible worktree path.

## Step 4 — Execute and Interpret Failures Correctly

When a Git write fails, classify the failure before telling the user what happened.

Use the guidance in `references/failure-modes.md`. The high-level rule is:

- If Git reports `CONFLICT`, conflict markers, or asks to resolve files, this is a code conflict
- If Git reports `operation not permitted`, `permission denied`, failure to create lock files, or inability to update refs or worktree metadata, this is a sandbox or permission problem
- If Git reports DNS failure, API/host connection failure, timeout, or network unreachable during `fetch`, `pull`, `push`, `ls-remote`, or submodule operations, this is network/sandbox access until rerun with network permission
- If Git reports dirty state, untracked-file overwrite, detached HEAD mismatch, or missing commit, this is a repository state problem

Do not tell the user "there is a conflict" unless Git actually reported one.

Do not tell the user "authentication failed", "SSH key is wrong", or "the remote repo is missing" when Git never reached the host because of DNS/network/sandbox restrictions.

## Step 5 — Escalate Cleanly When Sandbox Restrictions Are the Real Problem

If a write command is important and fails because of sandbox restrictions:

1. State that the failure is environmental, not a code conflict
2. Name the blocked operation
3. Mention the likely write target if known, such as:
   - `.git/index.lock`
   - `.git/worktrees/...`
   - shared refs under the common git dir
4. Request permission escalation and rerun the same command

Use wording like:

> This `git cherry-pick` failure looks like a sandbox write restriction, not a merge conflict. Git needs to update shared worktree metadata, so I should rerun it with elevated permissions.

If a network Git command is important and fails because DNS, API, or host connection is blocked:

1. State that the first failure is network/sandbox access, not proven Git auth or remote configuration failure
2. Name the command, such as `git fetch`, `git push`, or `git ls-remote`
3. Request network permission and rerun the same command
4. Only after a network-enabled rerun should you classify credential, permission, missing-repo, branch, or server-side errors

Use wording like:

> This `git ls-remote` failure did not reach GitHub; it looks like sandboxed network access, not a missing repo or bad SSH key. I should rerun it with network permission before diagnosing credentials.

## Step 6 — Worktree-Specific Rules

When the repo uses worktrees:

- Assume `commit`, `cherry-pick`, `merge`, `rebase`, and similar commands may write outside the current worktree directory
- Check `git worktree list` and `git rev-parse --git-common-dir` early
- Avoid claiming that a failure is "local to this worktree" until you confirm where Git is trying to write
- Be extra careful with branch deletion or reset because another worktree may be using the same branch

Read `references/worktrees.md` for the detailed handling rules.

## Step 7 — Report Outcomes Precisely

When you finish, report one of these outcomes clearly:

- success
- conflict requiring manual resolution
- sandbox or permission restriction
- network/sandbox restriction
- repository state problem that needs a user choice

For each case, give the user the next action, not a vague Git dump.

Good example:

> `git cherry-pick <commit>` did not reach merge resolution. Git was blocked from writing shared worktree metadata under the common git dir, so this is a sandbox issue. The next step is to rerun the same command with elevated permissions.

Bad example:

> cherry-pick failed, probably a conflict

## Preferred Output Shape

When the user asked "what happened?" or "why did this fail?", report in this structure:

```text
Operation: <git command>
Classification: success | content conflict | sandbox restriction | network/sandbox restriction | repository state problem
Evidence: <the key git message or state observation>
Why it happened: <short explanation>
Next step: <single concrete next action>
```

Keep the classification line explicit. That is the main protection against sloppy Git diagnoses.

## Commands This Skill Should Handle Well

- `git status`, `log`, `diff`, `show`, `branch`, `remote`
- `git fetch`, `pull`, `push`, `ls-remote`
- `git add`, `commit`, `stash`
- `git cherry-pick`
- `git merge`
- `git rebase`
- `git switch`, `checkout`, `checkout -b`
- `git worktree list`, `git worktree add`

## Commands Requiring Extra Caution

- `git reset --hard`
- `git checkout -- <path>`
- `git clean -fd`
- `git branch -D`
- `git stash drop` or `clear`
- `git push --force`

Do not run these without explicit user approval.
