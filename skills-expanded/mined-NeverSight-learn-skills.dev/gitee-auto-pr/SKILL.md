---
name: gitee-auto-pr
description: Create or update Gitee pull requests by pushing to protected branches in review mode (评审模式). Use when Codex is asked to push a branch so Gitee auto-creates or auto-updates a PR, to decide whether a push after `commit --amend`, `rebase`, `revert`, or other history rewriting will update the current auto PR or create a new one, or to keep the same PR by working on the generated `auto-*` source branch.
---

# Gitee Auto PR

## Overview

Use this skill for Gitee repositories that rely on protected branches in review mode instead of opening pull requests in the web UI. The key rule is commit-set based: Gitee updates an existing auto-created PR only if the pushed commits still fully contain that PR's diff commits.

Read `references/review-mode-rules.md` when you need the official rule summary, example commit graphs, or the two working styles documented by Gitee.

## Quick Start

1. Inspect repository state before pushing.

```bash
git remote -v
git branch --show-current
git status --short
git fetch origin
git log --oneline --decorate -n 10
```

2. Confirm the protected target branch.
- Treat the protected branch as the PR target branch.
- Ask once if the target branch is not already obvious from the user request, repository convention, or current branch naming.

3. Choose the push path.
- To create a PR or update an existing auto PR with new commits on top, push the current `HEAD` to the protected branch:

```bash
git push origin HEAD:<protected-branch>
```

- To keep working on the same existing auto PR, push to the generated `auto-*` source branch instead:

```bash
git push origin <auto-source-branch>
```

- If local history was rewritten and the user still wants the same PR, do not assume a protected-branch push will update it. Prefer the existing `auto-*` source branch or ask whether a new PR is acceptable.

## Update Decision

Use this rule before every push:

- If the new local history is a strict superset of the commits already represented by an existing auto PR, pushing to the protected branch updates that PR.
- If previous PR commits disappeared or were replaced because of `commit --amend`, `rebase`, `reset`, `revert`, or similar history rewriting, pushing to the protected branch creates a new PR.
- If there is no existing auto PR for this line of work, pushing to the protected branch creates a new PR.

Practical examples:

- Existing auto PR contains commit `5`; local history becomes `...-5-6`: update the same PR.
- Existing auto PR contains commits `5-6`; local history becomes `...-5-7`: create a new PR because `6` is no longer present.

## Execution Workflow

### Create or update through the protected branch

Use this path when the user wants Gitee to decide whether to create or update automatically.

```bash
git push origin HEAD:<protected-branch>
```

After pushing:

- Capture the terminal output.
- Report whether Gitee created or updated a PR.
- Return the PR URL if the remote printed one.

### Continue on the generated auto branch

Use this path when the repository already has an auto-created PR and the user wants to keep that same PR.

1. Find the source branch name from earlier push output, the Gitee UI, or remote refs.
2. Sync and switch if needed.

```bash
git fetch origin
git checkout <auto-source-branch>
```

3. Commit and push normally.

```bash
git push origin <auto-source-branch>
```

Do this especially after history rewriting, because a protected-branch push may create a new PR instead of updating the old one.

## Failure Modes

- If the push goes directly into the target branch and no PR is created, the branch is not effectively blocking this account or is not configured in review mode. Tell the user instead of pretending an auto PR exists.
- If the push is rejected, report the exact error and check branch protection, repository membership, and credentials.
- Avoid `--force` when the goal is "update the same PR". Rewritten history usually leads to a new PR decision when pushing to the protected branch.
