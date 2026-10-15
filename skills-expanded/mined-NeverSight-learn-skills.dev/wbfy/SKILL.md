---
name: wbfy
description: Apply `wbfy` to the current repository.
allowed-tools: Bash(bun:*), Bash(gh:*), Bash(git:*), Bash(yarn:*)
---

# wbfy application workflow

1. If the current branch is `main`, create and switch to a new branch from the latest remote `main` branch.
2. Run `yarn start <directory_path_of_target_repo>` in `~/ghq/github.com/WillBooster/wbfy`.
3. Run `yarn check-for-ai` or `bun check-for-ai` in the target repository (do not run this in `wbfy`).
4. If any checks fail, do one of the following:
   - Fix the issues in the target repository, then return to step 2.
   - If the failure originates from `wbfy`, fix `~/ghq/github.com/WillBooster/wbfy`, commit and push the changes, open a PR in the `wbfy` repository, then return to step 1.
5. Commit and push any changes in the target repository, then open a PR.
   - `wbfy` modifies various files in the target repository, so include all of them in the commit.
