---
name: complete-pr
description: Complete GitHub pull requests by iterating on CI and review feedback until the PR is ready.
---

Use this skill when the goal is to drive a PR to a merge-ready state rather than just inspect it once.
First, fetch the current repository owner with `gh repo view --json owner --jq '.owner.login'`.
If the owner is `WillBooster` or `WillBoosterLab`, follow the first workflow below.
Otherwise, follow the second workflow below.

## Workflow for `WillBooster` or `WillBoosterLab` repositories

1. Check the results of CI (GitHub Actions) with the `github-pr` skill.
2. If the latest run of any workflow has failed, fix the relevant code, commit, push, and then return to step 1.
3. Fetch unresolved review threads.
4. Review each unresolved thread and decide whether it requires a code or documentation change. Ignore only comments that are clearly outdated, incorrect, or intentionally declined with solid reasoning.
5. If there are valid review comments to address, make the changes, commit, push, and post `/gemini review` to the PR.
6. Reply to all review threads with the `github-pr` skill.
7. If you made any changes in step 5, wait for 5 minutes then return to step 1. Otherwise, stop.

## Workflow for the other repositories

1. Check the results of CI (GitHub Actions) with the `github-pr` skill.
2. If the latest run of any workflow has failed, fix the relevant code, commit, push, and then return to step 1.
3. Fetch unresolved review threads.
4. Review each unresolved thread and decide whether it requires a code or documentation change. Ignore only comments that are clearly outdated, incorrect, or intentionally declined with solid reasoning.
5. If there are valid review comments to address, make the changes, commit, push, and then return to step 1. Otherwise, stop.
   - Do not post any message like review replies on non-WillBooster repositories.
